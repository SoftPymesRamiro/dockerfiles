# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David"]

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, Image
import os
from ... import session
import uuid
from ...models import DefaultValue
from ...utils.math_ext import _round
from ...utils.image_converter import ImagesConverter
from ...utils.converters import *
import locale
from ..libs.styles import *


pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold')

locale.setlocale(locale.LC_ALL, '')


class DocumentAccounting:
    """DocumentAccounting as a public class.

       note::

       """

    @staticmethod
    def get_doucment_data():
        pass


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
        preview_data = DocumentAccountingPreview.preview_data

        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId)\
                                  .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        table_style_footer_totaling = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0 * cm),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, (0, 0, 0)),
                ('LINEBELOW', (0, 1), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (0, 1), (-1, -1)),
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

        table_style_header_description = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEABOVE', (0, 0), (-1, -1), 1, (0, 0, 0)),
                # ('LINEBELOW', (0, 1), (-1, -1), 1, (0, 0, 0)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (0, 1), (-1, -1)),
                ('SPAN', (0, 2), (-1, -1))
            ]
        )

        def paragraph_over_flow(**kwargs):
            """
            if the text on paragraph make a brake line only return the first line
            :param kwargs:
            :return:
            """

            left_indt = 0 if not kwargs.get('left_indent') else kwargs.get('left_indent')
            right_indt = 0 if not kwargs.get('right_indent') else kwargs.get('right_indent')

            style_inner_p = ParagraphStyle('Normal')
            style_inner_p.fontName = 'Arial'
            style_inner_p.fontSize = kwargs.get('font_size')
            style_inner_p.leading = kwargs.get('leading')
            style_inner_p.rightIndent = right_indt * cm
            style_inner_p.leftIndent = left_indt * cm

            # obtiene el texto del parrafo y le agrega los estilos correspondientes
            long_par = Paragraph(str(kwargs.get('text')), style_inner_p)
            # Asigna un ancho especifico al parrafo
            long_par.width = kwargs.get('width') * cm

            # agrega los saltos de línea correspondientes al ancho asignado
            par_frag = long_par.breakLines(width=kwargs.get('width') * cm)

            # Si el parrafo no tiene líneas retorna un string vacio
            if not len(par_frag.lines):
                return ''
            # pra_frag.kind == 0 cuando es texto agregado normalmente y en == 1 cuando tiene </br> en el texto
            if par_frag.kind == 0:
                short_text = " ".join(par_frag.lines[0][1])
            else:
                short_text = " ".join([w.text for w in par_frag.lines[0].words])

            return short_text

        def paragraph_over_flow_height(**kwargs):
            """
            if the text on paragraph make a brake line only return the first line
            :param kwargs:
            :return:
            """

            left_indt = 0 if not kwargs.get('left_indent') else kwargs.get('left_indent')
            right_indt = 0 if not kwargs.get('right_indent') else kwargs.get('right_indent')

            style_inner_p = ParagraphStyle('Normal')
            style_inner_p.fontName = 'Arial'
            style_inner_p.fontSize = kwargs.get('font_size')
            style_inner_p.leading = kwargs.get('leading')
            style_inner_p.rightIndent = right_indt * cm
            style_inner_p.leftIndent = left_indt * cm

            # obtiene el texto del parrafo y le agrega los estilos correspondientes
            long_par = Paragraph(str(kwargs.get('text')), style_inner_p)
            # Asigna un ancho especifico al parrafo
            long_par.width = kwargs.get('width') * cm
            no_par = kwargs.get('no_par')

            # agrega los saltos de línea correspondientes al ancho asignado
            par_frag = long_par.breakLines(width=kwargs.get('width') * cm)
            par_words = []
            # Si el parrafo no tiene líneas retorna un string vacio
            if not len(par_frag.lines):
                return ''
            # Si el parrafo no supera el número de saltos de línea máximo retorna el string completo
            if len(par_frag.lines) <= no_par:
                return kwargs.get('text')
            # pra_frag.kind == 0 cuando es texto agregado normalmente y en == 1 cuando tiene </br> en el texto
            if par_frag.kind == 0:
                for i in range(no_par):
                    par_words.append(" ".join(par_frag.lines[i][1]))
            else:
                for i in range(no_par):
                    # par_words.append([w.text for w in par_frag.lines[i].words[0].text])
                    par_words.append(par_frag.lines[i].words[0].text)

            short_word = " ".join([w for w in par_words])

            return short_word

        def footer(cnv):
            """
            draw the page footer
            :param cnv:
            :return:
            """
            cnv.saveState()

            fecha = Paragraph('{:%d/%m/%Y %H:%M:%S}'.format(datetime.now()), style_p_normal_right)
            # # Denota el contenor de la tabla
            fecha.wrap(3 * cm, 2 * cm)
            # # Dibuja la tabla en las coordenadas indicadas
            fecha.drawOn(cnv, 17.6 * cm, 1 * cm)

            # INFORMACIÓN DE LA TABLA DE TOTAL - FIN ------------------------------------------------------------------

            cnv.restoreState()

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
            draw_company_on_y = 25
            if len(par_frag.lines) >= 2:
                draw_company_on_y = 23.9

            data_header_company = [
                    [
                        p_company_name,
                    ],
                    [
                        Paragraph('<b>NIT: {0}</b>'.format(
                            paragraph_over_flow(
                                text=preview_data['nit'],
                                width=12.8,
                                font_size=12,
                                leading=12)),
                            style_p_normal_centred),
                    ],
                    [
                        Paragraph('<b>{0}</b>'.format(
                            paragraph_over_flow(
                                text='CONTABILIZACIÓN',
                                width=19.6,
                                font_size=9.5,
                                leading=9.5)),
                            style_p_normal_centred)
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
                                 style_p_normal_right)

            paginate.wrap(3 * cm, 0.4 * cm)
            paginate.drawOn(cnv, 17.5 * cm, 24.5 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>CUENTA PUC</b>', style_p_normal),
                        Paragraph('<b>BOD</b>', style_p_normal),
                        Paragraph('<b>TERCERO</b>', style_p_normal),
                        Paragraph('<b>DOC Nº</b>', style_p_normal_centred),
                        Paragraph('<b>VENCE</b>', style_p_normal_centred),
                        Paragraph('<b>CANTIDAD</b>', style_p_normal_right),
                        Paragraph('<b>DEBITOS</b>', style_p_normal_right),
                        Paragraph('<b>CREDITOS</b>', style_p_normal_right),
                    ],
                    [
                        Paragraph('<b>COMPROBANTE {0} {1}</b>'.format(preview_data['short_word'],
                                                                      preview_data['document_type']), style_p_normal),
                        # Paragraph('<b>BOD</b>', style_p_header_grid),

                    ],
                    [
                        Paragraph('<b>NÚMERO {0}{1} FECHA {2}</b>'.format('' if not preview_data['document_prefix']
                                                                          else preview_data['document_prefix'],
                                                                          preview_data['document_number'],
                                                                          preview_data['accounting_date']
                                                                          .strftime('%d/%m/%Y')), style_p_normal),
                    ]
                ],
                [1.91 * cm, 0.73 * cm, 6.3 * cm, 2.65 * cm, 1.7 * cm, 1.60 * cm, 2.35 * cm, 2.38 * cm],
                [0.4 * cm, 0.4 * cm, 0.4 * cm],
                style=table_style_header_description
            )

            table_header_description.wrap(19.6 * cm, 0.8 * cm)
            table_header_description.drawOn(cnv, 1 * cm, 23 * cm)

            # cnv.line(1 * cm, 23.7 * cm, 20.6 * cm, 23.7 * cm)  # Línea de firma proveedor

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            # INFORMACION DE LA TABLA LOGO ----------------------------------------------------------------------------
            image = None if preview_data['image'] is None \
                else "{0},{1}".format("data:image/*;base64", ImagesConverter.img_convert_to_base64(preview_data['image']
                                                                                                   .image))

            if image is not None:
                img = Image(image, width=2.3 * cm, height=2.3 * cm)

                img.wrap(2.3 * cm, 2.3 * cm)
                img.drawOn(cnv, 1 * cm, 25 * cm)

            # INFORMACION DE LA TABLA LOGO - FIN ----------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class DocumentAccountingPreview:
    preview_data = None
    @staticmethod
    def make_preview_pdf(preview_data):
        DocumentAccountingPreview.preview_data = preview_data
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId) \
            .filter(DefaultValue.branchId == preview_data['branch_id']).first()
        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        # Inserta los datos de Document detail en el pdf
        data = []
        for dct_det in preview_data['details']:
            identification_number = None if dct_det.identificationNumber is None else dct_det.identificationNumber+"-"+dct_det.identificationDV + " "
            third_name = ("" if not dct_det.identificationNumber else identification_number) + dct_det.name if dct_det.name else ""
            dct_det = dct_det[0]

            puc_account = '{0}{1}{2}-{3}-{4}'.format(dct_det.puc.pucClass, dct_det.puc.pucSubClass, dct_det.puc.account,
                                                     dct_det.puc.subAccount, dct_det.puc.auxiliary1)
            cross_prefix = '' if not dct_det.crossPrefix else dct_det.crossPrefix
            cross_document = '' if not dct_det.crossDocument else dct_det.crossDocument
            due_date = dct_det.dueDate.strftime('%d/%m/%Y') if dct_det.dueDate is not None else ''
            quantity = 0 if not dct_det.quantity else dct_det.quantity

            data.append(
                [
                    Paragraph(puc_account, style_p_normal),
                    Paragraph('' if not dct_det.warehouse else dct_det.warehouse.code, style_p_normal),
                    Paragraph(third_name, style_p_normal),
                    Paragraph('{0}{1}'.format(cross_prefix, cross_document), style_p_normal_right),
                    Paragraph(due_date, style_p_normal),
                    Paragraph('{:20,.{}f}'.format(_round(quantity, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals),
                              style=style_p_normal_right),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.debit, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals),
                              style=style_p_normal_right),
                    Paragraph('{:20,.{}f}'.format(_round(dct_det.credit, default_decimals.valueDecimals),
                                                  default_decimals.valueDecimals),
                              style=style_p_normal_right)
                ]
            )

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1),  0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
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
                            y1=1.5 * cm,
                            width=19.6 * cm,
                            height=21.5 * cm,
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

        table_style_footer_totaling = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0 * cm),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, (0, 0, 0)),
                ('LINEBELOW', (0, 1), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (0, 1), (-1, -1)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
            ]
        )
        total_debits = 0
        total_credits = 0

        for dct_det in preview_data['details']:
            dct_det = dct_det[0]
            total_credits += dct_det.credit
            total_debits += dct_det.debit
        total = total_debits - total_credits
        data_footer_totaling = [
            [
                Paragraph('', style_p_normal),
                Paragraph('<b>TOTAL</b>', style_p_normal),
                Paragraph('<b>{0}</b>'.format(
                    '{:20,.{}f}'.format(_round(total_debits, default_decimals.valueDecimals),
                                        default_decimals.valueDecimals)
                ), style_p_normal_right),
                Paragraph('<b>{0}</b>'.format(
                    '{:20,.{}f}'.format(_round(total_credits, default_decimals.valueDecimals),
                                        default_decimals.valueDecimals)
                ), style_p_normal_right)
            ],
            [
                Paragraph('<b>{0}</b>'.format(
                    '{:20,.{}f}'.format(_round(total, default_decimals.valueDecimals),
                                        default_decimals.valueDecimals)
                ), style_p_normal_right)
            ]
        ]

        table_footer_totaling = Table(
            data_footer_totaling,  # Contenido de la tabla
            [12.4 * cm, 2.5 * cm, 2.35 * cm, 2.38 * cm],  # Ancho de las columnas
            style=table_style_footer_totaling  # Estilos de la tabla
        )

        doc.build(
            [Table(
                data,
                [1.91 * cm, 0.73 * cm, 6.3 * cm, 2.65 * cm, 1.7 * cm, 1.60 * cm, 2.35 * cm, 2.38 * cm],
                style=table_style
            ), table_footer_totaling],
            canvasmaker=NumberedCanvas
        )

        # c.showPage()
        # c.save()
        return "{0}".format(outfilename)
