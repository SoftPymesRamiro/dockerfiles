__author__ = "SoftPymes"
__credits__ = ["Chelo"]

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
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
        preview_data = SaleOrderPreviewT.preview_data

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

        # factura impresa
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
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
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
        # tirilla
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
                # ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
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
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.01 * cm),
                # ('RIGHTPADDING', (0, 0), (-2, 0), 0),
                # ('TOPPADDING', (0, 0), (-1, 0), 0.24 * cm),
                # ('BOTTOMPADDING', (0, 0), (-1, 0), 0.1 * cm),
                # ('BOTTOMPADDING', (0, -1), (-1, -1), 0.31 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('VALIGN', (0, 0), (-3, -1), 'TOP'),
                # ('VALIGN', (-2, 0), (-1, -1), 'MIDDLE'),
                ('SPAN', (1, 2), (-1, -2)),  # span para plazo
                ('SPAN', (2, 3), (-1, -1)),  # span para tasa de cambio
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ]
        )

        # estilo moneda extranjera
        table_style_header_date_validity2 = TableStyle(
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
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
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

        # TIRILLA
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

        # --------------------------------------------------

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

            # ANULADO -------------------------------------------------------------------------------------------------

            if preview_data['annuled']:
                msm = 'ANULADO'
                annuled(cnv, msm)

            cnv.restoreState()

        def annuled(cvn, str):
            cvn.saveState()

            cvn.translate(8 * cm, 10 * cm)
            cvn.setFontSize(50, 70)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

            # ANULADO - FIN -------------------------------------------------------------------------------------------
            # cnv.restoreState()

        def header(cnv):
            cnv.saveState()
            # VARIABLES DEL HEADER ------------------------------------------------------------------------------------
            if preview_data['currencyId'] == default_decimals.currencyId:
                company_name = '{0}<br/>{1}'.format(preview_data['company_name'], preview_data['branch_name'])
            elif preview_data['currencyId'] != default_decimals.currencyId:
                company_name = '{0} - {1}'.format(preview_data['company_name'], preview_data['branch_name'])
            # VARIABLES DEL HEADER - FIN ------------------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class SaleOrderPreviewT:
    preview_data = None

    @staticmethod
    def make_preview_pdf(preview_data):
        SaleOrderPreviewT.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.currencyId,
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

        # cabecera de la tirilla

        style_p_company = ParagraphStyle('Normal')
        style_p_company.fontName = 'Arial'
        style_p_company.fontSize = 9
        style_p_company.leading = 10
        style_p_company.alignment = TA_CENTER

        style_p_header_t = ParagraphStyle('Normal')
        style_p_header_t.fontName = 'Arial'
        style_p_header_t.fontSize = 8
        style_p_header_t.leading = 10
        style_p_header_t.alignment = TA_CENTER

        style_p_header_tR = ParagraphStyle('Normal')
        style_p_header_tR.fontName = 'Arial'
        style_p_header_tR.fontSize = 7.5
        style_p_header_tR.leading = 10
        style_p_header_tR.alignment = TA_RIGHT

        style_p_header_tL = ParagraphStyle('Normal')
        style_p_header_tL.fontName = 'Arial'
        style_p_header_tL.fontSize = 7.5
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
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['branch_name'],
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text='NIT: {0}'.format(preview_data['nit']),
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['address'],
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text='{0} - {1}'.format(preview_data['city'],
                                                                          preview_data['department']),
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

                ],
                [
                    '',
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
                        width=10,
                        font_size=8,
                        leading=8),
                        style_p_header_t),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['regimen'],
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

                ],
                [
                    '',
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=preview_data['document_date'],
                                                  width=4.8,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''

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
                    Paragraph(paragraph_over_flow(text='PEDIDO N° {0}'.format(preview_data['consecutive']),
                                                  width=10,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''
                ],
                [
                    Paragraph(paragraph_over_flow(text=raya,
                                                  width=7,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_t),
                    ''
                ],

            ],
            [7.9 * cm, 0.1 * cm],
            0.2 * cm,
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
        # raya----------------------------------------------------------------------------------------------------------------
        table_header_raya = Table(
            [
                [
                    Paragraph(paragraph_over_flow(text=raya,
                                                  width=7,
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
            [7.9 * cm, 0.1 * cm],
            0.2 * cm,
            style=table_style_header_general2
        )

        # tabla totales -----------------------------------------------------------------------------------------------------
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
        sub_total = _round(preview_data['sub_total'], default_decimals.valueDecimals)
        descuento = _round(preview_data['discount'], default_decimals.valueDecimals)
        iva = _round(preview_data['iva'], default_decimals.valueDecimals)
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
                Paragraph('IVA', style_p_header_tL),
                Paragraph('{:20,.{}f}'.format(_round(iva, default_decimals.valueDecimals),
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

        # descripcion iva ---------------------------------------------------------------------------------------------------
        table_description_iva = Table(
            [
                [
                    Paragraph('', style_p_header_tL),
                    Paragraph('BASE', style_p_header_tR),
                    Paragraph('%IVA', style_p_header_tR),
                    Paragraph('Vr IVA', style_p_header_tR),
                ]

            ],
            [1.4 * cm, 2 * cm, 1.6 * cm, 2 * cm],
            [0.2 * cm],
            style=table_style_header_description
        )

        # detalle iva -------------------------------------------------------------------------------------------------------
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

        # datos cliente ------------------------------------------------------------------------------------------------------

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

        term_value = '{0} DÍA(S)'.format(preview_data['termDays'])

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
                    Paragraph('VENDEDOR:', style_p_header_tL),
                    Paragraph(paragraph_over_flow(text=vendedor_name[0].upper(),
                                                  width=4.5,
                                                  font_size=8,
                                                  leading=8),
                              style_p_header_tL),
                ],
                [
                    Paragraph('PLAZO:', style_p_header_tL),
                    Paragraph(term_value, style_p_header_tL)
                ]
            ],

            [2.5 * cm, 4.5 * cm],  # Ancho de las columnas
            0.3 * cm,
            style=table_style_footer_client  # Estilos de la tabla
        )

        # ESPACIO ------------------------------------------------------------------------------------------------------

        table_style_softpymes = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, 0), 0.15 * cm),
                # ('BOX', (0, 0), (0, 0), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        style_p_softpymes = ParagraphStyle('Normal')
        style_p_softpymes.fontName = 'Arial'
        style_p_softpymes.fontSize = 7
        style_p_softpymes.leading = 6
        style_p_softpymes.alignment = TA_CENTER

        space = []
        space.append(
            [
                Paragraph('', style_p_softpymes)
            ])

        # ESPACIO - FIN ------------------------------------------------------------------------------------------------

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
        style_p_pymes.fontSize = 8
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
        style_numT.fontSize = 8
        style_numT.alignment = TA_RIGHT

        style_numTL = ParagraphStyle('Normal')
        style_numTL.fontName = 'Arial'
        style_numTL.fontSize = 8
        style_numTL.alignment = TA_LEFT

        data = []
        for dct_det in preview_data['document_details']:

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

        # doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        doc = BaseDocTemplate(outfilepath, pagesize=(8.5 * cm, 50 * cm))

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

        doc.build(
            [table_header_tirilla,
             Table(
                 space,
                 [6.5 * cm],
                 style=table_style_softpymes
             ),
             table_header_description,
             table_header_raya,
             Table(
                 data,
                 [1.5 * cm, 2.5 * cm, 1 * cm, 2 * cm],
                 style=table_style
             ), table_header_raya,
             table_footer_totaling,
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
             Table(
                 space,
                 [6.5 * cm],
                 style=table_style_softpymes
             ),
             table_footer_pymes],
            canvasmaker=NumberedCanvas
        )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
