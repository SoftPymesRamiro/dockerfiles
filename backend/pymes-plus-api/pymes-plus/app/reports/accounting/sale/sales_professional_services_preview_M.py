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
        preview_data = SalesProfessionalServicesPreviewM.preview_data

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
                ('SPAN', (1, 0), (-1, 0)), #cliente
                ('SPAN', (1, 1), (3, 1)),  # direccion
                ('SPAN', (1, 2), (-1, -5)),  # ciudad
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (1, 5), (-1, -2)),  # vendedor
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
                ('SPAN', (1, 2), (-1, -2)), #span para plazo
                ('SPAN', (2, 3), (-1, -1)),#span para tasa de cambio
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

        # estilo parrafo subtotal
        style_p_subtotal_right = ParagraphStyle('Normal')
        style_p_subtotal_right.fontName = 'Arial'
        style_p_subtotal_right.fontSize = 6.8
        style_p_subtotal_right.leading = 7
        style_p_subtotal_right.alignment = TA_RIGHT

        style_p_subtotal = ParagraphStyle('Normal')
        style_p_subtotal.fontName = 'Arial'
        style_p_subtotal.fontSize = 6.8
        style_p_subtotal.leading = 7

        # estilo valor base
        style_p_vrBase = ParagraphStyle('Normal')
        style_p_vrBase.fontName = 'Arial'
        style_p_vrBase.fontSize = 7
        style_p_vrBase.leading = 7

        style_p_vrBase_right = ParagraphStyle('Normal')
        style_p_vrBase_right.fontName = 'Arial'
        style_p_vrBase_right.fontSize = 7
        style_p_vrBase_right.leading = 7
        style_p_vrBase_right.alignment = TA_RIGHT

        # estilo son
        style_p_son = ParagraphStyle('Normal')
        style_p_son.fontName = 'Arial'
        style_p_son.fontSize = 6.5
        style_p_son.leading = 7

        #estilo pymes+
        style_p_pymes = ParagraphStyle('Normal')
        style_p_pymes.fontName = 'Arial'
        style_p_pymes.fontSize = 6.5
        style_p_pymes.leading = 7
        style_p_pymes.alignment = TA_CENTER


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

        style_p_header_description_right = ParagraphStyle('Normal')
        style_p_header_description_right.fontName = 'Arial'
        style_p_header_description_right.fontSize = 8
        style_p_header_description_right.leading = 8
        style_p_header_description_right.alignment = TA_RIGHT

        style_p_header_date_validity = ParagraphStyle('Normal')
        style_p_header_date_validity.fontName = 'Arial'
        style_p_header_date_validity.fontSize = 7
        style_p_header_date_validity.leading = 7

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

            data_footer_send = [

                [
                    Paragraph('<b>Despachar a</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipTo'].upper(),
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ],
                [
                    Paragraph('<b>Dirección</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipAddress'],
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ],
                [
                    Paragraph('<b>Ciudad</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipCity'],
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ],
                [
                    Paragraph('<b>Departamento</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipDepartment'],
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ],
                [
                    Paragraph('<b>Teléfono</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipPhone'],
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ],
                [
                    Paragraph('<b>Zona</b>', style_p_subtotal),
                    Paragraph(paragraph_over_flow(text=preview_data['shipZipCode'],
                                                  width=4,
                                                  font_size=8,
                                                  leading=8), style_p_subtotal)
                ]
            ]

            # Tabla con datos de despacho
            table_footer_send = Table(
                data_footer_send,  # Contenido de la tabla
                [2.13 * cm, 4.4 * cm],  # Ancho de las columnas
                [0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.4 * cm],
                # [0.5 * cm, 2.62 * cm]
                style=table_style_footer_general  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_send.wrap(6.5 * cm, 2.62 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_send.drawOn(cnv, 1 * cm, 17.25 * cm)

            # INFORMACIÓN DE LA TABLA DE DESPACHO - FIN ---------------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE IMPUESTOS --------------------------------------------------------------------

            # preview_data['document_details'] detalles del documento
            iva_list = []
            ic_list = []
            base_value_arr = []
            iva_percent_arr = []
            ic_percent_arr = []
            tax_value_arr = []

            if page_count == self._pageNumber:

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
                        value += (_round(0 if ic[0] is None else ic[0], 2) / 100) * _round(ic[1], 2)
                        ic_percent = _round(0 if ic[0] is None else ic[0], 2)
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
            if page_count == self._pageNumber:
                base_value_par = '<br/>'.join(base_value_arr)
                iva_percent_par = '<br/>'.join(iva_percent_arr)
                ic_percent_par = '<br/>'.join(ic_percent_arr)
                tax_value_par = '<br/>'.join(tax_value_arr)

            if preview_data['currencyId'] == default_decimals.currencyId:
                new_value = '<b>Vr. BASE</b>'

            else:
                new_value = '<b>Vr.DIVISAS</b>'

            data_footer_taxes = [
                [
                    Paragraph(new_value, style_p_vrBase_right),
                    Paragraph('<b>%IVA</b>', style_p_vrBase_right),
                    Paragraph('<b>%IC</b>', style_p_vrBase_right),
                    Paragraph('<b>Vr. IMPTO</b>', style_p_vrBase_right),
                    Paragraph('', style_p_vrBase_right)
                ],
                [
                    Paragraph(base_value_par, style_p_vrBase_right),
                    Paragraph(iva_percent_par, style_p_vrBase_right),
                    Paragraph(ic_percent_par, style_p_vrBase_right),
                    Paragraph(tax_value_par, style_p_vrBase_right),
                    Paragraph('', style_p_vrBase_right)
                ]
            ]

            table_footer_taxes = Table(
                data_footer_taxes,  # Contenido de la tabla
                [2.165 * cm, 1 * cm, 1 * cm, 2.165 * cm, 0.2 * cm],  # Ancho de las columnas
                [0.3 * cm, 1.6 * cm],  # Alto de las filas
                style=table_style_footer_taxes  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_taxes.wrap(12.7 * cm, 2.6 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_taxes.drawOn(cnv, 7.53 * cm, 17.25 * cm)

            # INFORMACIÓN DE LA TABLA DE IMPUESTOS - FIN --------------------------------------------------------------

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

            data_footer_totaling = [
                [
                    Paragraph('<b>SUBTOTAL</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('<b>${:20,.{}f}</b>'.format(_round(sub_total, default_decimals.valueDecimals),
                                                          default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-Descuento</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(descuento, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-Otros Dsctos</b>', style_p_subtotal),
                    Paragraph('' if (disccount2 == '' or disccount2 == 0) else "{0}%".format(
                        '{:20,.{}f}'.format(disccount2, 2)), style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(otro_descuento, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>Base Gravable</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('<b>${:20,.{}f}</b>'.format(_round(base_gravable, default_decimals.valueDecimals),
                                                          default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>+IVA</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(iva, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>+ImpoConsumo</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(impo_consumo, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-ReteFuente</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(rete_fuente, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-Autorret. Renta</b>', style_p_subtotal),
                    Paragraph('' if (percentage_cree == '' or percentage_cree == 0) else "{0}%".format(
                        '{:20,.{}f}'.format(percentage_cree, 2)), style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(value_cree, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-ICA Retenido</b>', style_p_subtotal),
                    Paragraph('' if (rete_ica_percent == '' or rete_ica_percent == 0) else "{0}%".format(
                        '{:20,.{}f}'.format(rete_ica_percent, 2)), style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(rete_ica_value, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>-IVA Retenido</b>', style_p_subtotal),
                    Paragraph('' if (rete_iva_percent == '' or rete_iva_percent == 0) else "{0}%".format(
                        '{:20,.{}f}'.format(rete_iva_percent, 2)), style_p_subtotal_right),
                    Paragraph('${:20,.{}f}'.format(_round(rete_iva_value, default_decimals.valueDecimals),
                                                   default_decimals.valueDecimals), style_p_subtotal_right)
                ],
                [
                    Paragraph('<b>NETO COTIZACIÓN</b>', style_p_subtotal),
                    Paragraph('', style_p_subtotal_right),
                    Paragraph('<b>${:20,.{}f}</b>'.format(_round(neto_a_pagar, default_decimals.valueDecimals),
                                                          default_decimals.valueDecimals), style_p_subtotal_right)
                ]
            ]

            table_footer_totaling = Table(
                data_footer_totaling,  # Contenido de la tabla
                [2.66 * cm, 1.2 * cm, 2.67 * cm],  # Ancho de las columnas
                [0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm, 0.3 * cm,
                 0.3 * cm, 0.3 * cm, 0.5 * cm],
                style=table_style_footer_totaling  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_totaling.wrap(6.89 * cm, 4.2 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_totaling.drawOn(cnv, 14.06 * cm, 15.65 * cm)

            # linea de medicion
            # cnv.line(7.53 * cm, 30 * cm, 7.53 * cm, 1 * cm)

            # cnv.line(14.06 * cm, 30 * cm, 14.06 * cm, 1 * cm)

            # INFORMACIÓN DE LA TABLA DE TOTAL - FIN ------------------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES ----------------------------------------------------------------

            style_observaciones = ParagraphStyle('Normal')
            style_observaciones.fontName = 'Arial'
            style_observaciones.fontSize = 7
            style_observaciones.leading = 7
            style_observaciones.alignment = TA_JUSTIFY

            observaciones = '<para><b>Observaciones:</b> {0} </para>'.format(preview_data['comments'].capitalize())
            par_observations = paragraph_over_flow_height(text=observaciones,
                                                          width=12.5,
                                                          no_par=4,
                                                          font_size=8,
                                                          leading=8)

            data_footer_observations = [
                [
                    Paragraph(par_observations, style_observaciones),
                ]
            ]

            table_footer_observations = Table(
                data_footer_observations,
                [13.06 * cm, ],
                [1 * cm, ],
                style=table_style_footer_observations

            )

            # Denota el contenor de la tabla
            table_footer_observations.wrap(12.7 * cm, 1.6 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_observations.drawOn(cnv, 1 * cm, 15.65 * cm)

            # INFORMACIÓN DE LA TABLA DE OBSERVACIONES - FIN ----------------------------------------------------------

            # INFORMACIÓN DE LA TABLA DE TOTAL ESCRITO ----------------------------------------------------------------
            var_total_letter = 0
            if page_count == self._pageNumber:
                var_total_letter = preview_data['total']
            tot_word = '<para><strong>SON:</strong> {0} </para>'.format(
                total_to_letter(_round(var_total_letter, default_decimals.valueDecimals),
                                preview_data['currency'], 'M/L'))
            par_total_word = paragraph_over_flow_height(text=tot_word,
                                                        width=12.7,
                                                        no_par=3,
                                                        font_size=6.5,
                                                        leading=7)

            data_footer_total_word = [
                [
                    Paragraph(par_total_word, style_p_son),
                ]
            ]

            table_footer_total_word = Table(
                data_footer_total_word,
                [13.06 * cm, ],
                [0.6 * cm, ],
                style=table_style_footer_observations
            )

            # Denota el contenor de la tabla
            table_footer_total_word.wrap(12.7 * cm, 1.1 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_total_word.drawOn(cnv, 1 * cm, 16.65 * cm)

            # INFORMACIÓN DE LA TABLA DE TOTAL ESCRITO - FIN ----------------------------------------------------------

            # INFORMACIÓN DEL FIRMA -----------------------------------------------------------------------------------

            data_footer_sing = [
                [
                    Paragraph('{0}'.format(preview_data['createdBy'].title()), style_p_footer_centred),
                    Paragraph('Empresa', style_p_footer_centred),
                    Paragraph('Cliente', style_p_footer_centred),
                ]
            ]

            # Tabla con datos de despacho
            table_footer_sing = Table(
                data_footer_sing,  # Contenido de la tabla
                [6.53 * cm, 6.53 * cm, 6.53 * cm],  # Ancho de las columnas
                [1 * cm],
                style=table_style_footer_sing  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_sing.wrap(12.7 * cm, 2.6 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_sing.drawOn(cnv, 1 * cm, 14.65 * cm)

            company_information = Paragraph('Contabilidad Pymes+ NIT 830.506.365-7 '
                                            'Teléfono: (572) 3828300 Cali. '
                                            'www.softpymes.com.co', style_p_pymes)

            # Denota el contenor de la tabla
            company_information.wrap(16 * cm, 0.8 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            company_information.drawOn(cnv, 2.8 * cm, 14.37 * cm)

            # INFORMACIÓN DEL FIRMA - FIN -----------------------------------------------------------------------------
            # ANULADO -------------------------------------------------------------------------------------------------
            if preview_data['annuled']:
                msm = 'ANULADO'
                annuled(cnv, msm)

            cnv.restoreState()

        def annuled(cvn, str):
            cvn.saveState()

            cvn.translate(17 * cm, 22.5 * cm)
            cvn.setFontSize(80, 30)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

            # ANULADO - FIN -------------------------------------------------------------------------------------------

        def header(cnv):
            cnv.saveState()
            # VARIABLES DEL HEADER ------------------------------------------------------------------------------------

            company_name = '{0} - {1}'.format(preview_data['company_name'], preview_data['branch_name'])
            # VARIABLES DEL HEADER - FIN ------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA COMPAÑIA ------------------------------------------------------------------------

            p_company_name = Paragraph('<b>{0}</b>'.format(
                paragraph_over_flow_height(
                    text=company_name.upper(),
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
                [  # esta pendiente por valores
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
                            text='{0} {1}'.format(preview_data['regimen_iva'], preview_data['ica_activity']),
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
            paginate = Paragraph('Página {0} de {1}'.format(self._pageNumber, page_count),
                                 style_p_header_description_right)

            paginate.wrap(3 * cm, 0.4 * cm)
            paginate.drawOn(cnv, 17.5 * cm, 24.2 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA PROVEEDOR -----------------------------------------------------------------------

            if preview_data['business_agent'] == 'None':
                vendedor_name = preview_data['employee']
            else:
                vendedor_name = preview_data['business_agent']

            table_header_provider = Table(
                [
                    [
                        Paragraph('<b>Cliente</b>', style_p_header_provider),
                        Paragraph(
                            paragraph_over_flow(text=preview_data['customer'].upper(),
                                                width=10,
                                                font_size=8,
                                                leading=8),
                            style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Dirección</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_address'],
                                                      width=10,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Ciudad</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_city'],
                                                      width=10,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>País</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_country'],
                                                      width=4.6,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider),
                        Paragraph('<b>C.C ó NIT</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_nit'],
                                                      width=4,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider)
                    ],
                    [
                        Paragraph('<b>Teléfono</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_phone'],
                                                      width=4.6,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider),
                        Paragraph('<b>Celular</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=preview_data['customer_cellphone'],
                                                      width=4,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider)
                    ],
                    [
                        Paragraph('<b>Vendedor</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=vendedor_name.upper(),
                                                      width=10,
                                                      font_size=8,
                                                      leading=8),
                                  style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        '',
                        '',
                        '',
                        ''
                    ],

                ],
                [1.6 * cm, 4.96 * cm, 2 * cm, 4.5 * cm],
                0.35 * cm,
                style=table_style_header_general
            )
            table_header_provider.wrap(12.06 * cm, 2 * cm)
            table_header_provider.drawOn(cnv, 1 * cm, 21.42 * cm)

            # INFORMACION DE LA TABLA PROVEEDOR - FIN -----------------------------------------------------------------

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ -----------------------------------------------------------------

            # Validacion para documento origen
            text_order_n = '<b>{0} Nº</b>'.format(preview_data['sourceDocumentType']) \
                if preview_data['sourceDocumentType'] else ''
            text_order_n_value = '{0}{1}'.format(preview_data['sourceDocumentPrefix'],
                                                 preview_data['sourceDocumentNumber']) \
                if preview_data['sourceDocumentNumber'] else ''

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
                        term_value = preview_data['forma_pago']

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

            table_header_date_validity = Table(
                [
                    [
                        Paragraph('<b>Fecha</b>', style_p_header_date_validity),
                        Paragraph(preview_data['document_date'], style_p_header_date_validity),
                        Paragraph(text_order_n, style_p_header_date_validity),
                        Paragraph(text_order_n_value, style_p_header_date_validity)

                    ],
                    [
                        Paragraph('<b>Vence</b>', style_p_header_date_validity),
                        Paragraph(preview_data['date_finish'], style_p_header_date_validity),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Plazo</b>', style_p_header_date_validity),
                        Paragraph(term_value, style_p_header_date_validity),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Moneda</b>', style_p_header_date_validity),
                        Paragraph(preview_data['currency'].title(), style_p_header_date_validity),
                        Paragraph("<b>Tasa de Cambio</b> {0}".format(_round(preview_data['exchangeRate'], 2), 2),
                                  style_p_header_date_validity),
                        Paragraph('', style_p_header_date_validity),
                    ]

                ],
                [1.1 * cm, 2.5 * cm, 1.7 * cm, 1.23 * cm],
                0.4 * cm,
                style=table_style_header_date_validity
            )
            table_header_date_validity.wrap(5.1 * cm, 0.6 * cm)
            table_header_date_validity.drawOn(cnv, 14.06 * cm, 21.42 * cm)

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>DESCRIPCIÓN</b>', style_p_header_provider),
                        Paragraph('<b>Vr UNITARIO</b>', style_p_header_description_right),
                        Paragraph('<b>CANTIDAD</b>', style_p_header_description_right),
                        Paragraph('<b>%DSC</b>', style_p_header_description_right),
                        Paragraph('<b>%IVA</b>', style_p_header_description_right),
                        Paragraph('<b>%RTF</b>', style_p_header_description_right),
                        Paragraph('<b>VALOR</b>', style_p_header_description_right),
                    ]

                ],
                [8.9 * cm, 2 * cm, 2 * cm, 1.3 * cm, 1.2 * cm, 1.2 * cm, 3 * cm],
                [0.4 * cm],
                style=table_style_header_description
            )

            table_header_description.wrap(19.6 * cm, 0.4 * cm)
            table_header_description.drawOn(cnv, 1 * cm, 20.95 * cm)

            cnv.line(1 * cm, 20.95 * cm, 20.6 * cm, 20.95 * cm)  # Línea de firma proveedor

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            # INFORMACION DE LA TABLA ORDEN DE COMPRA No --------------------------------------------------------------

            document_type = 'COTIZACIÓN '

            document_number = 'Nº {0}'.format(preview_data['consecutive'])

            style_p_header_provider.alignment = TA_CENTER
            table_header_order_no = Table(
                [
                    [
                        Paragraph("<b>{0}<br/>{1}</b>".format(document_type, document_number),
                                  style_p_header_provider),
                    ],
                    [
                        Paragraph('', style_p_header_provider),
                    ]

                ],
                [6.53 * cm],
                [0.65 * cm, 0.2 * cm],
                style=table_style_header_order_no
            )
            table_header_order_no.wrap(7.54 * cm, 1 * cm)
            table_header_order_no.drawOn(cnv, 14.06 * cm, 23.02 * cm)

            # INFORMACION DE LA TABLA ORDEN DE COMPRA No - FIN --------------------------------------------------------

            # INFORMACION DE LA TABLA LOGO ----------------------------------------------------------------------------
            image = None if preview_data['image'] is None \
                else "{0},{1}".format("data:image/*;base64",
                                      ImagesConverter.img_convert_to_base64(preview_data['image'].image))

            if image is not None:
                img = Image(image, width=2.3 * cm, height=2.3 * cm)

                img.wrap(2.3 * cm, 2.3 * cm)
                img.drawOn(cnv, 1 * cm, 25.3 * cm)

            # INFORMACION DE LA TABLA LOGO - FIN ----------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class SalesProfessionalServicesPreviewM:
    preview_data = None

    @staticmethod
    def make_preview_pdf(preview_data):
        SalesProfessionalServicesPreviewM.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId,
                                         DefaultValue.currencyId) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 9

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        # style_num.leading = 8
        style_num.alignment = TA_RIGHT

        style_comment = ParagraphStyle('Normal')
        style_comment.fontName = 'Arial'
        style_comment.fontSize = 8
        style_comment.leading = 9
        style_comment.alignment = TA_JUSTIFY

        # Inserta los datos de Document detail en el pdf
        data = []
        for dct_det in preview_data['document_details']:
            # for i in range(10):
            data.append(
                [
                    Paragraph(dct_det.comments.capitalize(), style_comment),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.unitValue, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.quantity, default_decimals.quantityDecimals),
                                                  default_decimals.quantityDecimals), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.disccount, 2), 2), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.iva, 2), 2), style=style_num),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.withholdingTax, 2), 2),
                              style=style_num),
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
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )

        doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            x1=1 * cm,
                            y1=19.15 * cm,
                            width=19.6 * cm,
                            height=1.8 * cm,
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
                [8.9 * cm, 2 * cm, 2 * cm, 1.3 * cm, 1.2 * cm, 1.2 * cm, 3 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
