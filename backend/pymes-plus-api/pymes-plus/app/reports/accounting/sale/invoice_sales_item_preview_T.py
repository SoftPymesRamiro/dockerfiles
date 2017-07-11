__author__ = "SoftPymes"
__credits__ = ["Chelo"]

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color
import os
from .... import session
from itertools import groupby
import uuid
from ....models import DefaultValue
from ....utils.math_ext import _round
from ....utils.image_converter import ImagesConverter
from ....utils.converters import total_to_letter
from ...libs.functions import paragraph_over_flow, paragraph_over_flow_height

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        # self.preview_data = preview_data

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_footer_n_header(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_footer_n_header(self, page_count):
        """
        draw page footer and page header if the file is on the last page also draw the total of the document
        :param page_count:
        :return:
        """
        preview_data = SaleItemPreviewT.preview_data

        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId,
                                         DefaultValue.currencyId) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        # FOOTER

        # declara estilos para los parrafos del footer
        style_p_footer = ParagraphStyle('Normal')
        style_p_footer.fontName = 'Arial'
        style_p_footer.fontSize = 8
        style_p_footer.leading = 8

        style_p_footer_centred = ParagraphStyle('Normal')
        style_p_footer_centred.fontName = 'Arial'
        style_p_footer_centred.fontSize = 8
        style_p_footer_centred.leading = 8
        style_p_footer_centred.alignment = TA_CENTER

        style_p_header_cards_centred = ParagraphStyle('Normal')
        style_p_header_cards_centred.fontName = 'Helvetica-Oblique'
        style_p_header_cards_centred.fontSize = 8
        style_p_header_cards_centred.leading = 8
        style_p_header_cards_centred.alignment = TA_CENTER

        #factura impresa
        style_printed_invoice_footer_centred = ParagraphStyle('Normal')
        style_printed_invoice_footer_centred.fontName = 'Arial'
        style_printed_invoice_footer_centred.fontSize = 7
        style_printed_invoice_footer_centred.leading = 8
        style_printed_invoice_footer_centred.alignment = TA_CENTER


        style_p_footer_right = ParagraphStyle('Normal')
        style_p_footer_right.fontName = 'Arial'
        style_p_footer_right.fontSize = 7
        style_p_footer_right.leading = 8
        style_p_footer_right.alignment = TA_RIGHT

        # estilo generico de la tabla - borde negro con pequeño padding
        table_style_footer_general = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        table_style_footer_taxes = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, 0), 0),
                ('LEFTPADDING', (0, 1), (-1, 1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, 0), 0),
                ('RIGHTPADDING', (0, 1), (-1, 1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        table_style_footer_observations = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, 0), 0.15 * cm),
                ('BOX', (0, 0), (0, 0), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_footer_totaling = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        # HEADER

        table_style_header = TableStyle(
            [
                # ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('LEFTPADDING', (0, -1), (0, -1), 0),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, -1), (0, -1), 0),
                ('TOPPADDING', (0, 0), (0, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, -1), 0),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        table_style_header_general = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (-2, 0), (-2, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('LEFTPADDING', (-1, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (-2, 0), (-2, -1), 0),
                ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (-2, 0), (-2, -1), 0.1 * cm),
                # ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('SPAN', (1, 0), (-1, 0)),
                ('SPAN', (1, 1), (3, 1)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )
        #tirilla
        table_style_header_general2 = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                # ('LEFTPADDING', (-2, 0), (-2, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                # ('LEFTPADDING', (-1, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                # ('RIGHTPADDING', (-2, 0), (-2, -1), 0),
                ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                # ('RIGHTPADDING', (-2, 0), (-2, -1), 0.1 * cm),
                # ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (1, 0), (-1, 0)),
                # ('SPAN', (1, 1), (3, 1)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        table_style_header_date_validity = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('LEFTPADDING', (1, 0), (-1, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('RIGHTPADDING', (0, 0), (-2, 0), 0),
                # ('TOPPADDING', (0, 0), (-1, 0), 0.24 * cm),
                # ('BOTTOMPADDING', (0, 0), (-1, 0), 0.1 * cm),
                # ('BOTTOMPADDING', (0, -1), (-1, -1), 0.31 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('VALIGN', (0, 0), (-3, -1), 'TOP'),
                # ('VALIGN', (-2, 0), (-1, -1), 'MIDDLE'),
                ('SPAN', (1, 2), (-1, -2)), #span para plazo
                ('SPAN', (2, 3), (-1, -1)),#span para tasa de cambio
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        #estilo moneda extranjera
        table_style_header_date_validity2 = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('LEFTPADDING', (1, 0), (-1, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('RIGHTPADDING', (0, 0), (-2, 0), 0),
                # ('TOPPADDING', (0, 0), (-1, 0), 0.24 * cm),
                # ('BOTTOMPADDING', (0, 0), (-1, 0), 0.1 * cm),
                # ('BOTTOMPADDING', (0, -1), (-1, -1), 0.31 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('VALIGN', (0, 0), (-3, -1), 'TOP'),
                # ('VALIGN', (-2, 0), (-1, -1), 'MIDDLE'),
                # ('SPAN', (1, 2), (-1, -2)),  # span para plazo
                # ('SPAN', (2, 3), (-1, -1)),  # span para tasa de cambio
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        table_style_header_order_no = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('TOPPADDING', (0, 0), (0, 0), 0 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                # ('SPAN', (0, 1), (-1, -1)),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        table_style_header_description = TableStyle(
            [
                ('LEFTPADDING', (1, 0), (-1, 0), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        table_style_header_cards = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                # ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                # ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_footer_sing = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM')
            ]
        )

        style_p_header = ParagraphStyle('Normal')
        style_p_header.fontName = 'Arial'
        style_p_header.fontSize = 12
        style_p_header.leading = 12
        style_p_header.rightIndent = 2.8 * cm
        style_p_header.leftIndent = 2.8 * cm
        style_p_header.alignment = TA_CENTER
        # style_p_header.backColor = '#FFFF00'

        #TIRILLA
        style_p_header_t = ParagraphStyle('Normal')
        style_p_header_t.fontName = 'Arial'
        style_p_header_t.fontSize = 6
        style_p_header_t.leading = 10
        style_p_header_t.alignment = TA_CENTER

        style_p_header_tR = ParagraphStyle('Normal')
        style_p_header_tR.fontName = 'Arial'
        style_p_header_tR.fontSize = 6
        style_p_header_tR.leading = 10
        style_p_header_tR.alignment = TA_RIGHT

        style_p_header_tL = ParagraphStyle('Normal')
        style_p_header_tL.fontName = 'Arial'
        style_p_header_tL.fontSize = 6
        style_p_header_tL.leading = 10
        style_p_header_tL.alignment = TA_LEFT

        #--------------------------------------------------

        style_p_sub_header = ParagraphStyle('Normal')
        style_p_sub_header.fontName = 'Arial'
        style_p_sub_header.fontSize = 10
        style_p_sub_header.leading = 10
        style_p_sub_header.rightIndent = 2.8 * cm
        style_p_sub_header.leftIndent = 2.8 * cm
        style_p_sub_header.alignment = TA_CENTER
        # style_p_sub_header.backColor = '#FFFF00'

        style_p_sub_header_ica = ParagraphStyle('Normal')
        style_p_sub_header_ica.fontName = 'Arial'
        style_p_sub_header_ica.fontSize = 9.5
        style_p_sub_header_ica.leading = 9.5
        style_p_sub_header_ica.rightIndent = 0
        style_p_sub_header_ica.leftIndent = 0
        style_p_sub_header_ica.alignment = TA_CENTER
        # style_p_sub_header_ica.backColor = '#FFFF00'

        style_p_header_provider = ParagraphStyle('Normal')
        style_p_header_provider.fontName = 'Arial'
        style_p_header_provider.fontSize = 8
        style_p_header_provider.leading = 8
        # style_p_header_provider.backColor = '#FFFF00'

        style_p_header_description_right = ParagraphStyle('Normal')
        style_p_header_description_right.fontName = 'Arial'
        style_p_header_description_right.fontSize = 8
        style_p_header_description_right.leading = 8
        style_p_header_description_right.alignment = TA_RIGHT

        style_p_header_date_validity = ParagraphStyle('Normal')
        style_p_header_date_validity.fontName = 'Arial'
        style_p_header_date_validity.fontSize = 7
        style_p_header_date_validity.leading = 7

        style_p_header_extra_validity = ParagraphStyle('Normal')
        style_p_header_extra_validity.fontName = 'Arial'
        style_p_header_extra_validity.fontSize = 7.5
        style_p_header_extra_validity.leading = 7

        style_p_header_date_validity_right = ParagraphStyle('Normal')
        style_p_header_date_validity_right.fontName = 'Arial'
        style_p_header_date_validity_right.fontSize = 8
        style_p_header_date_validity_right.leading = 8
        style_p_header_date_validity_right.alignment = TA_RIGHT

        style_p_annuled = ParagraphStyle('Normal')
        style_p_annuled.fontName = 'Arial'
        style_p_annuled.fontSize = 50
        style_p_annuled.leading = 50
        style_p_annuled.textColor = Color(255, 0, 0, alpha=0.3)

        def footer(cnv):
            """
            draw the page footer
            :param cnv:
            :return:
            """
            cnv.saveState()

            # INFORMACIÓN DE LA TABLA DE DESPACHO ---------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:
                data_footer_send = [
                    [
                        Paragraph('<b>Ship to / Despachar Producto a</b>', style_p_footer),
                        ''
                    ],
                    [
                        Paragraph(paragraph_over_flow(text=preview_data['shipTo'].upper(),
                                                      width=6.3,
                                                      font_size=8,
                                                      leading=8), style_p_footer),
                        Paragraph('', style_p_footer)
                    ],
                    [
                        Paragraph(paragraph_over_flow(text=preview_data['shipAddress'],
                                                      width=6.3,
                                                      font_size=8,
                                                      leading=8), style_p_footer),
                        Paragraph('', style_p_footer)
                    ],
                    [
                        Paragraph(paragraph_over_flow(text='{0}, {1}'.format(preview_data['shipCity'],
                                                                             preview_data['shipDepartment']),
                                                      width=6.3,
                                                      font_size=8,
                                                      leading=8), style_p_footer),
                        Paragraph('', style_p_footer)
                    ],
                    [
                        Paragraph(paragraph_over_flow(text=preview_data['shipCountry'],
                                                      width=6.3,
                                                      font_size=8,
                                                      leading=8), style_p_footer),
                        Paragraph('', style_p_footer)
                    ],
                    [
                        Paragraph('', style_p_footer),
                        Paragraph('', style_p_footer)
                    ]
                ]

                # Tabla con datos de despacho
                table_footer_send = Table(
                    data_footer_send,  # Contenido de la tabla
                    [6.8 * cm, 0.1 * cm],  # Ancho de las columnas
                    [0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.5 * cm, 0.32 * cm],
                    style=table_style_footer_general  # Estilos de la tabla
                )

                # Denota el contenor de la tabla
                table_footer_send.wrap(6.5 * cm, 2.6 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                table_footer_send.drawOn(cnv, 1 * cm, 4.9 * cm)

            # INFORMACIÓN DE LA TABLA DE DESPACHO - FIN ---------------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE TOTAL ------------------------------------------------------------------------

            total_base_value = 0
            for dct_det in preview_data['document_details']:
                total_base_value += dct_det.baseValue

            sub_total = 0
            descuento = 0
            otro_descuento = 0
            base_gravable = 0
            iva = 0
            impo_consumo = 0
            rete_fuente = 0
            neto_a_pagar = 0
            interest = 0
            value_cree = 0
            rete_ica_value = 0
            rete_iva_value = 0
            retention_value = 0
            over_cost = 0
            disccount2 = ''
            percentage_cree = ''
            rete_ica_percent = ''
            rete_iva_percent = ''

            if page_count == self._pageNumber:
                sub_total = _round(preview_data['sub_total'], default_decimals.valueDecimals)
                descuento = _round(preview_data['discount'], default_decimals.valueDecimals)
                otro_descuento = _round(preview_data['discount2'], default_decimals.valueDecimals)
                base_gravable = _round(total_base_value, default_decimals.valueDecimals)
                iva = _round(preview_data['iva'], default_decimals.valueDecimals)
                impo_consumo = _round(preview_data['consumptionTaxValue'], default_decimals.valueDecimals)
                rete_fuente = _round(preview_data['withholdingTaxValue'], default_decimals.valueDecimals)
                neto_a_pagar = _round(preview_data['total'], default_decimals.valueDecimals)
                interest = _round(preview_data['interest'], default_decimals.valueDecimals)
                value_cree = _round(preview_data['valueCREE'], default_decimals.valueDecimals)
                rete_ica_value = _round(preview_data['reteICAValue'], default_decimals.valueDecimals)
                rete_iva_value = _round(preview_data['reteIVAValue'], default_decimals.valueDecimals)
                retention_value = _round(preview_data['retentionValue'], default_decimals.valueDecimals)
                over_cost = _round(preview_data['overCost'], default_decimals.valueDecimals)
                disccount2 = _round(preview_data['disccount2P'], 2)
                percentage_cree = _round(preview_data['percentageCREE'], 2)
                rete_ica_percent = _round(preview_data['reteICAPercent'], 2)
                rete_iva_percent = _round(preview_data['reteIVAPercent'], 2)

            if preview_data['currencyId'] != default_decimals.currencyId:
                data_footer_totaling = [
                    [
                        Paragraph('<b>SALES / TOTAL VENTA</b>', style_p_footer_right),
                        Paragraph('${:20,.{}f}'.format(_round(sub_total, default_decimals.valueDecimals),
                                                              default_decimals.valueDecimals), style_p_footer_right)
                    ],
                    [
                        Paragraph('<b>SHIPPING AND HANDLING/ TRANSPORTE Y MANEJO</b>', style_p_footer_right),
                        Paragraph('${:20,.{}f}'.format(_round(preview_data['freight'], default_decimals.valueDecimals),
                                                       default_decimals.valueDecimals), style_p_footer_right)
                    ],
                    [
                        Paragraph('<b>SALES TAX / IVA</b>', style_p_footer_right),
                        Paragraph('${:20,.{}f}'.format(_round(iva, default_decimals.valueDecimals),
                                                       default_decimals.valueDecimals), style_p_footer_right)
                    ],
                    [
                        Paragraph('<b>DISCOUNT / DESCUENTO</b>', style_p_footer_right),
                        Paragraph('${:20,.{}f}'.format(_round(descuento, default_decimals.valueDecimals),
                                                       default_decimals.valueDecimals), style_p_footer_right)
                    ],
                    [
                        Paragraph('<b>TOTAL</b>', style_p_footer_right),
                        Paragraph('<b>${:20,.{}f}</b>'.format(_round(neto_a_pagar, default_decimals.valueDecimals),
                                                       default_decimals.valueDecimals), style_p_footer_right)
                    ]
                ]

                table_footer_totaling = Table(
                    data_footer_totaling,  # Contenido de la tabla
                    [9.9 * cm, 2.8 * cm],  # Ancho de las columnas

                    style=table_style_footer_totaling  # Estilos de la tabla
                )

                # Denota el contenor de la tabla
                table_footer_totaling.wrap(12.7 * cm, 4.2 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                table_footer_totaling.drawOn(cnv, 7.9 * cm, 4.9 * cm)
                # linea total
                cnv.line(18 * cm, 5.4 * cm, 20.6 * cm, 5.4 * cm)

            # linea de medicion borde derecho
            # cnv.line(20.6 * cm, 30 * cm, 20.6 * cm, 2 * cm)
            #linea medicion tabla subtotal y despacho
            # cnv.line(13.7 * cm, 30 * cm, 13.7 * cm, 1 * cm)

            # INFORMACIÓN DE LA TABLA DE TOTAL - FIN ------------------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES ----------------------------------------------------------------
            style_observaciones_extra = ParagraphStyle('Normal')
            style_observaciones_extra.fontName = 'Arial'
            style_observaciones_extra.fontSize = 8
            style_observaciones_extra.leading = 8
            style_observaciones_extra.alignment = TA_JUSTIFY

            if preview_data['currencyId'] != default_decimals.currencyId:
                par_observations = paragraph_over_flow_height(text=preview_data['comments'].capitalize(),
                                                              width=6.6,
                                                              no_par=3,
                                                              font_size=8,
                                                              leading=8)

                data_footer_observations = [
                    [
                        Paragraph('<para><b>Notes/Observaciones:</b> {0} </para>'.format(par_observations)
                                  , style_observaciones_extra),
                    ]
                ]

                table_footer_observations = Table(
                    data_footer_observations,
                    [6.9 * cm, ],
                    [2 * cm, ],
                    style=table_style_footer_observations

                )

                # Denota el contenor de la tabla
                table_footer_observations.wrap(12.7 * cm, 1.6 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                table_footer_observations.drawOn(cnv, 1 * cm, 1.6 * cm)

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES - FIN ----------------------------------------------------------

            #FACTURA IMPRESA --------------------------------------------------------------------------------------------------

            text_change = ''
            #AUTORIZADA
            if preview_data['type_resolution'] == 0 and preview_data['months'] == 0:
                text_change = 'Numeración Autorizada por la DIAN según la Resolución ' \
                              'N° {0} de {1} desde {2} {3} hasta {4} {5}'.format(
                                                                            preview_data['resolution'],
                                                                            preview_data['resolution_date'],
                                                                            preview_data['prefix_resolution'],
                                                                            preview_data['consecutive_from'],
                                                                            preview_data['prefix_resolution'],
                                                                            preview_data['consecutive_to'])

            # con mes
            elif preview_data['type_resolution'] == 0 and preview_data['months'] > 0:
                consecutive_end = int(preview_data['consecutive_to'])
                conseutive_ini = int(preview_data['consecutive_from'])

                if preview_data['months'] > 1:
                    mes = 'meses'
                else:
                    mes = 'mes'

                text_change = 'Autorización Numeración de Facturación N° {0} de {1} ' \
                              'desde {2} {3} hasta {4} {5} con ' \
                              'vigencia de {6} {7}'.format(preview_data['resolution'],
                                                               preview_data['resolution_date'],
                                                               preview_data['prefix_resolution'],
                                                               conseutive_ini,
                                                               preview_data['prefix_resolution'],
                                                               consecutive_end,
                                                               preview_data['months'],
                                                           mes)
            # habilitada
            elif preview_data['type_resolution'] == 1 and preview_data['months'] == 0:
                text_change = 'Numeración Habilitada por la DIAN según la Resolución ' \
                              'N° {0} de {1} desde {2} {3} hasta {4} {5}'.format(
                                                                            preview_data['resolution'],
                                                                            preview_data['resolution_date'],
                                                                            preview_data['prefix_resolution'],
                                                                            preview_data['consecutive_from'],
                                                                            preview_data['prefix_resolution'],
                                                                            preview_data['consecutive_to'])

            elif preview_data['type_resolution'] == 1 and preview_data['months'] > 0:
                consecutive_end = int(preview_data['consecutive_to'])
                conseutive_ini = int(preview_data['consecutive_from'])

                if preview_data['months'] > 1:
                    mes = 'meses'
                else:
                    mes = 'mes'

                text_change = 'Habilitación con  Autorización Numeración de Facturación ' \
                              'N° {0} de {1} desde {2} {3} hasta {4} {5} ' \
                              'con vigencia de {6} {7}'.format(preview_data['resolution'],
                                                                   preview_data['resolution_date'],
                                                                   preview_data['prefix_resolution'],
                                                                   conseutive_ini,
                                                                   preview_data['prefix_resolution'],
                                                                   consecutive_end,
                                                                   preview_data['months'],
                                                               mes)

            information_doc = 'FACTURA IMPRESA POR COMPUTADOR (Art. 617 E.T y Decreto 1165/96 Art. 13) ' \
                              '<br/>El (los)comprador(es) la firma(n) en señal de aceptación y de haber recibido ' \
                              'real y materialmente la mercancia y/o el servicio ' \
                              '<br/>{0}' \
                              '<br/><b>{1}</b> - <b>{2}</b>'.format(text_change,
                                                                    preview_data['company_web'],
                                                                    preview_data['company_email'])

            if preview_data['currencyId'] != default_decimals.currencyId:
                data_footer_total_word = [
                    [
                        Paragraph(information_doc, style_printed_invoice_footer_centred),
                    ]
                ]

                table_footer_total_word = Table(
                    data_footer_total_word,
                    [19.6 * cm, ],
                    [1.3 * cm, ],
                    style=table_style_footer_observations
                )

                # Denota el contenor de la tabla
                table_footer_total_word.wrap(19.6 * cm, 1.1 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                table_footer_total_word.drawOn(cnv, 1 * cm, 3.6 * cm)

            #FACTURA IMPRESA - FIN--------------------------------------------------------------------------------------------------

            # INFORMACIÓN DEL FIRMA -----------------------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:

                data_footer_sing = [

                    [
                        Paragraph('Company / Empresa', style_p_footer_centred),
                        Paragraph('Customer / Cliente', style_p_footer_centred)
                    ]
                ]

                # Tabla con datos de despacho
                table_footer_sing = Table(
                    data_footer_sing,  # Contenido de la tabla
                    [6.35 * cm, 6.35 * cm],  # Ancho de las columnas
                    [2 * cm],
                    style=table_style_footer_sing  # Estilos de la tabla
                )
                # Denota el contenor de la tabla
                table_footer_sing.wrap(12.7 * cm, 2.6 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                table_footer_sing.drawOn(cnv, 7.9 * cm, 1.6 * cm)

                documento = ''
                if preview_data['copy_or_original'] == '1':
                    documento = 'ORIGINAL'
                else:
                    documento = 'COPIA'

                company_information = Paragraph('Contabilidad Pymes+ NIT 830.506.365-7 '
                                                'Teléfono: (572) 3828300 Cali. '\
                                                'www.softpymes.com.co<br/> ***{0}***'.format(documento),
                style_p_footer_centred)

                # Denota el contenor de la tabla
                company_information.wrap(16 * cm, 0.8 * cm)
                # Dibuja la tabla en las coordenadas indicadas
                company_information.drawOn(cnv, 2.8 * cm, 1 * cm)

            # INFORMACIÓN DEL FIRMA - FIN -----------------------------------------------------------------------------

            # ANULADO -------------------------------------------------------------------------------------------------

            if preview_data['annuled']:
                msm = 'ANULADO'
                if default_decimals.currencyId == preview_data['currencyId']:
                    annuled(cnv, msm)
                else:
                    annuled_extra(cnv, msm)

            cnv.restoreState()

        def annuled(cvn, str):
            cvn.saveState()

            cvn.translate(8 * cm, 10 * cm)
            cvn.setFontSize(50, 70)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

        def annuled_extra(cvn, str):
            cvn.saveState()

            cvn.translate(17 * cm, 22 * cm)
            cvn.setFontSize(80, 30)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

            # ANULADO - FIN -------------------------------------------------------------------------------------------
            # cnv.restoreState()

        def header(cnv):
            cnv.saveState()
            # VARIABLES DEL HEADER ------------------------------------------------------------------------------------

            company_name = '{0} - {1}'.format(preview_data['company_name'], preview_data['branch_name'])

            # VARIABLES DEL HEADER - FIN ------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA COMPAÑIA ------------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:

                p_company_name = Paragraph('<b>{0}</b>'.format(
                    paragraph_over_flow_height(
                        text=company_name,
                        width=12.8,
                        no_par=2,
                        font_size=12,
                        leading=12,
                        left_indent=2.8,
                        right_indent=2.8)),
                    style_p_header)
                p_company_name.width = 12.8 * cm
                par_frag = p_company_name.breakLines(width=12.8 * cm)

                # Verifica el tamaña de el primer parrafo, Si tiene mas de 1 renglon rederiza la tabla mas abajo
                draw_company_on_y = 24.3
                if len(par_frag.lines) >= 2:
                    draw_company_on_y = 23.9
                nit1 = preview_data['nit'].split('-')
                data_header_company = [
                    [
                        p_company_name,
                    ],
                    [
                        Paragraph('<b>NIT: {0}-{1} {2}</b>'.format(
                            paragraph_over_flow(
                                # text='NIT: {0} {1}'.format(preview_data['nit'], preview_data['regimen']),
                                text='.'.join([str(nit1[0])[i:i + 3]
                                               for i in range(0, len(str(nit1[0])), 3)]),
                                width=12.8,
                                font_size=12,
                                leading=12), nit1[1], preview_data['regimen']),
                            style_p_header),
                    ],
                    [               #esta pendiente por valores
                        Paragraph('<b>Actividad Económica {0} Tarifa Renta {1}</b>'.format(
                            paragraph_over_flow(
                                text=preview_data['activity_code'],
                                width=12.8,
                                font_size=10,
                                leading=10,
                                left_indent=2.8,
                                right_indent=2.8), preview_data['porcent_renta']),
                            style_p_sub_header),
                    ],
                    [
                        Paragraph('<b>{0}</b>'.format(
                            paragraph_over_flow(
                                text='{0} - {1}'.format(preview_data['address'],
                                                        '{0} - {1}'.format(preview_data['city'],
                                                                           preview_data['department'])),
                                width=12.8,
                                font_size=12,
                                leading=12)),
                            style_p_header),
                    ],
                    [
                        Paragraph('<b>{0}</b>'.format(
                            paragraph_over_flow(
                                text='Teléfonos: {0} {1} {2} {3}'.format(preview_data['phone1'],
                                                                         preview_data['phone2'],
                                                                         preview_data['phone3'],
                                                                         '' if preview_data['fax'] is None or
                                                                               preview_data['fax'] == '' else
                                                                         'Celular: {0}'.format(preview_data['fax'])),
                                width=12.8,
                                font_size=12,
                                leading=12)),
                            style_p_header),
                    ],

                    [
                        Paragraph('<b>{0}</b>'.format(
                            paragraph_over_flow(
                                text=preview_data['retainer_taxpayer'],
                                width=19.6,
                                font_size=9.5,
                                leading=9.5)),
                            style_p_sub_header_ica),
                    ],
                    [
                        Paragraph('<b>{0}</b>'.format(
                            paragraph_over_flow(
                                text=preview_data['ica_activity'],
                                width=19.6,
                                font_size=9.5,
                                leading=9.5)),
                            style_p_sub_header_ica)
                    ]
                ]

                table_header_company = Table(
                    data_header_company,
                    [19.6 * cm],
                    style=table_style_header
                )

                table_header_company.wrap(19.6 * cm, 3.6 * cm)
                table_header_company.drawOn(cnv, 1 * cm, draw_company_on_y * cm)

            # INFORMACION DE LA TABLA COMPAÑIA - FIN ------------------------------------------------------------------

            # PAGINADO ------------------------------------------------------------------------------------------------

            # page_count == self._pageNumber
            if preview_data['currencyId'] != default_decimals.currencyId:
                paginate = Paragraph('Página {0} de {1}'.format(self._pageNumber, page_count),
                                     style_p_header_description_right)

                paginate.wrap(3 * cm, 0.4 * cm)
                paginate.drawOn(cnv, 17.5 * cm, 24.2 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA CLIENTE -----------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:

                table_header_provider = Table(
                    [
                        [
                            Paragraph('<b>Bill to / Facturado a</b>', style_p_header_provider),
                            ''
                        ],
                        [
                            Paragraph(paragraph_over_flow(text=preview_data['customer'].upper(),
                                                          width=9.4,
                                                          font_size=8,
                                                          leading=8),
                                      style_p_header_provider),
                            ''
                        ],
                        [
                            Paragraph(paragraph_over_flow(text=preview_data['customer_nit'],
                                                          width=9.4,
                                                          font_size=8,
                                                          leading=8),
                                      style_p_header_provider),
                            ''
                        ],
                        [
                            Paragraph(paragraph_over_flow(text=preview_data['customer_address'],
                                                          width=9.4,
                                                          font_size=8,
                                                          leading=8),
                                      style_p_header_provider),
                            ''
                        ],
                        [
                            Paragraph(paragraph_over_flow(text='{0}, {1}'.format(preview_data['customer_city'],
                                                                                 preview_data['customer_department']),
                                                          width=9.4,
                                                          font_size=8,
                                                          leading=8),
                                      style_p_header_provider),
                            ''
                        ],
                        [
                            Paragraph(paragraph_over_flow(text=preview_data['customer_country'],
                                                          width=9.4,
                                                          font_size=8,
                                                          leading=8),
                                      style_p_header_provider),
                            ''
                        ],
                        [
                            '',
                            ''
                        ],

                    ],
                    [9.7 * cm, 0.1 * cm],
                    0.4 * cm,
                    style=table_style_header_general2
                )
                table_header_provider.wrap(9.8 * cm, 2 * cm)
                table_header_provider.drawOn(cnv, 1 * cm, 21.07 * cm)

            # INFORMACION DE LA TABLA CLIENTE - FIN -----------------------------------------------------------------

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ -----------------------------------------------------------------

            # Validaciones para text de dias de plazo
            term_value = ''
            if preview_data['needTermDays'] == 1 and preview_data['termDays'] == 0:
                term_value = 'Contado'
            else:
                if preview_data['needTermDays'] == 1 and preview_data['termDays'] == 1:
                    term_value = "{0} a {1} Día".format(preview_data['forma_pago'], preview_data['termDays'])
                else:
                    if preview_data['needTermDays'] == 1 and preview_data['termDays'] > 1:
                        term_value = "{0} a {1} Días".format(preview_data['forma_pago'], preview_data['termDays'])
                    else:
                        term_value = '{0} Día(s)'.format(preview_data['termDays'])

            # Validaciones para cuando es moneda extranjera
            text_trm = '<b>TRM</b>' if default_decimals.currencyId != preview_data['currencyId'] else ''
            text_trm_value = '{:20,.{}f}'.format(
                _round(preview_data['exchangeRate'],
                       default_decimals.valueDecimals),
                default_decimals.valueDecimals) if default_decimals.currencyId != preview_data[
                'currencyId'] \
                else ''
            text_currency = '<b>Moneda</b>' if default_decimals.currencyId != preview_data[
                'currencyId'] else ''
            text_currency_value = preview_data['currency'] if default_decimals.currencyId != preview_data[
                'currencyId'] \
                else ''

            if preview_data['currencyId'] != default_decimals.currencyId:
                consecutive = int(preview_data['consecutive'])
                table_header_date_validity = Table(
                    [
                        [
                            Paragraph('<b>Invoice / Factura de Venta</b>', style_p_header_extra_validity),
                            Paragraph('N°{0}{1}'.format('' if preview_data['prefix_resolution'] == ''
                                                        else '{0}-'.format(
                                preview_data['prefix_resolution']),
                                                        consecutive),
                                      style_p_header_date_validity_right)


                        ],
                        [
                            Paragraph('<b>Invoice Date / Fecha de Factura</b>', style_p_header_extra_validity),
                            Paragraph(preview_data['document_date'], style_p_header_date_validity_right)

                        ],
                        [
                            Paragraph('<b>Terms / Plazo</b>', style_p_header_extra_validity),
                            Paragraph(term_value, style_p_header_date_validity_right)

                        ],
                        [
                            Paragraph('<b>Due / Fecha Vencimiento</b>', style_p_header_extra_validity),
                            Paragraph(preview_data['date_finish'], style_p_header_date_validity_right)
                        ],
                        [
                            Paragraph('<b>Po Number / N° Orden de Compra</b>', style_p_header_extra_validity),
                            Paragraph(preview_data['order_number'], style_p_header_date_validity_right)
                        ],
                        [
                            Paragraph('<b>Currency / Moneda</b>', style_p_header_extra_validity),
                            Paragraph(preview_data['currency'].title(), style_p_header_date_validity_right)
                        ],
                        [
                            Paragraph('<b>Exchangerate / Tasa de Cambio</b>', style_p_header_extra_validity),
                            Paragraph(text_trm_value, style_p_header_date_validity_right)
                        ]

                    ],
                    [4.5 * cm, 5.3 * cm],
                    0.4 * cm,
                    style=table_style_header_date_validity2
                )

                table_header_date_validity.wrap(9.8 * cm, 0.6 * cm)
                table_header_date_validity.drawOn(cnv, 10.8 * cm, 21.07 * cm)


            # INFORMACION DE LA TABLA FECHA Y VALIDEZ - FIN -----------------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:

                table_header_description = Table(
                    [
                        [
                            Paragraph('<b>PRODUCT CODE</b>', style_p_header_provider),
                            Paragraph('<b>ITEM N°/DESCRIPTION</b>', style_p_header_provider),
                            Paragraph('<b>UOM</b>', style_p_header_description_right),
                            Paragraph('<b>QTY ORDERED</b>', style_p_header_description_right),
                            Paragraph('<b>UNIT PRICE</b>', style_p_header_description_right),
                            Paragraph('<b>EXTENDED PRICE</b>', style_p_header_description_right),
                        ]

                    ],
                    [2.7 * cm, 6.03 * cm, 2.2 * cm, 2.8 * cm, 2.6 * cm, 3.266 * cm],
                    [0.4 * cm],
                    style=table_style_header_description
                )

                table_header_description.wrap(19.6 * cm, 0.4 * cm)
                table_header_description.drawOn(cnv, 1 * cm, 20.6 * cm)

                table_header_description = Table(
                    [
                        [
                            Paragraph('<b>COD PRODUCTO</b>', style_p_header_provider),
                            Paragraph('<b>N°ARTICULO/DESCRIPCIÓN</b>', style_p_header_provider),
                            Paragraph('<b>U DE M</b>', style_p_header_description_right),
                            Paragraph('<b>CANT ORDENADA</b>', style_p_header_description_right),
                            Paragraph('<b>VR UNITARIO</b>', style_p_header_description_right),
                            Paragraph('<b>VALOR</b>', style_p_header_description_right),
                        ]

                    ],
                    [2.7 * cm, 6.03 * cm, 2.2 * cm, 2.8 * cm, 2.6 * cm, 3.266 * cm],
                    [0.4 * cm],
                    style=table_style_header_description
                )

                table_header_description.wrap(19.6 * cm, 0.4 * cm)
                table_header_description.drawOn(cnv, 1 * cm, 20.3 * cm)

                cnv.line(1 * cm, 20.2 * cm, 20.6 * cm, 20.2 * cm)  # Línea

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            # INFORMACION DE LA TABLA LOGO ----------------------------------------------------------------------------

            if preview_data['currencyId'] != default_decimals.currencyId:
                image = None if preview_data['image'] is None \
                    else "{0},{1}".format("data:image/*;base64",
                                          ImagesConverter.img_convert_to_base64(preview_data['image'].image))

                if image is not None:
                    img = Image(image, width=2.3 * cm, height=2.3 * cm)

                    img.wrap(2.3 * cm, 2.3 * cm)
                    img.drawOn(cnv, 1 * cm, 25.2 * cm)

            # INFORMACION DE LA TABLA LOGO - FIN ----------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class SaleItemPreviewT:
    preview_data = None

    @staticmethod
    def make_preview_pdf(preview_data):
        SaleItemPreviewT.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.currencyId,
                                         DefaultValue.branchId,
                                         DefaultValue.printDescription,
                                         DefaultValue.descriptionFrom,
                                         DefaultValue.invoiceText) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 7
        style.leading = 9

        style_num.fontName = 'Arial'
        style_num.fontSize = 7
        style_num.alignment = TA_RIGHT
        # style_num.backColor = '#FFFF00'
        # style_num.borderColor = '#000000'
        # style_num.borderWidth = 1

        #cabecera de la tirilla

        style_p_company = ParagraphStyle('Normal')
        style_p_company.fontName = 'Arial'
        style_p_company.fontSize = 8
        style_p_company.leading = 10
        style_p_company.alignment = TA_CENTER

        style_p_company_info = ParagraphStyle('Normal')
        style_p_company_info.fontName = 'Arial'
        style_p_company_info.fontSize = 7.5
        style_p_company_info.leading = 10
        style_p_company_info.alignment = TA_CENTER

        style_p_header_t = ParagraphStyle('Normal')
        style_p_header_t.fontName = 'Arial'
        style_p_header_t.fontSize = 7
        style_p_header_t.leading = 10
        style_p_header_t.alignment = TA_CENTER

        style_p_header_tR = ParagraphStyle('Normal')
        style_p_header_tR.fontName = 'Arial'
        style_p_header_tR.fontSize = 7
        style_p_header_tR.leading = 10
        style_p_header_tR.alignment = TA_RIGHT

        style_p_header_tL = ParagraphStyle('Normal')
        style_p_header_tL.fontName = 'Arial'
        style_p_header_tL.fontSize = 7
        style_p_header_tL.leading = 10
        style_p_header_tL.alignment = TA_LEFT

        table_style_header_general2 = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (-1, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]
        )

        raya = '-' * 100

        table_header_tirilla = Table(
            [
                [
                    Paragraph(
                        paragraph_over_flow(text=preview_data['company_name'].upper(),
                                            width=7,
                                            font_size=6,
                                            leading=8),
                        style_p_company),
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['branch_name'],
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(text='NIT: {0}'.format(preview_data['nit']),
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['address'],
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(text='{0} - {1}'.format(preview_data['city'],
                                                                          preview_data['department']),
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(
                        text='Teléfonos: {0} {1} {2} {3}'.format(preview_data['phone1'],
                                                                 preview_data['phone2'],
                                                                 preview_data['phone3'],
                                                                 '' if preview_data['fax'] is None or
                                                                       preview_data['fax'] == '' else
                                                                 'Celular: {0}'.format(preview_data['fax'])),
                            width=8,
                            font_size=8,
                            leading=8),
                        style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['regimen'],
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['document_date'],
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text='FACTURA N° {0}{1}'.format(
                        '' if preview_data['prefix_resolution'] == ''
                        else '{0}-'.format(
                            preview_data['prefix_resolution']), preview_data['consecutive']),
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=raya,
                                                  width=7.5,
                                                  font_size=8,
                                                  leading=8),
                              style_p_company_info),
                    ''
                ]

            ],
            [8 * cm, 0.1 * cm],
            0.3 * cm,
            style=table_style_header_general2
        )

        # descripcion de los detalles ---------------------------------------------------------------------------------------

        table_style_header_description = TableStyle(
            [
                ('LEFTPADDING', (1, 0), (-1, 0), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )
        style_code = ParagraphStyle('Normal')
        style_code.fontName = 'Helvetica-Bold'
        style_code.fontSize = 7
        style_code.leading = 10
        style_code.alignment = TA_RIGHT

        style_code_tL = ParagraphStyle('Normal')
        style_code_tL.fontName = 'Helvetica-Bold'
        style_code_tL.fontSize = 7
        style_code_tL.leading = 10
        style_code_tL.alignment = TA_LEFT

        table_header_description = Table(
            [
                [
                    Paragraph('CÓDIGO', style_code_tL),
                    Paragraph('DESCRIPCIÓN', style_code_tL),
                    Paragraph('CANT', style_code),
                    Paragraph('VALOR', style_code),
                ]

            ],
            [1.4 * cm, 2 * cm, 1.6 * cm, 2 * cm],
            [0.2 * cm],
            style=table_style_header_description
        )
        #raya----------------------------------------------------------------------------------------------------------------
        table_header_raya = Table(
            [
                [
                    Paragraph(paragraph_over_flow(text=raya,
                                                  width=8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''
                ],
                [
                    '',
                    ''
                ]

            ],
            [8 * cm, 0.1 * cm],
            0.2 * cm,
            style=table_style_header_general2
        )

        #tabla totales -----------------------------------------------------------------------------------------------------
        table_style_footer_totaling = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        style_total = ParagraphStyle('Normal')
        style_total.fontName = 'Helvetica-Bold'
        style_total.fontSize = 7
        style_total.leading = 10
        style_total.alignment = TA_RIGHT

        style_p_total_tL = ParagraphStyle('Normal')
        style_p_total_tL.fontName = 'Helvetica-Bold'
        style_p_total_tL.fontSize = 7
        style_p_total_tL.leading = 10
        style_p_total_tL.alignment = TA_LEFT

        total_base_value = 0
        for dct_det in preview_data['document_details']:
            total_base_value += dct_det.baseValue

        sub_total = 0
        descuento = 0
        iva = 0
        rete_fuente = 0
        impo_consumo = 0
        neto_a_pagar = 0
        value_cree = 0
        sub_total = _round(preview_data['sub_total'], default_decimals.valueDecimals)
        descuento = _round(preview_data['discount'], default_decimals.valueDecimals)
        iva = _round(preview_data['iva'], default_decimals.valueDecimals)
        value_cree = _round(preview_data['valueCREE'], default_decimals.valueDecimals)
        impo_consumo = _round(preview_data['consumptionTaxValue'], default_decimals.valueDecimals)
        neto_a_pagar = _round(preview_data['total'], default_decimals.valueDecimals)
        rete_fuente = _round(preview_data['withholdingTaxValue'], default_decimals.valueDecimals)

        if dct_det.item.typeItem == 'A':
            tipo = 2
        else:
            tipo = 1

        data_footer_totaling = [
            [
                Paragraph('', style_p_header_tR),
                Paragraph('SUBTOTAL', style_p_header_tL),
                Paragraph('{:20,.{}f}'.format(_round(sub_total, default_decimals.valueDecimals),
                                               default_decimals.valueDecimals), style_total)
            ],
            [
                Paragraph('', style_p_header_tR),
                Paragraph('DESCUENTO', style_p_header_tL),
                Paragraph('{:20,.{}f}'.format(_round(descuento, default_decimals.valueDecimals),
                                               default_decimals.valueDecimals), style_p_header_tR)
            ],
            [
                Paragraph('', style_p_header_tR),
                Paragraph('' if tipo != 1 else 'RETEFUENTE', style_p_header_tL),
                Paragraph('' if tipo != 1 else'${:20,.{}f}'.format(_round(rete_fuente, default_decimals.valueDecimals),
                                                                   default_decimals.valueDecimals), style_p_header_tR)
            ],
            [
                Paragraph('', style_p_header_tR),
                Paragraph('IMPOCONSUMO', style_p_header_tL),
                Paragraph('{:20,.{}f}'.format(_round(impo_consumo, default_decimals.valueDecimals),
                                               default_decimals.valueDecimals), style_p_header_tR)
            ],
            [
                Paragraph('', style_p_header_tR),
                Paragraph('AUTORET RENTA', style_p_header_tL),
                Paragraph('{:20,.{}f}'.format(_round(value_cree, default_decimals.valueDecimals),
                                               default_decimals.valueDecimals), style_p_header_tR)
            ],
            [
                Paragraph('', style_p_header_tR),
                Paragraph('TOTAL', style_p_total_tL),
                Paragraph('{:20,.{}f}'.format(_round(neto_a_pagar, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_total)
            ]
        ]

        table_footer_totaling = Table(
            data_footer_totaling,  # Contenido de la tabla
            [1.4 * cm, 2.8 * cm, 2.8 * cm],  # Ancho de las columnas
            0.3 * cm,
            style=table_style_footer_totaling  # Estilos de la tabla
        )

        #Efectivo o cuotas---------------------------------------------------------------------------------------------------

        if preview_data['forma_pago'] == 'Cuotas':
            quota_number = preview_data['num_couta']
            valor_cuota = neto_a_pagar / int(quota_number)

            data_footer_cuota =[
                [
                    Paragraph('', style_p_header_tR),
                    Paragraph('TOTAL CUOTAS', style_p_header_tL),
                    Paragraph('{:20,.{}f}'.format(_round(neto_a_pagar, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style_p_header_tR)
                ],
                [
                    Paragraph('', style_p_header_tR),
                    Paragraph('N° CUOTAS', style_p_header_tL),
                    Paragraph('{0}'.format(quota_number), style_p_header_tR)
                ],
                [
                    Paragraph('', style_p_header_tR),
                    Paragraph('VALOR CUOTA', style_p_header_tL),
                    Paragraph('{:20,.{}f}'.format(_round(valor_cuota, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style_p_header_tR)
                ]
            ]

        elif preview_data['forma_pago'] == 'Contado':
            efectivo = 0
            cheque = 0
            transferencia = 0
            debito = 0
            credito = 0
            bono = 0

            for datos in preview_data['payment_receipt'].paymentDetails:

                if datos.paymentMethod.paymentType == 'EF':
                    efectivo += datos.value
                elif datos.paymentMethod.paymentType == 'CH':
                    cheque += datos.value
                elif datos.paymentMethod.paymentType == 'TR':
                    transferencia += datos.value
                elif datos.paymentMethod.paymentType == 'TD':
                    debito += datos.value
                elif datos.paymentMethod.paymentType == 'TC':
                    credito += datos.value
                elif datos.paymentMethod.paymentType == 'BN':
                    bono += datos.value

            data_footer_cuota = [

            ]

            if efectivo > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('EFECTIVO', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(efectivo, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )
            if bono > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('BONO', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(bono, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )

            if cheque > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('CHEQUE', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(cheque, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )

            if transferencia > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('TRANSFERENCIA', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(transferencia, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )

            if debito > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('DÉBITO', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(debito, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )

            if credito > 0:
                data_footer_cuota.append(
                    [
                        Paragraph('', style_p_header_tR),
                        Paragraph('CRÉDITO ', style_p_header_tL),
                        Paragraph('{:20,.{}F}'.format(_round(credito, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_header_tR)
                    ]
                )

        else:
            data_footer_cuota = [
                [
                    '',
                    '',
                    ''
                ]
            ]

        table_footer_cuotas = Table(
            data_footer_cuota,  # Contenido de la tabla
            [1.4 * cm, 2.8 * cm, 2.8 * cm],  # Ancho de las columnas
            0.3 * cm,
            style=table_style_footer_totaling  # Estilos de la tabla
        )

        # descripcion iva --------------------------------------------------------------------------------------------------

        data_footer_totaling = [
            [
                Paragraph('', style_p_header_tR),
                Paragraph('**DETALLE IVA**', style_p_header_t),
                Paragraph('', style_p_header_tR)
            ]
        ]
        table_header_iva = Table(
            data_footer_totaling,  # Contenido de la tabla
            [1.5 * cm, 4 * cm, 1.5 * cm],  # Ancho de las columnas
            0.3 * cm,
            style=table_style_footer_totaling  # Estilos de la tabla
        )

        #descripcion iva ---------------------------------------------------------------------------------------------------

        style_p_base = ParagraphStyle('Normal')
        style_p_base.fontName = 'Helvetica-Bold'
        style_p_base.fontSize = 7
        style_p_base.leading = 10
        style_p_base.alignment = TA_RIGHT

        style_p_base_tL = ParagraphStyle('Normal')
        style_p_base_tL.fontName = 'Helvetica-Bold'
        style_p_base_tL.fontSize = 7
        style_p_base_tL.leading = 10
        style_p_base_tL.alignment = TA_LEFT

        table_description_iva = Table(
            [
                [
                    Paragraph('', style_p_base_tL),
                    Paragraph('BASE', style_p_base),
                    Paragraph('%IVA', style_p_base),
                    Paragraph('Vr IVA', style_p_base),
                ]

            ],
            [1.4 * cm, 2 * cm, 1.6 * cm, 2 * cm],
            [0.2 * cm],
            style=table_style_header_description
        )

        #detalle iva -------------------------------------------------------------------------------------------------------
        iva_list = []
        ic_list = []
        base_value_arr = []
        iva_percent_arr = []
        ic_percent_arr = []
        tax_value_arr = []

        for dct_det in preview_data['document_details']:
            iva_list.append((dct_det.iva, dct_det.baseValue))
            ic_list.append((dct_det.consumptionTaxPercent, dct_det.baseValue))

        # iva_gruop = []

        # for i, j in groupby(iva_list):
        #     iva_gruop.append(j)

        iva_gruop = sorted(iva_list, key=lambda tup: tup[0])
        ic_gruop = sorted(ic_list, key=lambda tup: tup[0])
        iva_gruop = [list(j) for i, j in groupby(iva_gruop, lambda x: x[0])]
        ic_gruop = [list(j) for i, j in groupby(ic_gruop, lambda x: x[0])]
        # ic_gruop = [list(j) for i, j in groupby(ic_list)]

        iva_values = []
        ic_values = []

        for ic_l in ic_gruop:
            value = 0
            ic_percent = 0
            base_value = 0
            for ic in ic_l:
                value += (_round(ic[0], 2) / 100) * _round(ic[1], 2)
                ic_percent = _round(ic[0], 2)
                base_value += _round(ic[1], default_decimals.valueDecimals)
            ic_values.append({'tax_value': value,
                              'ic_percent': ic_percent,
                              'iva_percent': 0,
                              'base_value': base_value})

        for iva_l in iva_gruop:
            value = 0
            iva_percent = 0
            base_value = 0
            for iva in iva_l:
                value += (_round(iva[0], 2) / 100) * _round(iva[1], 2)
                iva_percent = _round(iva[0], 2)
                base_value += _round(iva[1], default_decimals.valueDecimals)
            iva_values.append({'tax_value': value,
                               'iva_percent': iva_percent,
                               'ic_percent': 0,
                               'base_value': base_value})

        ic_values = [ic for ic in ic_values if not ic['ic_percent'] == 0]

        tax_values = iva_values + ic_values

        for tax in tax_values:
            if len(base_value_arr) < 7:
                base_value_arr.append(
                    '{:20,.{}f}'.format(_round(tax['base_value'], default_decimals.valueDecimals),
                                        default_decimals.valueDecimals))
            if len(iva_percent_arr) < 7:
                iva_percent_arr.append('{:20,.{}f}'.format(_round(tax['iva_percent'], 2), 2))
            if len(ic_percent_arr) < 7:
                ic_percent_arr.append('{:20,.{}f}'.format(_round(tax['ic_percent'], 2), 2))
            if len(tax_value_arr) < 7:
                tax_value_arr.append(
                    '{:20,.{}f}'.format(_round(tax['tax_value'], default_decimals.valueDecimals),
                                        default_decimals.valueDecimals))

            base_value_par = ''
            iva_percent_par = ''
            ic_percent_par = ''
            tax_value_par = ''
            # if page_count == self._pageNumber:
        base_value_par = '<br/>'.join(base_value_arr)
        iva_percent_par = '<br/>'.join(iva_percent_arr)

        data_iva = []

        data_iva.append(
            [
                Paragraph('A', style_p_header_tL),
                Paragraph(base_value_par, style_p_header_tR),
                Paragraph(iva_percent_par, style_p_header_tR),
                Paragraph('{:20,.{}f}'.format(_round(preview_data['iva'], 2), 2), style=style_num),
            ]
        )

        #datos cliente ------------------------------------------------------------------------------------------------------

        table_style_footer_client = TableStyle(
            [
                # ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                # ('LEFTPADDING', (1, 0), (1, -1), 0),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        term_value = ''
        if preview_data['needTermDays'] == 1 and preview_data['termDays'] == 0:
            term_value = 'Contado'
        else:
            if preview_data['needTermDays'] == 1 and preview_data['termDays'] == 1:
                term_value = "{0} a {1} Día".format(preview_data['forma_pago'], preview_data['termDays'])
            else:
                if preview_data['needTermDays'] == 1 and preview_data['termDays'] > 1:
                    term_value = "{0} a {1} Días".format(preview_data['forma_pago'], preview_data['termDays'])
                else:
                    term_value = preview_data['forma_pago']

        if preview_data['business_agent'] == 'None':
            vendedor_name = preview_data['employee'].split('-')
        else:
            vendedor_name = preview_data['business_agent'].split('-')

        table_footer_client = Table(
            [
                [
                    Paragraph('CLIENTE:', style_p_header_tL),
                    Paragraph(paragraph_over_flow(text=preview_data['customer'].upper(),
                                                  width=4,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_tL),
                ],
                [
                    Paragraph('NIT o CC:', style_p_header_tL),
                    Paragraph(preview_data['customer_nit'], style_p_header_tL)
                ],
                [
                    Paragraph('FORMA DE PAGO:', style_p_header_tL),
                    Paragraph(term_value.upper(), style_p_header_tL)
                ],
                [
                    Paragraph('VENDEDOR:', style_p_header_tL),
                    Paragraph(paragraph_over_flow(text=vendedor_name[0].upper(),
                                                  width=5,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_tL),
                ],
                [
                    Paragraph('TOTAL ITEMS:', style_p_header_tL),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.quantity, default_decimals.quantityDecimals),
                                                  default_decimals.quantityDecimals), style=style_p_header_tL),
                ]
            ],

            [2.5 * cm, 4.5 * cm],  # Ancho de las columnas
            0.3 * cm,
            style=table_style_footer_client  # Estilos de la tabla
        )

        #DIAN------ -------------------------------------------------------------------------------------------------------

        table_style_footer_dian = TableStyle(
            [
                # ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                # ('LEFTPADDING', (1, 0), (1, -1), 0),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )
        style_p_dian = ParagraphStyle('Normal')
        style_p_dian.fontName = 'Arial'
        style_p_dian.fontSize = 7
        style_p_dian.leading = 10
        style_p_dian.alignment = TA_CENTER

        information_dian = ''
        #autorizada
        if preview_data['type_resolution'] == 0 and preview_data['months'] == 0:

            information_dian = 'Numeración Autorizada por la DIAN según la Resolución N° {0} de {1} ' \
                               'desde {2} {3} hasta {4} {5}'.format(
                preview_data['resolution'], preview_data['resolution_date'],
                preview_data['prefix_resolution'], preview_data['consecutive_from'],
                preview_data['prefix_resolution'], preview_data['consecutive_to'])

        elif preview_data['type_resolution'] == 0 and preview_data['months'] > 0:

            consecutive_end = int(preview_data['consecutive_to'])
            conseutive_ini = int(preview_data['consecutive_from'])

            if preview_data['months'] > 1:
                mes = 'meses'
            else:
                mes = 'mes'

            information_dian = 'Autorización Numeración de Facturación ' \
                               'N° {0} de {1} desde {2} {3} hasta {4} {5} ' \
                               'con vigencia de {6} {7}'.format(
                                                            preview_data['resolution'],
                                                            preview_data['resolution_date'],
                                                            preview_data['prefix_resolution'],
                                                            conseutive_ini,
                                                            preview_data['prefix_resolution'],
                                                            consecutive_end,
                                                            preview_data['months'],
                                                            mes)

        #habilitada
        elif preview_data['type_resolution'] == 1 and preview_data['months'] == 0:

            information_dian = 'Numeración Habilitada por la DIAN según la Resolución N° {0} de {1} ' \
                               'desde {2} {3} hasta {4} {5}'.format(
                preview_data['resolution'], preview_data['resolution_date'],
                preview_data['prefix_resolution'], preview_data['consecutive_from'],
                preview_data['prefix_resolution'], preview_data['consecutive_to'])

        elif preview_data['type_resolution'] == 1 and preview_data['months'] > 0:
            consecutive_end = int(preview_data['consecutive_to'])
            conseutive_ini = int(preview_data['consecutive_from'])

            if preview_data['months'] > 1:
                mes = 'meses'
            else:
                mes = 'mes'

            information_dian = 'Habilitación Numeración de Facturación ' \
                               'N° {0} de {1} desde {2} {3} hasta {4} {5} ' \
                                       'con vigencia de {6} {7}'.format(
                                                                    preview_data['resolution'],
                                                                    preview_data['resolution_date'],
                                                                    preview_data['prefix_resolution'],
                                                                    conseutive_ini,
                                                                    preview_data['prefix_resolution'],
                                                                    consecutive_end,
                                                                    preview_data['months'],
                                                                    mes)

        table_footer_dian = Table(
            [
                [
                  ''
                ],
                [
                    Paragraph(information_dian, style_p_dian)
                ]
            ],
            [7 * cm],  # Ancho de las columnas
            [0.1 * cm, 1.1 * cm],
            style=table_style_footer_dian  # Estilos de la tabla
        )

        # gracias compra ---------------------------------------------------------------------------------------------------
        table_style_compra = TableStyle(
            [
                # ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                # ('LEFTPADDING', (1, 0), (1, -1), 0),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )
        style_p_compra = ParagraphStyle('Normal')
        style_p_compra.fontName = 'Arial'
        style_p_compra.fontSize = 7
        style_p_compra.leading = 10
        style_p_compra.alignment = TA_CENTER

        table_footer_compra = Table(
            [
                [
                    '',
                    '',
                    ''
                ],
                [
                    Paragraph('', style_p_header_tR),
                    Paragraph('GRACIAS POR SU COMPRA', style_p_compra),
                    Paragraph('', style_p_header_tR)
                ]
            ],
            [1.5 * cm, 4 * cm, 1.5 * cm],  # Ancho de las columnas
            [0.3 * cm, 0.6 * cm],
            style=table_style_compra  # Estilos de la tabla
        )

        # factura pymes+ ----------------------------------------------------------------------------------------------------

        table_style_pymes = TableStyle(
            [
                # ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                # ('LEFTPADDING', (1, 0), (1, -1), 0),
                # ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.183 * cm),
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 10), (-2, -3)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )
        style_p_pymes = ParagraphStyle('Normal')
        style_p_pymes.fontName = 'Arial'
        style_p_pymes.fontSize = 7
        style_p_pymes.leading = 10
        style_p_pymes.alignment = TA_CENTER

        information_pymes = 'Factura impresa por software Pymes+ <br/>Desarrollado por ' \
                            'SoftPymes SAS <br/>NIT 830.506.365-7 <br/>www.softpymes.com.co ' \
                                        '<br/>Teléfono: (572) 3828300 Cali.'
        table_footer_pymes = Table([
            [
                Paragraph(information_pymes, style_p_pymes)
            ]
        ],
            [7 * cm],  # Ancho de las columnas
            1.1 * cm,
            style=table_style_pymes  # Estilos de la tabla
        )

        # Inserta los datos de Document detail en el pdf --------------------------------------------------------------------
        style_numT = ParagraphStyle('Normal')
        style_numT.fontName = 'Arial'
        style_numT.fontSize = 7
        style_numT.alignment = TA_RIGHT

        style_numTL = ParagraphStyle('Normal')
        style_numTL.fontName = 'Arial'
        style_numTL.fontSize = 7
        style_numTL.alignment = TA_LEFT

        data = []
        for dct_det in preview_data['document_details']:
            det_color = ''
            det_size = ''
            det_comment = ''
            det_lot = ''
            det_siz_col_brake = ''
            det_serials = ''
            invima = ''

            if dct_det.sizeId is not None:
                det_size = '<font size=6>TALLA: {0} </font>'.format(dct_det.size.code)
            if dct_det.colorId is not None:
                det_color = '<font size=6>COLOR: {0} </font>'.format(dct_det.color.name)

            if default_decimals.printDescription == 1 and default_decimals.descriptionFrom == 1:
                if dct_det.item.description is None:
                    det_comment = ''
                else:
                    det_comment = '<br/><font size=6>{0}</font>'.format(dct_det.item.description)
            elif default_decimals.printDescription == 1 and default_decimals.descriptionFrom == 2:
                if dct_det.comments is None:
                    det_comment = ''
                else:
                    det_comment = '<br/><font size=6>{0}</font>'.format(dct_det.comments)

            if dct_det.lot is not None:
                det_lot = '<br/><font size=6>LOTE: {0} VENCE: {1}</font>'.format(dct_det.lot,
                                                                                 dct_det.dueDate.strftime(
                                                                                     '%d %b. %Y')
                                                                                 .upper())
            if dct_det.item.serial:
                serials_str = ", ".join(s.serial.serialNumber for s in dct_det.serialDetail.all())
                det_serials = '<br/><font size=6>SERIAL Nº: {0}</font>'.format(serials_str)

            if dct_det.sizeId is not None or dct_det.colorId is not None:
                det_siz_col_brake = '<br/>'

            if preview_data['invima'] == '1':
                invima = '<br/><font size=6>{0} {1}</font>'.format(
                    '' if dct_det.item.invimaRegister is None else dct_det.item.invimaRegister,
                    '' if dct_det.item.invimaDueDate is None else dct_det.item.invimaDueDate.strftime("%d/%m/%Y"))

            if preview_data['currencyId'] == default_decimals.currencyId:
                # for i in range(15):
                data.append(
                    [
                        Paragraph(dct_det.item.code, style_numTL),
                        Paragraph('{0}'.format(dct_det.item.name), style_numTL),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.quantity, default_decimals.quantityDecimals),
                                                      default_decimals.quantityDecimals), style=style_numT),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.value, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style=style_numT)

                    ]
                )
            else:
                style_num_extra = ParagraphStyle('Normal')
                style_num_extra.fontName = 'Arial'
                style_num_extra.fontSize = 8
                style_num_extra.leading = 8

                style_num_extra_right = ParagraphStyle('Normal')
                style_num_extra_right.fontName = 'Arial'
                style_num_extra_right.fontSize = 8
                style_num_extra_right.leading = 8
                style_num_extra_right.alignment = TA_RIGHT

                # for i in range(70):
                data.append(
                    [
                        Paragraph(dct_det.item.code, style_num_extra),
                        Paragraph('{0}{1}{2}{3}{4}{5}{6}{7}'.format(dct_det.item.name,
                                                                    det_siz_col_brake,
                                                                    det_size,
                                                                    det_color,
                                                                    det_lot,
                                                                    det_serials,
                                                                    det_comment,
                                                                    invima), style_num_extra),
                        Paragraph(dct_det.item.measurementUnit.code, style_num_extra),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.quantity, default_decimals.quantityDecimals),
                                                      default_decimals.quantityDecimals), style=style_num_extra_right),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.unitValue, 2), 2), style=style_num_extra_right),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.value, default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style=style_num_extra_right)
                    ]
                )

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        if preview_data['currencyId'] == default_decimals.currencyId:

            doc = BaseDocTemplate(outfilepath, pagesize=(8.5 * cm, 50 * cm))

        else:

            doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        if preview_data['currencyId'] == default_decimals.currencyId:
            doc.addPageTemplates(
                [
                    PageTemplate(
                        frames=[
                            Frame(
                                x1=0.5 * cm,
                                y1=4.5 * cm,
                                width=7.5 * cm,
                                height=45 * cm,
                                leftPadding=0,
                                bottomPadding=0,
                                rightPadding=0,
                                topPadding=0,
                                id=None,
                                showBoundary=False
                            ),
                        ],
                    ),
                ]
            )
        else:
            doc.addPageTemplates(
                [
                    PageTemplate(
                        frames=[
                            Frame(
                                x1=1 * cm,
                                y1=7.9 * cm,
                                width=19.6 * cm,
                                height=12.2 * cm,
                                leftPadding=0,
                                bottomPadding=0,
                                rightPadding=0,
                                topPadding=0,
                                id=None,
                                showBoundary=False
                            ),
                        ],
                    ),
                ]
            )

        if preview_data['currencyId'] == default_decimals.currencyId:
            doc.build(
                [table_header_tirilla,
                 table_header_description,
                 table_header_raya,
                 Table(
                    data,
                     [1.5 * cm, 2.5 * cm, 1 * cm, 2 * cm],
                    style=table_style
                ), table_header_raya,
                 table_footer_totaling,
                 table_header_raya,
                 table_footer_cuotas,
                 table_header_raya,
                 table_header_iva,
                 table_header_raya,
                 table_description_iva,
                 table_header_raya,
                 Table(
                     data_iva,
                     [1 * cm, 2.4 * cm, 1.6 * cm, 2 * cm],
                     style=table_style
                 ), table_footer_client,
                 table_footer_dian,
                 table_footer_compra,
                 table_footer_pymes],
                canvasmaker=NumberedCanvas
            )
        else:
            doc.build(
                [Table(
                    data,
                    [2.8 * cm, 7.6 * cm, 1.6 * cm, 1.7 * cm, 2.6 * cm, 3.3 * cm],
                    style=table_style
                )],
                canvasmaker=NumberedCanvas
            )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
