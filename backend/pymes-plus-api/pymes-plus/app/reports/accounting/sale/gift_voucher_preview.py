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
    num_page = 0

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
        preview_data = GiftVoucherPreview.preview_data
        NumberedCanvas.num_page = page_count

        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId,
                                         DefaultValue.currencyId,
                                         DefaultValue.commentsGiftVoucher) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        # FOOTER

        # declara estilos para los parrafos del footer
        style_p_footer = ParagraphStyle('Normal')
        style_p_footer.fontName = 'Arial'
        style_p_footer.fontSize = 8
        style_p_footer.leading = 8

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
        style_p_company.fontSize = 9
        style_p_company.leading = 7
        style_p_company.alignment = TA_CENTER

        style_p_bono_value = ParagraphStyle('Normal')
        style_p_bono_value.fontName = 'Arial'
        style_p_bono_value.fontSize = 12
        style_p_bono_value.leading = 8
        style_p_bono_value.alignment = TA_RIGHT

        style_p_header_t = ParagraphStyle('Normal')
        style_p_header_t.fontName = 'Arial'
        style_p_header_t.fontSize = 7
        style_p_header_t.leading = 6
        style_p_header_t.alignment = TA_CENTER

        style_p_header_tL = ParagraphStyle('Normal')
        style_p_header_tL.fontName = 'Arial'
        style_p_header_tL.fontSize = 7
        style_p_header_tL.leading = 6
        style_p_header_tL.alignment = TA_LEFT

        # --------------------------------------------------

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

            cvn.translate(7.5 * cm, 8 * cm)
            cvn.setFontSize(50, 70)
            cvn.setFillColorRGB(1, 0, 0, alpha=0.3)
            cvn.rotate(35)
            cvn.drawRightString(0, 0, str)

            cvn.restoreState()

            # ANULADO - FIN -------------------------------------------------------------------------------------------

        def header(cnv):
            cnv.saveState()

            # PAGINADO ------------------------------------------------------------------------------------------------


            # FIN PAGINADO --------------------------------------------------------------------------------------------


            cnv.restoreState()

        footer(self)
        header(self)

        x = GiftVoucherPreview()
        x.number_page(NumberedCanvas.num_page)


class GiftVoucherPreview:
    preview_data = None
    n = 0

    def number_page(self, num):
        GiftVoucherPreview.n = num

    @staticmethod
    def make_preview_pdf(preview_data):
        GiftVoucherPreview.preview_data = preview_data
        n = GiftVoucherPreview.n
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.currencyId,
                                         DefaultValue.branchId,
                                         DefaultValue.commentsGiftVoucher) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        # INFORMACION DE LA EMPRESA -------------------------------------------------------------------------------

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

        style_p_company = ParagraphStyle('Normal')
        style_p_company.fontName = 'Helvetica-Bold'
        style_p_company.fontSize = 9
        style_p_company.leading = 7
        style_p_company.alignment = TA_CENTER

        style_p_nit = ParagraphStyle('Normal')
        style_p_nit.fontName = 'Helvetica-Bold'
        style_p_nit.fontSize = 7
        style_p_nit.leading = 6
        style_p_nit.alignment = TA_CENTER

        style_p_header_t = ParagraphStyle('Normal')
        style_p_header_t.fontName = 'Arial'
        style_p_header_t.fontSize = 7
        style_p_header_t.leading = 6
        style_p_header_t.alignment = TA_CENTER

        style_p_header_tL = ParagraphStyle('Normal')
        style_p_header_tL.fontName = 'Arial'
        style_p_header_tL.fontSize = 7
        style_p_header_tL.leading = 6
        style_p_header_tL.alignment = TA_LEFT

        style_p_bono = ParagraphStyle('Normal')
        style_p_bono.fontName = 'Helvetica-Bold'
        style_p_bono.fontSize = 8
        style_p_bono.leading = 7
        style_p_bono.alignment = TA_LEFT

        p_company_name = Paragraph('{0}'.format(
            paragraph_over_flow_height(
                text=preview_data['company_name'].upper(),
                width=10,
                no_par=2,
                font_size=10,
                leading=10,
                left_indent=2.8,
                right_indent=2.8)),
            style_p_company)
        p_company_name.width = 8 * cm
        par_frag = p_company_name.breakLines(width=8 * cm)

        # Verifica el tamaño de el primer parrafo, Si tiene mas de 1 renglon rederiza la tabla mas abajo
        draw_company_on_y = 6.6
        if len(par_frag.lines) >= 2:
            draw_company_on_y = 6.2

        nit = preview_data['nit'].split('-')

        data_header_company = [
            [
                p_company_name,
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ],
            [
                Paragraph('NIT: {0}-{1}'.format(
                    paragraph_over_flow(
                        text='.'.join([str(nit[0])[i:i + 3]
                                       for i in range(0, len(str(nit[0])), 3)]),
                        width=7,
                        font_size=6,
                        leading=6), nit[1]),
                    style_p_nit),
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text=preview_data['branch_name'],
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_company),
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='DIR: {0}, {1}'.format(preview_data['address'],
                                                    preview_data['city']),
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_tL),
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='TEL: {0} - {1}'.format(preview_data['phone1'],
                                                     preview_data['phone2']),
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t),
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ],
            [
                Paragraph('FECHA: {0}'.format(
                    paragraph_over_flow(
                        text=preview_data['document_date'],
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t),
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ],
            [
                Paragraph('BONO REGALO N° {0}'.format(
                    paragraph_over_flow(
                        text=preview_data['consecutive'],
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_bono)
            ],
            [
                Paragraph('{0}'.format(
                    paragraph_over_flow(
                        text='',
                        width=7,
                        font_size=6,
                        leading=6)),
                    style_p_header_t)
            ]
        ]

        table_header_company = Table(
            data_header_company,
            [6.5 * cm],
            style=table_style_header
        )

        # INFORMACION DE LA EMPRESA - FIN -------------------------------------------------------------------------

        # LINEA ------------------------------------------------------------------------------------------------------

        table_style_raya = TableStyle(
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

        style_p_raya = ParagraphStyle('Normal')
        style_p_raya.fontName = 'Helvetica-Bold'
        style_p_raya.fontSize = 15
        style_p_raya.leading = 6
        style_p_raya.alignment = TA_CENTER

        line_space = []
        raya = '_' * 23
        line_space.append(
            [
                Paragraph(raya, style_p_raya)
            ]
        )

        # LINEA - FIN ------------------------------------------------------------------------------------------------

        # TOTAL -----------------------------------------------------------------------------------------------------
        table_style_footer_bono_value = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, 0), 0.15 * cm),
                # ('BOX', (0, 0), (0, 0), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        style_p_bono_value = ParagraphStyle('Normal')
        style_p_bono_value.fontName = 'Helvetica-Bold'
        style_p_bono_value.fontSize = 12
        style_p_bono_value.leading = 8
        style_p_bono_value.alignment = TA_RIGHT

        data_footer_taxes = [
            [
                Paragraph('${:20,.{}f}'.format(_round(preview_data['total'], default_decimals.valueDecimals),
                                                      default_decimals.valueDecimals), style_p_bono_value)
            ]
        ]

        table_footer_total = Table(
            data_footer_taxes,  # Contenido de la tabla
            [6.5 * cm],  # Ancho de las columnas
            [0.7 * cm],  # Alto de las filas
            style=table_style_footer_bono_value  # Estilos de la tabla
        )

        # FIN TOTAL ---------------------------------------------------------------------------------------------------

        # TABLA TOTAL ESCRITO -----------------------------------------------------------------------------------------

        table_style_total_write= TableStyle(
            [
                ('LEFTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (0, 0), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, 0), 0.15 * cm),
                # ('BOX', (0, 0), (0, 0), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        style_p_total_write = ParagraphStyle('Normal')
        style_p_total_write.fontName = 'Arial'
        style_p_total_write.fontSize = 8
        style_p_total_write.leading = 8

        var_total_letter = 0

        var_total_letter = preview_data['total']
        tot_word = '{0}'.format(
            total_to_letter(_round(var_total_letter, default_decimals.valueDecimals),
                            preview_data['currency'], 'M/L'))
        par_total_word = paragraph_over_flow_height(text=tot_word,
                                                    width=10,
                                                    no_par=2,
                                                    font_size=8,
                                                    leading=8)

        data_footer_total_word = [
            [
                Paragraph(par_total_word, style_p_total_write),
            ]
        ]

        table_footer_total_word = Table(
            data_footer_total_word,
            [6.8 * cm, ],
            [0.5 * cm, ],
            style=table_style_total_write
        )

        # TABLA TOTAL ESCRITO FIN -------------------------------------------------------------------------------------

        # INFORMACIÓN DE LA TABLA DE OBSERVACIONES ----------------------------------------------------------------

        style_p_observations = ParagraphStyle('Normal')
        style_p_observations.fontName = 'Arial'
        style_p_observations.fontSize = 7
        style_p_observations.leading = 7
        style_p_observations.alignment = TA_JUSTIFY

        comments_bono = ' ' if preview_data['comments'] == ' ' else '* {0}'.format(preview_data['comments'].capitalize())

        comentario = Paragraph(comments_bono, style_p_observations)

        # INFORMACIÓN DE LA TABLA DE OBSERVACIONES - FIN ----------------------------------------------------------

        # DESCRIPCION BONO REGALO ---------------------------------------------------------------------------------

        style_p_description_bono = ParagraphStyle('Normal')
        style_p_description_bono.fontName = 'Arial'
        style_p_description_bono.fontSize = 7
        style_p_description_bono.leading = 7
        style_p_description_bono.alignment = TA_JUSTIFY

        pymes2 = Paragraph('{0}'.format(default_decimals.commentsGiftVoucher),
                           style_p_description_bono)

        # DESCRIPCION BONO REGALO - FIN ---------------------------------------------------------------------------

        # TEXTO SOFTPYMES -----------------------------------------------------------------------------------------

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
        style_p_softpymes.fontSize = 8
        style_p_softpymes.leading = 8.5
        style_p_softpymes.alignment = TA_CENTER

        softpymes = '<br/>Factura impresa por software Pymes+ ' \
                    '<br/>Desarrollado por Softpymes SAS <br/>NIT 830.506.365-7' \
                    '<br/>www.softpymes.com.co <br/>Teléfono: (572) 3828300 Cali'
        pymes = Paragraph('{0}'.format(softpymes),
                          style_p_softpymes)

        # TEXTO SOFTPYMES - FIN -----------------------------------------------------------------------------------

        # ESPACIO ------------------------------------------------------------------------------------------------------

        space = []
        space.append(
            [
                Paragraph('', style_p_softpymes)
            ])

        # ESPACIO - FIN ------------------------------------------------------------------------------------------------
        value = 10 * n

        doc = BaseDocTemplate(outfilepath, pagesize=(7.5 * cm, 50 * cm))

        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            x1=0.5 * cm,
                            y1=4.5 * cm,
                            width=6.5 * cm,
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
            [table_header_company,
             Table(
                 line_space,
                 [7 * cm],
                 style=table_style_raya
             ),
             Table(
                 space,
                 [6.5 * cm],
                 0.5 * cm,
                 style=table_style_softpymes
             ),
             table_footer_total,
             table_footer_total_word,
             Table(
                 line_space,
                 [7 * cm],
                 style=table_style_raya
             ),
             Table(
                 space,
                 [6.5 * cm],
                 0.5 * cm,
                 style=table_style_softpymes
             ),
             comentario,
             Table(
                 space,
                 [6.5 * cm],
                 style=table_style_softpymes
             ),
             pymes2,
             Table(
                 space,
                 [6.5 * cm],
                 style=table_style_softpymes
             ),
             pymes
             ],
            canvasmaker=NumberedCanvas
        )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
