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
        preview_data = AdvanceCustomerPreview.preview_data

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

        style_p_footer_left = ParagraphStyle('Normal')
        style_p_footer_left.fontName = 'Arial'
        style_p_footer_left.fontSize = 8
        style_p_footer_left.leading = 8

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
                ('SPAN', (0, 3), (1, 5)), #observaciones
                # ('SPAN', (1, 1), (3, 1)),  # direccion
                # ('SPAN', (1, 2), (-1, -5)),  # ciudad
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('SPAN', (1, 5), (-1, -2)),  # vendedor
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
                # ('SPAN', (1, 2), (-1, -2)), #span para plazo
                # ('SPAN', (2, 3), (-1, -1)),#span para tasa de cambio
                # ('SPAN', (2, 1), (3, 1)),  # span para No orden
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
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
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

        style_p_company = ParagraphStyle('Normal')
        style_p_company.fontName = 'Arial'
        style_p_company.fontSize = 13
        style_p_company.leading = 13
        style_p_company.rightIndent = 2.8 * cm
        style_p_company.leftIndent = 2.8 * cm
        style_p_company.alignment = TA_CENTER

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

        style_p_header_comments = ParagraphStyle('Normal')
        style_p_header_comments.fontName = 'Arial'
        style_p_header_comments.fontSize = 8
        style_p_header_comments.leading = 8
        style_p_header_comments.alignment = TA_JUSTIFY

        style_p_header_description_right = ParagraphStyle('Normal')
        style_p_header_description_right.fontName = 'Arial'
        style_p_header_description_right.fontSize = 8
        style_p_header_description_right.leading = 8
        style_p_header_description_right.alignment = TA_RIGHT

        style_p_header_date_validity = ParagraphStyle('Normal')
        style_p_header_date_validity.fontName = 'Arial'
        style_p_header_date_validity.fontSize = 7
        style_p_header_date_validity.leading = 7

        style_p_header_date_validity_right = ParagraphStyle('Normal')
        style_p_header_date_validity_right.fontName = 'Arial'
        style_p_header_date_validity_right.fontSize = 7
        style_p_header_date_validity_right.leading = 7
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

            # INFORMACIÓN DEL FIRMA -----------------------------------------------------------------------------------

            data_footer_sing = [

                [
                    Paragraph(preview_data['CreatedBy'], style_p_footer_left),
                    '',
                    '',
                    Paragraph('Firma y Sello - C.C. ó NIT', style_p_footer_left),
                ]
            ]

            # Tabla con datos de despacho
            table_footer_sing = Table(
                data_footer_sing,  # Contenido de la tabla
                [4.9 * cm, 4.9 * cm, 4.9 * cm, 4.9 * cm],  # Ancho de las columnas
                [2 * cm],
                # [0.4 * cm, 1.2 * cm],
                style=table_style_footer_sing  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_sing.wrap(12.7 * cm, 2.6 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_sing.drawOn(cnv, 1 * cm, 1.3 * cm)

            company_information = Paragraph('Contabilidad Pymes+ NIT 830.506.365-7 '
                                            'Teléfono: (572)3828300 Cali. '
                                            'www.softpymes.com.co',
                                            style_p_footer_centred)

            # Denota el contenor de la tabla
            company_information.wrap(16 * cm, 0.8 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            company_information.drawOn(cnv, 2.8 * cm, 1 * cm)

            # TEXTOS FIRMAS --------------------------------------------------------------------------------------------

            elaborado = Paragraph('<b>Elaborado por</b>',style_p_footer_left)
            elaborado.wrap(16 * cm, 0.8 * cm)
            elaborado.drawOn(cnv, 1.1 * cm, 3 * cm)

            autorizado = Paragraph('<b>Autorizado por</b>', style_p_footer_left)
            autorizado.wrap(16 * cm, 0.8 * cm)
            autorizado.drawOn(cnv, 6 * cm, 3 * cm)

            revisado = Paragraph('<b>Revisado por</b>', style_p_footer_left)
            revisado.wrap(16 * cm, 0.8 * cm)
            revisado.drawOn(cnv, 10.9 * cm, 3 * cm)

            cnv.line(15.9 * cm, 1.8 * cm, 20 * cm, 1.8 * cm)

            # TEXTOS FIRMAS - FIN --------------------------------------------------------------------------------------

            # INFORMACIÓN DEL FIRMA - FIN -----------------------------------------------------------------------------
            # ANULADO -------------------------------------------------------------------------------------------------
            if preview_data['annuled']:
                msm = 'ANULADO'
                annuled(cnv, msm)

            cnv.restoreState()

        def annuled(cvn, str):
            cvn.saveState()

            cvn.translate(17 * cm, 22 * cm)
            cvn.setFontSize(80, 30)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

            # ANULADO - FIN -------------------------------------------------------------------------------------------

        def header(cnv):
            cnv.saveState()
            # VARIABLES DEL HEADER ------------------------------------------------------------------------------------

            company_name = '{0}'.format(preview_data['company_name'].upper())
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
                style_p_company)
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
                            # text='{0} {1}'.format(preview_data['nit'], preview_data['regimen']),
                            text='.'.join([str(nit1[0])[i:i + 3]
                                           for i in range(0, len(str(nit1[0])), 3)]),
                            width=12.8,
                            font_size=12,
                            leading=12), nit1[1], preview_data['regimen']),
                        style_p_sub_header_ica),
                ],

                [
                    Paragraph('<b>{0}</b>'.format(
                        paragraph_over_flow(
                            text='{0} - {1}'.format(preview_data['address'],
                                                    preview_data['branch_name']),
                            width=12.8,
                            font_size=12,
                            leading=12)),
                        style_p_sub_header_ica),
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
                        style_p_sub_header_ica),
                ],

                [
                    Paragraph('<b>{0}</b>'.format(
                        paragraph_over_flow(
                            text='{0} - {1}'.format(preview_data['city'], preview_data['department']),
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
            paginate = Paragraph('Página {0} de {1}'.format(self._pageNumber, page_count),
                                 style_p_header_description_right)

            paginate.wrap(3 * cm, 0.4 * cm)
            paginate.drawOn(cnv, 17.5 * cm, 24.2 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA PROVEEDOR -----------------------------------------------------------------------

            table_header_provider = Table(
                [
                    [
                        Paragraph('<b>Fecha</b> {0}'.format(paragraph_over_flow(
                            text=preview_data['document_date'],
                            width=11,
                            font_size=8,
                            leading=8)),
                            style_p_header_provider)

                    ],
                    [
                        Paragraph('<b>Recibo de</b> {0}'.format(paragraph_over_flow(
                            text=preview_data['customer'].upper(),
                            width=11,
                            font_size=8,
                            leading=8)),
                            style_p_header_provider),

                    ],
                    [
                        Paragraph('<b>C.C ó NIT</b> {0}'.format(paragraph_over_flow(
                            text=preview_data['customer_nit'],
                            width=8,
                            font_size=8,
                            leading=8)),
                            style_p_header_provider),

                    ],
                    [
                        Paragraph('<b>Observaciones</b> {0}'.format(paragraph_over_flow(
                            text=preview_data['comments'].capitalize(),
                            width=48,
                            font_size=8,
                            leading=8)),
                            style_p_header_comments),

                    ],
                    [
                        '',
                        ''
                    ],
                    [
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>Avance Recibo de Cliente N° </b>{0}'.format(preview_data['consecutive']),
                                  style_p_header_provider),
                        Paragraph('', style_p_header_provider),

                    ],
                    [
                        '',
                        ''
                    ]

                ],
                [13.05 * cm, 0.01 * cm],
                0.4 * cm,
                style=table_style_header_general
            )
            table_header_provider.wrap(12.06 * cm, 2 * cm)
            table_header_provider.drawOn(cnv, 1 * cm, 20.67 * cm)

            # INFORMACION DE LA TABLA PROVEEDOR - FIN -----------------------------------------------------------------

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ -----------------------------------------------------------------

            efectivo = 0
            cheque = 0
            transferencia = 0
            debito = 0
            credito = 0
            total = 0
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
            total = efectivo + credito + cheque + transferencia + debito

            table_header_date_validity = Table(
                [
                    [
                        Paragraph('<b>Efectivo</b>', style_p_header_date_validity),
                        Paragraph('{:20,.{}f}'.format(_round(efectivo, 2), 2),
                                  style_p_header_date_validity_right),
                    ],
                    [
                        Paragraph('<b>Cheque</b>', style_p_header_date_validity),
                        Paragraph('{:20,.{}f}'.format(_round(cheque, 2), 2),
                                  style_p_header_date_validity_right),
                    ],
                    [
                        Paragraph('<b>Transferencia</b>', style_p_header_date_validity),
                        Paragraph('{:20,.{}f}'.format(_round(transferencia, 2), 2),
                                  style_p_header_date_validity_right),
                    ],
                    [
                        Paragraph('<b>Tarjeta Débito</b>', style_p_header_date_validity),
                        Paragraph('{:20,.{}f}'.format(_round(debito, 2), 2),
                                  style_p_header_date_validity_right),
                    ],
                    [
                        Paragraph('<b>Tarjeta Crédito</b>', style_p_header_date_validity),
                        Paragraph('{:20,.{}f}'.format(_round(credito, 2), 2),
                                  style_p_header_date_validity_right),
                    ],
                    [
                        Paragraph('<b>TOTAL</b>', style_p_header_date_validity),
                        Paragraph('<b>${:20,.{}f}</b>'.format(_round(total, 2), 2),
                                  style_p_header_date_validity_right),
                    ]

                ],
                [3 * cm, 3.53 * cm],
                [0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm],
                style=table_style_header_date_validity
            )
            table_header_date_validity.wrap(5.1 * cm, 0.6 * cm)
            table_header_date_validity.drawOn(cnv, 14.06 * cm, 20.67 * cm)

            # INFORMACION DE LA TABLA FECHA Y VALIDEZ - FIN -----------------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>CTA</b>', style_p_header_provider),
                        Paragraph('<b>SUB</b>', style_p_header_provider),
                        Paragraph('<b>AUX</b>', style_p_header_provider),
                        Paragraph('<b>DOC N°</b>', style_p_header_provider),
                        Paragraph('<b>VENCE</b>', style_p_header_provider),
                        Paragraph('<b>TERCERO</b>', style_p_header_provider),
                        Paragraph('<b>DÉBITOS</b>', style_p_header_description_right),
                        Paragraph('<b>CRÉDITOS</b>', style_p_header_description_right)
                    ]

                ],
                [1 * cm, 1 * cm, 1 * cm, 2 * cm, 2 * cm, 7 * cm, 2.8 * cm, 2.8 * cm],
                [0.4 * cm],
                style=table_style_header_description
            )

            table_header_description.wrap(19.6 * cm, 0.4 * cm)
            table_header_description.drawOn(cnv, 1 * cm, 20 * cm)

            cnv.line(1 * cm, 19.8 * cm, 20.6 * cm, 19.8 * cm)  # Línea de firma proveedor

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            # INFORMACION DE LA TABLA ORDEN DE COMPRA No --------------------------------------------------------------

            document_type = 'RECIBO DE CAJA Nº {0}'.format(preview_data['controlNumber'])

            style_p_header_provider.alignment = TA_CENTER
            table_header_order_no = Table(
                [
                    [
                        Paragraph("<b>{0}</b>".format(document_type), style_p_header_provider),
                    ],
                    [
                        Paragraph('', style_p_header_provider),
                    ]

                ],
                [6.53 * cm],
                [0.5 * cm, 0.3 * cm],
                style=table_style_header_order_no
            )
            table_header_order_no.wrap(7.54 * cm, 1 * cm)
            table_header_order_no.drawOn(cnv, 14.06 * cm, 23.07 * cm)

            # INFORMACION DE LA TABLA ORDEN DE COMPRA No - FIN --------------------------------------------------------

            # INFORMACION DE LA TABLA LOGO ----------------------------------------------------------------------------
            image = None if preview_data['image'] is None \
                else "{0},{1}".format("data:image/*;base64",
                                      ImagesConverter.img_convert_to_base64(preview_data['image'].image))

            if image is not None:
                img = Image(image, width=2.3 * cm, height=2.3 * cm)

                img.wrap(2.3 * cm, 2.3 * cm)
                img.drawOn(cnv, 1 * cm, 24.6 * cm)

            # INFORMACION DE LA TABLA LOGO - FIN ----------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class AdvanceCustomerPreview:
    preview_data = None

    @staticmethod
    def make_preview_pdf(preview_data):
        AdvanceCustomerPreview.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId) \
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
        style_num.alignment = TA_RIGHT
        # style_num.backColor = '#FFFF00'
        # style_num.borderColor = '#000000'
        # style_num.borderWidth = 1

        # Inserta los datos de Document detail en el pdf

        data = []
        if preview_data['annuled'] == 0:
            for dct_det in preview_data['document_details']:
                if dct_det.customer is not None:
                    customer_name = "{0} {1} {2} {3} - {4}".format(
                        "" if dct_det.customer.thirdParty.tradeName is None
                        else dct_det.customer.thirdParty.tradeName.strip(),
                        "" if dct_det.customer.thirdParty.lastName is None
                        else dct_det.customer.thirdParty.lastName.strip(),
                        "" if dct_det.customer.thirdParty.maidenName is None
                        else dct_det.customer.thirdParty.maidenName.strip(),
                        "" if dct_det.customer.thirdParty.firstName is None
                        else dct_det.customer.thirdParty.firstName.strip(),
                        "" if dct_det.customer.name is None
                        else dct_det.customer.name)
                else:
                    customer_name = ''
            # for i in range(60):
                data.append(
                    [
                        Paragraph('{0}{1}{2}'.format(dct_det.puc.pucClass,
                                                     dct_det.puc.pucSubClass,
                                                     dct_det.puc.account), style),
                        Paragraph(dct_det.puc.subAccount, style),
                        Paragraph(dct_det.puc.auxiliary1, style),
                        Paragraph('' if dct_det.crossDocument is None else dct_det.crossDocument, style),
                        Paragraph('' if dct_det.dueDate is None else dct_det.dueDate, style),
                        Paragraph(customer_name, style),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.debit, 2), 2),
                                  style=style_num),
                        Paragraph('{:20,.{}f}'.format(_round(dct_det.credit, 2), 2),
                                  style=style_num)
                    ]
                )
        else:
            data.append(
                [
                    Paragraph(' ', style),
                    Paragraph(' ', style),
                    Paragraph(' ', style),
                    Paragraph(' ', style),
                    Paragraph(' ', style),
                    Paragraph(' ', style),
                    Paragraph(' ', style=style_num),
                    Paragraph(' ', style=style_num)
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
                            y1=3.4 * cm,
                            width=19.6 * cm,
                            height=16.2 * cm,
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
                [1 * cm, 1 * cm, 1 * cm, 2 * cm, 2 * cm, 7 * cm, 2.8 * cm, 2.8 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
