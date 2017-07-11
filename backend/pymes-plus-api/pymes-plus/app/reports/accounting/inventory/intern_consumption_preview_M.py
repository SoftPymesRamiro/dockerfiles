__author__ = "SoftPymes"
__credits__ = ["Chelo"]

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm,mm,inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color
from reportlab.lib import colors
import os
from .... import session
from itertools import groupby, product
import uuid
from ....models import DefaultValue
from ....utils.math_ext import _round
from ....utils.image_converter import ImagesConverter
from ....utils.converters import total_to_letter
from ...libs.functions import paragraph_over_flow, paragraph_over_flow_height
import time

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
        preview_data = InternConsumptionPreviewM.preview_data

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

        style_p_footerr = ParagraphStyle('Normal')
        style_p_footerr.fontName = 'Arial'
        style_p_footerr.fontSize = 8
        style_p_footerr.leading = 8
        style_p_footerr.alignment = TA_CENTER

        style_p_footer_centred = ParagraphStyle('Normal')
        style_p_footer_centred.fontName = 'Arial'
        style_p_footer_centred.fontSize = 8
        style_p_footer_centred.leading = 8
        style_p_footer_centred.alignment = TA_CENTER

        style_p_footer_right = ParagraphStyle('Normal')
        style_p_footer_right.fontName = 'Arial'
        style_p_footer_right.fontSize = 8
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
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_footer_taxes = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, 0), 1),
                ('LEFTPADDING', (0, 1), (-1, 1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, 0), 0),
                ('RIGHTPADDING', (0, 1), (-1, 1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_footer_observations = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, 0), 0.15 * cm),
                ('BOX', (0, 0), (0, 0), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        table_style_footer_totaling = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, -1), 0.1 * cm),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('BOTTOMPADDING', (0, 0), (-1, -1), 0.143 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('SPAN', (0, 4), (-1, -2)),
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
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
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
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        table_style_header_date_validity = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                # ('LEFTPADDING', (1, 0), (-1, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.01 * cm),
                # ('RIGHTPADDING', (0, 0), (-2, 0), 0),
                # ('TOPPADDING', (0, 0), (-1, 0), 0.24 * cm),
                # ('BOTTOMPADDING', (0, 0), (-1, 0), 0.1 * cm),
                # ('BOTTOMPADDING', (0, -1), (-1, -1), 0.31 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('VALIGN', (0, 0), (-3, -1), 'TOP'),
                # ('VALIGN', (-2, 0), (-1, -1), 'MIDDLE'),
                # ('SPAN', (1, 3), (-1, -2)),
                # ('BACKGROUND', (1, 2), (2, 1), colors.orange),
                ('SPAN', (1, 2), (2, 2)),  # bodega
                ('SPAN', (1, 3), (2, 3)),  # C.Costo
                ('SPAN', (1, 4), (2, 4)),  # division
                ('SPAN', (1, 5), (2, 5)),  # seccion
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
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
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
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
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

        style_p_header_description_left = ParagraphStyle('Normal')
        style_p_header_description_left.fontName = 'Arial'
        style_p_header_description_left.fontSize = 8
        style_p_header_description_left.leading = 8
        style_p_header_description_left.alignment = TA_LEFT

        style_p_header_description_right = ParagraphStyle('Normal')
        style_p_header_description_right.fontName = 'Arial'
        style_p_header_description_right.fontSize = 8
        style_p_header_description_right.leading = 8
        style_p_header_description_right.alignment = TA_RIGHT

        style_p_header_date_validity = ParagraphStyle('Normal')
        style_p_header_date_validity.fontName = 'Arial'
        style_p_header_date_validity.fontSize = 8
        style_p_header_date_validity.leading = 8

        style_p_annuled = ParagraphStyle('Normal')
        style_p_annuled.fontName = 'Arial'
        style_p_annuled.fontSize = 50
        style_p_annuled.leading = 50
        style_p_annuled.textColor = Color(255, 0, 0, alpha=0.3)

        def footer(cnv, last_value= 7):
            """
            draw the page footer
            :param cnv:
            :return:
            """
            cnv.saveState()

            # INFORMACIÓN DE LA TABLA DE TOTAL ------------------------------------------------------------------------

            # total_base_value = 99
            # for dct_det in preview_data['document_details']:
            #     total_base_value += dct_det.baseValue

            sub_total = 0
            # descuento = 0
            # otro_descuento = 0
            # base_gravable = 0
            iva = 0
            iva_base = 0
            # impo_consumo = 0
            # rete_fuente = 0
            neto_a_pagar = preview_data['total']
            # interest = 0
            # value_cree = 0
            # rete_ica_value = 0
            # rete_iva_value = 0
            # retention_value = 0
            # over_cost = 0
            # disccount2 = ''
            # percentage_cree = ''
            # rete_ica_percent = ''
            # rete_iva_percent = ''
            # rete_iva_percent = ''

            if page_count == self._pageNumber:
                sub_total = _round(preview_data['sub_total'], default_decimals.valueDecimals)
                # descuento = _round(preview_data['discount'], default_decimals.valueDecimals)
                # otro_descuento = _round(preview_data['discount2'], default_decimals.valueDecimals)
                # base_gravable = _round(total_base_value, default_decimals.valueDecimals)
                iva = _round(preview_data['iva'], default_decimals.valueDecimals)
                iva_base = _round(preview_data['iva_base'], default_decimals.valueDecimals)
                # impo_consumo = _round(preview_data['consumptionTaxValue'], default_decimals.valueDecimals)
                # rete_fuente = _round(preview_data['withholdingTaxValue'], default_decimals.valueDecimals)
                neto_a_pagar = _round(preview_data['total'], default_decimals.valueDecimals)
                # interest = _round(preview_data['interest'], default_decimals.valueDecimals)
                # value_cree = _round(preview_data['valueCREE'], default_decimals.valueDecimals)
                # rete_ica_value = _round(preview_data['reteICAValue'], default_decimals.valueDecimals)
                # rete_iva_value = _round(preview_data['reteIVAValue'], default_decimals.valueDecimals)
                # retention_value = _round(preview_data['retentionValue'], default_decimals.valueDecimals)
                # over_cost = _round(preview_data['overCost'], default_decimals.valueDecimals)
                # # disccount2 = _round(preview_data['disccount2P'], 2)
                # percentage_cree = _round(preview_data['percentageCREE'], 2)
                # rete_ica_percent = _round(preview_data['reteICAPercent'], 2)
                # rete_iva_percent = _round(preview_data['reteIVAPercent'], 2)
            # prueba = 10000000000 #valor de prueba
            data_footer_totaling = [

                [
                    Paragraph('<b>SubTotal</b>', style_p_footer),
                    Paragraph('', style_p_footer_right),
                    Paragraph('${:20,.{}f}'.format(_round(sub_total, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style_p_footer_right)
                ],
                [
                    Paragraph('<b>+Base IVA</b>', style_p_footer),
                    Paragraph('', style_p_footer_right),
                    Paragraph('${:20,.{}f}'.format(_round(iva_base, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style_p_footer_right)
                ],
                [
                    Paragraph('<b>+IVA</b>', style_p_footer),
                    Paragraph('', style_p_footer_right),
                    Paragraph('${:20,.{}f}'.format(_round(iva, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_footer_right)
                ],
                [
                    Paragraph('<b>Valor Total</b>', style_p_footer),
                    Paragraph('', style_p_footer_right),
                    Paragraph('${:20,.{}f}'.format(_round(neto_a_pagar, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style_p_footer_right)

                ]
            ]

            table_footer_totaling = Table(
                data_footer_totaling,  # Contenido de la tabla
                [3.4 * cm, 0.4 * cm, 3.1 * cm],  # Ancho de las columnas
                0.5 * cm,
                style=table_style_footer_totaling  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_totaling.wrap(0.89 * cm, 0.2 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            # table_footer_totaling.drawOn(cnv, 13.7 * cm, (last_value+1.57) * cm) # totales del contrato 1

            table_footer_totaling.drawOn(cnv, 13.7 * cm, 15 * cm)  # totales del contrato 1
            cnv.line(17 * cm, 15.38 * cm, 20.6 * cm, 15.38 * cm)  # Línea de total
            # INFORMACIÓN DE LA TABLA DE TOTAL - FIN ------------------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES ----------------------------------------------------------------

            style_p_observa = ParagraphStyle('Normal')
            style_p_observa.fontName = 'Arial'
            style_p_observa.fontSize = 8
            style_p_observa.leading = 8
            style_p_observa.alignment = TA_JUSTIFY

            observaciones = '<para><b>Observaciones:</b> {0} </para>'.format(preview_data['comments'].capitalize())
            par_observations = paragraph_over_flow_height(text=observaciones,
                                                          width=13,
                                                          no_par=5,
                                                          font_size=8,
                                                          leading=8)

            data_footer_observations = [
                [
                    Paragraph(par_observations, style_p_observa),
                ]
            ]

            table_footer_observations = Table(
                data_footer_observations,
                [12.7 * cm, ],
                [2 * cm, ],
                style=table_style_footer_observations

            )

            # Denota el contenor de la tabla
            table_footer_observations.wrap(13.7 * cm, 1.9 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_observations.drawOn(cnv, 1 * cm, 15 * cm)  # cobservaciones contrato 4.1

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES - FIN ----------------------------------------------------------

            # ANULADO -------------------------------------------------------------------------------------------------
            if preview_data['annuled']:
                msm = 'ANULADO'
                annuled(cnv, msm)

            cnv.restoreState()

        def annuled(cvn, str):
            cvn.saveState()

            cvn.translate(17 * cm, 23 * cm)
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

            data_header_company = [
                [
                    p_company_name,
                ],
                [
                    Paragraph('<b>{0}</b>'.format(
                        paragraph_over_flow(
                            text='CONSUMO INTERNO DE ARTÍCULOS DE INVENTARIO',
                            width=12.8,
                            font_size=12,
                            leading=12)),
                        style_p_header),

                   # '.'.join([str(66665583202)[::-1][i:i + 3] for i in range(0, \  len(str(66665583202)), 3)])
                ],
                [
                    # Paragraph('<b>{0}</b>'.format(
                    #     paragraph_over_flow(
                    #         text='{0} - {1}'.format(preview_data['address'],
                    #                                 '{0} - {1}'.format(preview_data['city'],
                    #                                                    preview_data['department'])),
                    #         width=12.8,
                    #         font_size=12,
                    #         leading=12)),
                    #     style_p_header),
                ],
                [
                    # Paragraph('<b>{0}</b>'.format(
                    #     paragraph_over_flow(
                    #         text='Teléfonos: {0} {1} {2} Fax:{3}'.format(preview_data['phone1'],
                    #                                                      preview_data['phone2'],
                    #                                                      preview_data['phone3'],
                    #                                                      preview_data['fax']),
                    #         width=12.8,
                    #         font_size=12,
                    #         leading=12)),
                    #     style_p_header),
                ],
                # [
                #     Paragraph('<b>{0}</b>'.format(
                #         paragraph_over_flow(
                #             text=preview_data['web'],
                #             width=12.8,
                #             font_size=10,
                #             leading=10,
                #             left_indent=2.8,
                #             right_indent=2.8)),
                #         style_p_sub_header),
                # ],
                [
                    # Paragraph('<b>{0}</b>'.format(
                    #     paragraph_over_flow(
                    #         text=preview_data['retainer_taxpayer'],
                    #         width=19.6,
                    #         font_size=9.5,
                    #         leading=9.5)),
                    #     style_p_sub_header_ica),
                ],
                [
                    # Paragraph('<b>{0}</b>'.format(
                    #     paragraph_over_flow(
                    #         text=preview_data['document_date'],
                    #         width=19.6,
                    #         font_size=9.5,
                    #         leading=9.5)),
                    #     style_p_sub_header_ica)
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
            fecha = time.strftime("%d/%m/%y")

            paginate1 = Paragraph('<b>Fecha:</b> '+fecha, style_p_header_description_left)

            paginate1.wrap(3 * cm, 0.4 * cm)
            paginate1.drawOn(cnv, 1 * cm, 24.8 * cm)
            # page_count == self._pageNumber
            paginate = Paragraph('Página {0} de {1}'.format(self._pageNumber, page_count),
                                 style_p_header_description_right)

            paginate.wrap(3 * cm, 0.4 * cm)
            paginate.drawOn(cnv, 17.5 * cm, 24.8 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ -----------------------------------------------------------------

            table_header_date_validity = Table(
                [

                    [

                        Paragraph('<b>Consumo N° </b>', style_p_header_date_validity),
                        Paragraph(preview_data['consecutive'], style_p_header_date_validity),
                        Paragraph('<b>Fecha </b> '+preview_data['document_date'], style_p_header_date_validity),

                    ],
                    [
                        '',
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Bodega</b>', style_p_header_date_validity),
                        Paragraph(preview_data['bodega'], style_p_header_date_validity),
                        ''
                    ],
                    [
                        Paragraph('<b>C.Costo</b>', style_p_header_date_validity),
                        Paragraph(preview_data['costCenter'], style_p_header_date_validity),
                        ''

                    ],
                    [
                        Paragraph('<b>División</b>', style_p_header_date_validity),
                        Paragraph(preview_data['division'], style_p_header_date_validity),
                        ''
                    ],
                    [
                        Paragraph('<b>Sección</b>', style_p_header_date_validity),
                        Paragraph(preview_data['section'], style_p_header_date_validity),
                        ''
                    ]

                ],

                [2.2 * cm, 3.4 * cm, 14 * cm],
                0.4 * cm,
                style=table_style_header_date_validity
            )
            table_header_date_validity.wrap(19.6 * cm, 0.6 * cm)
            table_header_date_validity.drawOn(cnv, 1 * cm, 22.2 * cm)

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ - FIN -----------------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>CÓDIGO</b>', style_p_header_provider),
                        Paragraph('<b>DESCRIPCIÓN</b>', style_p_header_provider),
                        Paragraph('<b>UND</b>', style_p_header_provider),
                        Paragraph('<b>COSTO UNIT</b>', style_p_header_description_right),
                        Paragraph('<b>CANTIDAD</b>', style_p_header_description_right),
                        Paragraph('<b>%IVA</b>', style_p_header_description_right),
                        Paragraph('<b>VALOR</b>', style_p_header_description_right),
                    ]
                ],
                [1.8 * cm, 8 * cm, 1.4 * cm, 2.1 * cm, 2.6 * cm, 1 * cm, 2.7 * cm],
                [0.4 * cm],
                style=table_style_header_description
            )

            table_header_description.wrap(19.6 * cm, 0.4 * cm)
            table_header_description.drawOn(cnv, 1 * cm, 21.8 * cm)
            #
            cnv.line(1 * cm, 21.8 * cm, 20.6 * cm, 21.8 * cm)  # Línea de firma proveedor

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            # INFORMACION DE LA TABLA LOGO ----------------------------------------------------------------------------
            image = None if preview_data['image'] is None \
                else "{0},{1}".format("data:image/*;base64",
                                      ImagesConverter.img_convert_to_base64(preview_data['image'].image))

            if image is not None:
                img = Image(image, width=2.1 * cm, height=2.1 * cm)

                img.wrap(2.3 * cm, 2.3 * cm)
                img.drawOn(cnv, 1 * cm, 25.3 * cm)

            # INFORMACION DE LA TABLA LOGO - FIN ----------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class InternConsumptionPreviewM:
    preview_data = None

    @staticmethod
    def make_preview_pdf(preview_data):
        InternConsumptionPreviewM.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')

        #estilo nuevo codigo activo
        estilo = ParagraphStyle('Normal')
        estilo.fontName = 'Arial'
        estilo.fontSize = 8
        estilo.leading = 9
        estilo.alignment = TA_LEFT

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 9

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        style_num.alignment = TA_RIGHT
        # style_num.backColor = '#FFFF00'
        # style_num.borderColor = '#000000'
        # style_num.borderWidth = 1

        # Inserta los datos de Document detail en el pdf
        data = []

        for dct_det in preview_data['document_details']:
            # for x in range(12):
            data.append(
                [
                    Paragraph(dct_det.item.code, style),
                    Paragraph(dct_det.item.name, style),
                    Paragraph(dct_det.item.measurementUnit.code, style),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.unitValue, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.quantity, default_decimals.quantityDecimals),
                                                  default_decimals.quantityDecimals), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.iva, 2), 2), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.value, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style=style_num)
                ]
            )

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        doc.addPageTemplates(
            [

                PageTemplate(
                    frames=[
                        Frame(
                            x1=1 * cm,
                            y1=16.7 * cm,
                            width=19.6 * cm,
                            height=5 * cm,
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

        doc.build(
            [Table(
                data,
                [1.9 * cm, 8 * cm, 1.3 * cm, 2.1 * cm, 2.6 * cm, 1 * cm, 2.7 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )



        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
