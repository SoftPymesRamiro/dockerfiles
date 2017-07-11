from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, FrameBreak, KeepTogether, NextPageTemplate, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
import os
import math
from .... import session
from decimal import *
from itertools import groupby
import uuid
from ....models import DefaultValue
from ....utils.math_ext import _round
import locale
# from io import BytesIO

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold')

locale.setlocale(locale.LC_ALL, '')


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
        preview_data = InvoiceImportPreview.preview_data

        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId)\
                                  .filter(DefaultValue.branchId == 13).first()
        #  TODO Quitar branchId quemado cuando funcione la consulta
                                  # .filter(DefaultValue.branchId == preview_data['branch_id']).first()

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

        style_p_footer_left = ParagraphStyle('Normal')
        style_p_footer_left.fontName = 'Arial'
        style_p_footer_left.fontSize = 8
        style_p_footer_left.leading = 8
        style_p_footer_left.alignment = TA_LEFT

        # HEADER

        table_style_header = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (0, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (0, -1), 0),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_header_general = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (0, 3), (1, 4)),
                ('SPAN', (2, 0), (-2, 3)),
                ('SPAN', (-1, 0), (-1, 3)),
                ('SPAN', (2, 4), (-1, 5)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (-2, -2), (-1, -1), 'TOP'),
                ('VALIGN', (0, 3), (1, 4), 'TOP')

            ]
        )

        table_style_header_description = TableStyle(
            [
                ('LEFTPADDING', (1, 0), (-1, 0), 0.1 * cm),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (0, 0), (-1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, 0), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        )

        table_style_footer_sing = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                ('VALIGN', (0, -1), (-1, -1), 'BOTTOM'),
                ('LINEBEFORE', (1, 0), (-1, -1), 1, (0, 0, 0))
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

        style_p_sub_header_centred = ParagraphStyle('Normal')
        style_p_sub_header_centred.fontName = 'Arial'
        style_p_sub_header_centred.fontSize = 8
        style_p_sub_header_centred.leading = 8
        style_p_sub_header_centred.alignment = TA_CENTER

        style_p_header_provider = ParagraphStyle('Normal')
        style_p_header_provider.fontName = 'Arial'
        style_p_header_provider.fontSize = 8
        style_p_header_provider.leading = 7

        style_p_header_calc = ParagraphStyle('Normal')
        style_p_header_calc.fontName = 'Arial'
        style_p_header_calc.fontSize = 8
        style_p_header_calc.leading = 7
        style_p_header_calc.alignment = TA_RIGHT

        style_p_header_date_validity = ParagraphStyle('Normal')
        style_p_header_date_validity.fontName = 'Arial'
        style_p_header_date_validity.fontSize = 7
        style_p_header_date_validity.leading = 7

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

            # INFORMACIÓN DEL FIRMA -----------------------------------------------------------------------------------

            data_footer_sing = [
                [
                    Paragraph('Elaborado por', style_p_footer_left),
                    Paragraph('Autorizado por', style_p_footer_left),
                    Paragraph('Revisado por', style_p_footer_left),
                    Paragraph('Recibido', style_p_footer_left),
                ],
                [
                    Paragraph('Administrador del Sistema', style_p_footer_left),
                    '',
                    '',
                    Paragraph('Firma y Sello - CC ó NIT', style_p_footer_centred),
                ]
            ]

            # Tabla con datos de despacho
            table_footer_sing = Table(
                data_footer_sing,  # Contenido de la tabla
                [3.8 * cm, 3.6 * cm, 3.6 * cm, 5 * cm],  # Ancho de las columnas
                [0.5 * cm, 0.7 * cm],
                style=table_style_footer_sing  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_sing.wrap(16 * cm, 1.2 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_sing.drawOn(cnv, 2.8 * cm, 3.4 * cm)

            # INFORMACIÓN DEL FIRMA - FIN -----------------------------------------------------------------------------

            cnv.restoreState()

        def header(cnv):
            cnv.saveState()

            # CHEQUE --------------------------------------------------------------------------------------------------

            # check_data = ['asd', 'fgh', 'jkl']

            # if self._pageNumber == page_count and page_count < len(check_data):
            #     check = Paragraph(check_data[self._pageNumber - 1], style_p_header)
            #
            #     check.wrap(14.5 * cm, 2 * cm)
            #     check.drawOn(cnv, 2.8 * cm, 20.3 * cm)
            #     cnv.showPage()
            #     return

            if len(preview_data['checkBook']) == 1:
                p_titular = Paragraph('ADRIAN SERNA GOMEZ', style_p_header_provider)

                p_titular.wrap(14.5 * cm, 2 * cm)
                p_titular.drawOn(cnv, 3.7 * cm, 24.7 * cm)

                p_total_letras = Paragraph('VENTICINCOMIL PESOS CON 00/100 M/L', style_p_header_provider)

                p_total_letras.wrap(14.5 * cm, 2 * cm)
                p_total_letras.drawOn(cnv, 3.7 * cm, 23.9 * cm)

                p_ano = Paragraph('2016', style_p_header_provider)

                p_ano.wrap(14.5 * cm, 2 * cm)
                p_ano.drawOn(cnv, 10.4 * cm, 25.4 * cm)

                p_mes = Paragraph('11', style_p_header_provider)

                p_mes.wrap(14.5 * cm, 2 * cm)
                p_mes.drawOn(cnv, 11.8 * cm, 25.4 * cm)

                p_dia = Paragraph('11', style_p_header_provider)

                p_dia.wrap(14.5 * cm, 2 * cm)
                p_dia.drawOn(cnv, 12.8 * cm, 25.4 * cm)

                p_total_numeros = Paragraph('*******25.000,00', style_p_header_provider)

                p_total_numeros.wrap(14.5 * cm, 2 * cm)
                p_total_numeros.drawOn(cnv, 15.9 * cm, 25.4 * cm)

            # CHEQUE --------------------------------------------------------------------------------------------------

            # PAGINADO ------------------------------------------------------------------------------------------------

            # page_count == self._pageNumber
            # paginate = Paragraph('Página {0} de {1}'.format(self._pageNumber, page_count),
            #                      style_p_header_calc)
            #
            # paginate.wrap(3 * cm, 0.4 * cm)
            # paginate.drawOn(cnv, 17.5 * cm, 23.5 * cm)

            # PAGINADO - FIN ------------------------------------------------------------------------------------------

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL -----------------------------------------------------------

            table_header_data = Table(
                [
                    [
                        Paragraph('NOMBRE PROVEEDOR XYZ', style_p_header_provider),
                        Paragraph('COMPROBANTE DE EGRESO Nº', style_p_header_provider),
                        Paragraph('0000000124', style_p_header_provider)
                    ],
                    [
                        Paragraph('<b>NIT:   1.151.947.099</b>', style_p_header_provider),
                        Paragraph('ANTICIPO A TERCERO Nº', style_p_header_provider),
                        Paragraph('0000000024', style_p_header_provider)
                    ]
                ],
                [7.7 * cm, 4.6 * cm, 3.7 * cm],
                [0.4 * cm, 0.6 * cm],
                style=table_style_header
            )
            table_header_data.wrap(14.5 * cm, 2 * cm)
            table_header_data.drawOn(cnv, 2.8 * cm, 18.3 * cm)

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL - FIN -----------------------------------------------------

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL -----------------------------------------------------------
            paymentMet = '<br/><br/><b>TOTAL</b>'
            paymentMetValue = '<br/><br/> 0,00'

            if self._pageNumber == 1 :
                paymentMet = '<b>CHEQUE</b> <br/> <b>EFECTIVO</b> <br/> <b>TARJETA DE CRÉDITO</b> <br/> <b>TRANSFERENCIA</b> <br/> <b>BONOS</b> <br/><br/> <b>TOTAL</b>'
                paymentMetValue = '25.000,00 <br/> 25.000,00 <br/> 25.000,00 <br/> 25.000,00 <br/> 25.000,00 <br/><br/> 25.000,00'
            table_header_provider = Table(
                [
                    [
                        Paragraph('<b>FECHA</b>', style_p_header_provider),
                        Paragraph('10 NOV. 2016', style_p_header_provider),
                        Paragraph(paymentMet, style_p_header_provider),
                        Paragraph(paymentMetValue, style_p_header_calc)
                    ],
                    [
                        Paragraph('<b>PAGADO A</b>', style_p_header_provider),
                        Paragraph('ADRIAN SERNA', style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>CC ó NIT</b>', style_p_header_provider),
                        Paragraph('1151947099', style_p_header_provider),
                        '',
                        ''
                    ],
                    [
                        Paragraph('<b>SON</b> ', style_p_header_provider),
                        '',
                        '',
                        ''
                    ],
                    [
                        '',
                        '',
                        Paragraph('<b>OBSERVACIONES</b> OBSERVACION OBSERVACION', style_p_header_provider),
                        ''
                    ],
                    [
                        Paragraph('<b>CHEQUE/DOC N</b>', style_p_header_provider),
                        Paragraph('10 NOV. 2016', style_p_header_provider),
                        '',
                        ''
                    ],



                ],
                [2.6 * cm, 6 * cm, 3.4 * cm, 4 * cm],
                [0.4 * cm, 0.4 * cm, 0.4 * cm, 0.8 * cm, 0.4 * cm, 0.4 * cm],
                style=table_style_header_general
            )
            table_header_provider.wrap(14.5 * cm, 2 * cm)
            table_header_provider.drawOn(cnv, 2.8 * cm, 15.5 * cm)

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL - FIN -----------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>CUENTA</b>', style_p_sub_header_centred),
                        Paragraph('<b>DOCUMENTO</b>', style_p_sub_header_centred),
                        Paragraph('<b>TERCERO</b>', style_p_sub_header_centred),
                        Paragraph('<b>%</b>', style_p_sub_header_centred),
                        Paragraph('<b>DEBITO</b>', style_p_sub_header_centred),
                        Paragraph('<b>CREDITO</b>', style_p_sub_header_centred)
                    ]

                ],
                [2.1 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
                [0.4 * cm],
                style=table_style_header_description
            )

            table_header_description.wrap(16 * cm, 0.4 * cm)
            table_header_description.drawOn(cnv, 2.8 * cm, 15 * cm)

            cnv.line(2.8 * cm, 15 * cm, 18.8 * cm, 15 * cm)  # Línea de firma proveedor

            # INFORMACION DE LA TABLA DESCRIPTION - FIN ---------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self)


class InvoiceImportPreview:
    preview_data = None

    @staticmethod
    def make_same_page_preview_pdf(preview_data):
        InvoiceImportPreview.preview_data = preview_data
        #  TODO Quitar comentario cuando funcione la consulta
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId) \
            .filter(DefaultValue.branchId == 13).first()
        #  TODO Quitar branchId quemado cuando funcione la consulta
        # .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 8

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        style_num.leading = 8
        style_num.alignment = TA_RIGHT

        data = [
                   [
                       Paragraph('100505005', style),
                       Paragraph('852', style),
                       Paragraph('BANCO DE OCCIDENTE', style),
                       Paragraph('0,00', style_num),
                       Paragraph('0,00', style_num),
                       Paragraph('15.000,00', style_num)
                   ]
               ] * 100
        # for dct_det in preview_data['document_details']:
        #     det_color = ''
        #     det_size = ''
        #     det_comment = ''
        #     det_siz_col_brake = ''
        #     if dct_det.sizeId is not None:
        #         det_size = '<font size=5>TALLA: {0} </font>'.format(dct_det.size.code)
        #     if dct_det.colorId is not None:
        #         det_color = '<font size=5>COLOR: {0} </font>'.format(dct_det.color.name)
        #     if dct_det.comments is not None:
        #         det_comment = '<br/><font size=5>{0}</font>'.format(dct_det.comments)
        #
        #     if dct_det.sizeId is not None or dct_det.colorId is not None:
        #         det_siz_col_brake = '<br/>'
        #
        #     data.append(
        #         [
        #             Paragraph(dct_det.item.code, style),
        #             Paragraph('{0}{1}{2}{3}{4}'.format(dct_det.item.name,
        #                                                det_siz_col_brake,
        #                                                det_size,
        #                                                det_color,
        #                                                det_comment), style),
        #             Paragraph(dct_det.item.measurementUnit.code, style),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.valueDecimals),
        #                                     _round(dct_det.unitValue, default_decimals.valueDecimals),
        #                                     grouping=True
        #                                     ),
        #                       style=style_num),
        #             # Paragraph(str(_round(dct_det.unitValue, default_decimals.valueDecimals)),
        #             #           style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.quantityDecimals),
        #                                     _round(dct_det.quantity, default_decimals.quantityDecimals),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(2),
        #                                     _round(dct_det.disccount, 2),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(2),
        #                                     _round(dct_det.iva, 2),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.valueDecimals),
        #                                     _round(dct_det.baseValue, default_decimals.valueDecimals),
        #                                     grouping=True),
        #                       style=style_num)
        #         ]
        #     )

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]
        )

        doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        doc.addPageTemplates(
            [
                PageTemplate(
                    id='bodyFrame',
                    frames=[
                        Frame(
                            x1=2.8 * cm,
                            y1=4.6 * cm,
                            width=16 * cm,
                            height=10.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='body',
                            showBoundary=False
                        ),
                    ],
                ),
            ]
        )

        doc.build(
            [Table(
                data,
                [2.1 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )

        return "{0}".format(outfilename)

    @staticmethod
    def make_preview_pdf(preview_data):
        InvoiceImportPreview.preview_data = preview_data
        #  TODO Quitar comentario cuando funcione la consulta
        default_decimals = session.query(DefaultValue.quantityDecimals,
                                         DefaultValue.valueDecimals,
                                         DefaultValue.branchId) \
            .filter(DefaultValue.branchId == 13).first()
        #  TODO Quitar branchId quemado cuando funcione la consulta
            # .filter(DefaultValue.branchId == preview_data['branch_id']).first()

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 8

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        style_num.leading = 8
        style_num.alignment = TA_RIGHT

        data = [
            [
                Paragraph('100505005', style),
                Paragraph('852', style),
                Paragraph('BANCO DE OCCIDENTE', style),
                Paragraph('0,00', style_num),
                Paragraph('0,00', style_num),
                Paragraph('15.000,00', style_num)
            ]
        ]*100
        # for dct_det in preview_data['document_details']:
        #     det_color = ''
        #     det_size = ''
        #     det_comment = ''
        #     det_siz_col_brake = ''
        #     if dct_det.sizeId is not None:
        #         det_size = '<font size=5>TALLA: {0} </font>'.format(dct_det.size.code)
        #     if dct_det.colorId is not None:
        #         det_color = '<font size=5>COLOR: {0} </font>'.format(dct_det.color.name)
        #     if dct_det.comments is not None:
        #         det_comment = '<br/><font size=5>{0}</font>'.format(dct_det.comments)
        #
        #     if dct_det.sizeId is not None or dct_det.colorId is not None:
        #         det_siz_col_brake = '<br/>'
        #
        #     data.append(
        #         [
        #             Paragraph(dct_det.item.code, style),
        #             Paragraph('{0}{1}{2}{3}{4}'.format(dct_det.item.name,
        #                                                det_siz_col_brake,
        #                                                det_size,
        #                                                det_color,
        #                                                det_comment), style),
        #             Paragraph(dct_det.item.measurementUnit.code, style),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.valueDecimals),
        #                                     _round(dct_det.unitValue, default_decimals.valueDecimals),
        #                                     grouping=True
        #                                     ),
        #                       style=style_num),
        #             # Paragraph(str(_round(dct_det.unitValue, default_decimals.valueDecimals)),
        #             #           style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.quantityDecimals),
        #                                     _round(dct_det.quantity, default_decimals.quantityDecimals),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(2),
        #                                     _round(dct_det.disccount, 2),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(2),
        #                                     _round(dct_det.iva, 2),
        #                                     grouping=True),
        #                       style=style_num),
        #             Paragraph(locale.format("%.{0}f".format(default_decimals.valueDecimals),
        #                                     _round(dct_det.baseValue, default_decimals.valueDecimals),
        #                                     grouping=True),
        #                       style=style_num)
        #         ]
        #     )

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]
        )

        doc = BaseDocTemplate(outfilepath, pagesize=portrait(letter))

        doc.addPageTemplates(
            [
                PageTemplate(
                    id='bodyFrame',
                    frames=[
                        Frame(
                            x1=2.8 * cm,
                            y1=4.6 * cm,
                            width=16 * cm,
                            height=10.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='body',
                            showBoundary=False
                        ),
                    ],
                ),
                PageTemplate(
                    id='checkFrame',
                    frames=[
                        Frame(
                            x1=3.7 * cm,
                            y1=23.9 * cm,
                            width=14.5 * cm,
                            height=0.8 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0.4 * cm,
                            id='checkLetters',
                            showBoundary=False
                        ),
                        Frame(
                            x1=3.7 * cm,
                            y1=24.7 * cm,
                            width=14.5 * cm,
                            height=0.7 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0.3 * cm,
                            id='checkTo',
                            showBoundary=False
                        ),
                        Frame(
                            x1=10.4 * cm,
                            y1=25.4 * cm,
                            width=1.3 * cm,
                            height=0.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='checkYear',
                            showBoundary=False
                        ),
                        Frame(
                            x1=11.7 * cm,
                            y1=25.4 * cm,
                            width=1 * cm,
                            height=0.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='checkMonth',
                            showBoundary=False
                        ),
                        Frame(
                            x1=12.7 * cm,
                            y1=25.4 * cm,
                            width=1 * cm,
                            height=0.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='checkDay',
                            showBoundary=False
                        ),
                        Frame(
                            x1=13.7 * cm,
                            y1=25.4 * cm,
                            width=4.5 * cm,
                            height=0.4 * cm,
                            leftPadding=0,
                            bottomPadding=0,
                            rightPadding=0,
                            topPadding=0,
                            id='checkNumber',
                            showBoundary=False
                        ),
                    ],
                ),

            ]
        )

        story = list()
        story.append(Table(
            data,
            [2.1 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
            style=table_style
        ))

        story.append(NextPageTemplate('checkFrame'))
        story.append(PageBreak())

        for i in range(6):
            story.append(Paragraph('DOCIENTOS MIL PESOS COLOMBIANOS', style))
            story.append(FrameBreak())
            story.append(Paragraph('ADRIAN SERNA GOMEZ', style))
            story.append(FrameBreak())
            story.append(Paragraph('2015', style))
            story.append(FrameBreak())
            story.append(Paragraph('11', style))
            story.append(FrameBreak())
            story.append(Paragraph('22', style))
            story.append(FrameBreak())
            story.append(Paragraph('******25,000.00', style_num))

        story.append(NextPageTemplate('bodyFrame'))
        story.append(PageBreak())
        doc.build(
            story,
            canvasmaker=NumberedCanvas
        )

        return "{0}".format(outfilename)

    @staticmethod
    def number_to_text(value):
        num_to_text = ''
        value = math.trunc(value)

        if value == 0:
            num_to_text = 'CERO'
        elif value == 1:
            num_to_text = 'UNO'
        elif value == 2:
            num_to_text = 'DOS'
        elif value == 3:
            num_to_text = 'TRES'
        elif value == 4:
            num_to_text = 'CUATRO'
        elif value == 5:
            num_to_text = 'CINCO'
        elif value == 6:
            num_to_text = 'SEIS'
        elif value == 7:
            num_to_text = 'SIETE'
        elif value == 8:
            num_to_text = 'OCHO'
        elif value == 9:
            num_to_text = 'NUEVE'
        elif value == 10:
            num_to_text = 'DIEZ'
        elif value == 11:
            num_to_text = 'ONCE'
        elif value == 12:
            num_to_text = 'DOCE'
        elif value == 13:
            num_to_text = 'TRECE'
        elif value == 14:
            num_to_text = 'CATORCE'
        elif value == 15:
            num_to_text = 'QUINCE'
        elif value < 20:
            num_to_text = 'DIECI{0}'.format(InvoiceImportPreview.number_to_text(value - 10))
        elif value == 20:
            num_to_text = 'VEINTE'
        elif value < 30:
            segunda_cifra = ''
            if value % 20 == 1:
                segunda_cifra = 'UN'
            else:
                segunda_cifra = InvoiceImportPreview.number_to_text(value % 20)

            num_to_text = 'VEINTI{0}'.format(segunda_cifra)
        elif value == 30:
            num_to_text = 'TREINTA'
        elif value == 40:
            num_to_text = 'CUARENTA'
        elif value == 50:
            num_to_text = 'CINCUENTA'
        elif value == 60:
            num_to_text = 'SESENTA'
        elif value == 70:
            num_to_text = 'SETENTA'
        elif value == 80:
            num_to_text = 'OCHENTA'
        elif value == 90:
            num_to_text = 'NOVENTA'
        elif value < 100:
            segunda_cifra = ''
            if value % 10 == 1:
                segunda_cifra = 'UN'
            else:
                segunda_cifra = InvoiceImportPreview.number_to_text(value % 10)

            num_to_text = '{0} Y {1}'.format(InvoiceImportPreview.number_to_text(math.trunc(value / 10) * 10),
                                             segunda_cifra)

        elif value == 100:
            num_to_text = 'CIEN'
        elif value < 200:
            num_to_text = 'CIENTO {0}'.format(InvoiceImportPreview.number_to_text(value - 100))
        elif value == 200 or value == 300 or value == 400 or value == 600 or value == 800:
            num_to_text = '{0}CIENTOS'.format(InvoiceImportPreview.number_to_text(value / 100))
        elif value == 500:
            num_to_text = 'QUINIENTOS'
        elif value == 700:
            num_to_text = 'SETECIENTOS'
        elif value == 900:
            num_to_text = 'NOVECIENTOS'
        elif value < 1000:
            num_to_text = '{0} {1}'.format(InvoiceImportPreview.number_to_text(math.trunc(value / 100) * 100),
                                          InvoiceImportPreview.number_to_text(value % 100))
        elif value == 1000:
            num_to_text = 'MIL'
        elif value < 2000:
            num_to_text = 'MIL {0}'.format(InvoiceImportPreview.number_to_text(value % 1000))
        elif value < 1000000:
            num_to_text = '{0} MIL'.format(InvoiceImportPreview.number_to_text(value / 1000))
            if value % 1000 > 0:
                num_to_text = '{0} {1}'.format(num_to_text, InvoiceImportPreview.number_to_text(value % 1000))
        elif value == 1000000:
            num_to_text = 'UN MILLÓN'
        elif value < 2000000:
            num_to_text = 'UN MILLÓN {0}'.format(InvoiceImportPreview.number_to_text(value % 1000000))
        elif value < 1000000000000:
            num_to_text = '{0} MILLONES'.format(InvoiceImportPreview.number_to_text(math.trunc(value / 1000000)))
            if (value - math.trunc(value / 1000000) * 1000000) > 0:
                num_to_text = '{0} {1}'.format(num_to_text,
                                              InvoiceImportPreview.number_to_text(value - math.trunc(value / 1000000) * 1000000))
        elif value == 1000000000000:
            num_to_text = 'UN BILLÓN'
        elif value < 2000000000000:
            num_to_text = 'UN BILLÓN {0}'.format(InvoiceImportPreview.number_to_text(value - (math.trunc(value / 1000000000000) * 1000000000000)))
        else:
            num_to_text = '{0} BILLONES'.format(InvoiceImportPreview.number_to_text(math.trunc(value / 1000000000000)))
            if (value - math.trunc(value / 1000000000000) * 1000000000000) > 0:
                num_to_text = '{0} {1}'.format(num_to_text,
                                              InvoiceImportPreview.number_to_text(value - math.trunc(value / 1000000000000) * 1000000000000))
        return num_to_text

    @staticmethod
    def total_to_letter(total, currency, post_fijo_monto_letras):
        cantidad = Decimal(total)
        entero = int(math.trunc(cantidad))
        decimales = int(_round((cantidad - entero) * 100, 2))
        dec = 'CON {0}/100'.format(InvoiceImportPreview.fill_from_left(str(decimales), '0', 2))
        res = '{0} '.format(InvoiceImportPreview.number_to_text(Decimal(entero)))
        if not(entero == 0):
            if (entero % 1000000) == 0:
                res = '{0} DE '.format(res)

        res = '{0} {1} {2} {3}'.format(res, InvoiceImportPreview.get_currency(currency.upper()), dec, post_fijo_monto_letras.upper())
        return res

    @staticmethod
    def fill_from_left(strg, fill, size):
        filled_string = strg
        while len(filled_string) < size:
            filled_string = '{0}{1}'.format(fill, filled_string)
        return filled_string

    @staticmethod
    def get_currency(currency):
        curr = currency.split()

        if len(curr):
            for idx, c in enumerate(curr):
                if c[-1] == 'A' or c[-1] == 'E' or c[-1] == 'I' or c[-1] == 'O' or c[-1] == 'U':
                    curr[idx] = '{0}S'.format(curr[idx])
                else:
                    curr[idx] = '{0}ES'.format(curr[idx])

        return ' '.join(curr)
