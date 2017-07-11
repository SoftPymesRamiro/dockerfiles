from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, FrameBreak, KeepTogether, NextPageTemplate, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.colors import Color
import os
import uuid
from ....utils.math_ext import _round
from ....utils.converters import total_to_letter, format_decimal_values
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
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_page_footer_n_header(num_pages, i)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_footer_n_header(self, page_count, current_page):
        """
        draw page footer and page header if the file is on the last page also draw the total of the document
        :param page_count:
        :return:
        """
        preview_data = AdvanceThirdPreviewF.preview_data

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
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 1)),
            ]
        )

        table_style_header_general = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('TOPPADDING', (0, 0), (-1, -1), 0.05 * cm),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.1 * cm),
                ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ('SPAN', (0, 5), (1, 5)),
                # ('BACKGROUND', (2, 0), (-2, 4), (0, 0, 1)),
                # ('SPAN', (2, 0), (-2, 3)),
                # ('SPAN', (-1, 0), (-1, 3)),
                # ('SPAN', (2, 4), (-1, 5)),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 1)),
                ('LINEABOVE', (3, -1), (-1, -1), 1, (0, 0, 0)),
                # ('BACKGROUND', (3, 0), (-1, -2), (0, 0, 1)),
                ('VALIGN', (3, 0), (-1, -2), 'TOP'),
                ('VALIGN', (-2, -2), (-1, -1), 'TOP'),
                ('VALIGN', (0, 4), (1, 5), 'TOP')
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
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 1)),
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
                ('LINEBEFORE', (1, 1), (-1, -1), 1, (0, 0, 0)),
                ('LINEABOVE', (0, 1), (-1, -2), 1, (0, 0, 0)),
                ('SPAN', (0, 0), (-1, 0)),
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
            preview_data = AdvanceThirdPreviewF.preview_data['checkBook'][0]

            # INFORMACION PRINCIPAL - INICIO --------------------------------------------------------------------------

            p_comp = Paragraph('<b>COMPROBANTE DE EGRESO No </b>', style_p_header_provider)
            p_comp.wrap(14.5 * cm, 2 * cm)
            p_comp.drawOn(cnv, 2.8 * cm, 15 * cm)

            p_comp_num = Paragraph(preview_data['Comprobante_N'], style_p_header_provider)
            p_comp_num.wrap(14.5 * cm, 2 * cm)
            p_comp_num.drawOn(cnv, 7.5 * cm, 15 * cm)

            p_anti = Paragraph('<b>ANTICIPO A TERCERO No </b>',
                               style_p_header_provider)
            p_anti.wrap(14.5 * cm, 2 * cm)
            p_anti.drawOn(cnv, 2.8 * cm, 14.5 * cm)

            p_anti_num = Paragraph(preview_data['DocNum'], style_p_header_provider)
            p_anti_num.wrap(14.5 * cm, 2 * cm)
            p_anti_num.drawOn(cnv, 7.5 * cm, 14.5 * cm)


            # Validacion para llenar el campo CHEQUE/DOC N que corresponde a la informacion de cada cheque
            check_doc = ''
            if current_page > 0 or page_count == 1:
                check = AdvanceThirdPreviewF.preview_data['checkBook'][current_page-1]
                check_doc = '{0} {1} {2}'.format(check['PrefixCheck'] if check['PrefixCheck']
                                                 else '', check['DocNumCheque'], check['Financial_Entity'])

            p_cheque = Paragraph('<b>CHEQUE/DOC No </b>', style_p_header_provider)
            p_cheque.wrap(14.5 * cm, 2 * cm)
            p_cheque.drawOn(cnv, 2.8 * cm, 14 * cm)

            p_cheque_num = Paragraph(check_doc, style_p_header_provider)
            p_cheque_num.wrap(14.5 * cm, 2 * cm)
            p_cheque_num.drawOn(cnv, 7.5 * cm, 14 * cm)

            third = ''
            identification = ''
            if preview_data['CC_Third'] is None:
                third = preview_data['Employee_Name'] or preview_data['Beneficiary']
                identification = '{0}-{1}'.format('{:,}'.format(int(preview_data['Employee_IdentificationNumber'])),
                                                  preview_data['Employee_IdentificationDV'])
            else:
                identification = '{0}-{1}'.format('{:,}'.format(int(preview_data['CC_Third'])),
                                                  preview_data['IdentificationDVThird'])
                if preview_data['TradeName']:
                    third = preview_data['Beneficiary'] or preview_data['TradeName']
                else:
                    third = (preview_data['LastName']+' ' if preview_data['LastName'] else preview_data['LastName'] + ' ') \
                            + (preview_data['MaidenName']+' ' if preview_data['MaidenName'] else preview_data['MaidenName'] + ' ') \
                            + (preview_data['FirstName']+' ' if preview_data['FirstName'] else preview_data['FirstName'] + ' ') \
                            + (preview_data['SecondName'])

            p_giro = Paragraph('<b>GIRO A </b>', style_p_header_provider)
            p_giro.wrap(14.5 * cm, 2 * cm)
            p_giro.drawOn(cnv, 2.8 * cm, 13.5 * cm)

            # p_giro_num = Paragraph(third, style_p_header_provider)
            p_giro_num = Paragraph(paragraph_over_flow(
                text=third,
                width=10,
                font_size=8,
                leading=8), style_p_header_provider)
            p_giro_num.wrap(14.5 * cm, 2 * cm)
            p_giro_num.drawOn(cnv, 7.5 * cm, 13.5 * cm)

            p_user = Paragraph('<b>ELABORADO POR </b>', style_p_header_provider)
            p_user.wrap(14.5 * cm, 2 * cm)
            p_user.drawOn(cnv, 2.8 * cm, 12 * cm)

            p_user_value = Paragraph(preview_data['CreatedBy'].upper(), style_p_header_provider)
            p_user_value.wrap(14.5 * cm, 2 * cm)
            p_user_value.drawOn(cnv, 7.5 * cm, 12 * cm)


            # INFORMACION PRINCIPAL - FIN -----------------------------------------------------------------------------


            # ANULADO -------------------------------------------------------------------------------------------------
            if preview_data['Annuled']:
                # paragraph_annuled = Paragraph('ANULADO', style_p_annuled)
                # paragraph_annuled.wrap(10 * cm, 2.6 * cm)
                # paragraph_annuled.drawOn(cnv, 7 * cm, 20 * cm)
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
            # cnv.restoreState()

        def header(cnv, current_page, page_count):
            cnv.saveState()

            preview_header = AdvanceThirdPreviewF.preview_data['checkBook'][0]
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
                default_decimals = AdvanceThirdPreviewF.preview_data['checkBook'][0]['ValueDecimals']
                p_titular = Paragraph(preview_header['Beneficiary'] if not preview_header['Beneficiary'] is None else ''
                                      , style_p_header_provider)

                p_titular.wrap(14.5 * cm, 2 * cm)
                p_titular.drawOn(cnv, 3.7 * cm, 24.7 * cm)

                p_total_letras = Paragraph(total_to_letter(preview_header['Cheque'] if preview_header['Cheque'] else 0,
                                                           preview_header['Currency'], 'M/L'), style_p_header_provider)

                p_total_letras.wrap(14.5 * cm, 2 * cm)
                p_total_letras.drawOn(cnv, 3.7 * cm, 23.9 * cm)

                p_ano = Paragraph(str(preview_header['Fecha_Cheque'].year) if not preview_header['Fecha_Cheque'] is None
                                  else '', style_p_header_provider)

                p_ano.wrap(14.5 * cm, 2 * cm)
                p_ano.drawOn(cnv, 10.4 * cm, 25.4 * cm)

                p_mes = Paragraph(str(preview_header['Fecha_Cheque'].month) if not preview_header['Fecha_Cheque'] is None
                                  else '', style_p_header_provider)

                p_mes.wrap(14.5 * cm, 2 * cm)
                p_mes.drawOn(cnv, 11.8 * cm, 25.4 * cm)

                p_dia = Paragraph(str(preview_header['Fecha_Cheque'].day) if not preview_header['Fecha_Cheque'] is None
                                  else '', style_p_header_provider)

                p_dia.wrap(14.5 * cm, 2 * cm)
                p_dia.drawOn(cnv, 12.8 * cm, 25.4 * cm)

                p_total_numeros = Paragraph(
                    "{0}{1}".format('******', '{:20,.{}f}'.format(_round(preview_header['Cheque'] if
                                                                         not preview_header['Cheque'] is None
                                                                         else 0, default_decimals), default_decimals)),
                                    style_p_header_provider)

                p_total_numeros.wrap(14.5 * cm, 2 * cm)
                p_total_numeros.drawOn(cnv, 15.9 * cm, 25.4 * cm)

            # CHEQUE --------------------------------------------------------------------------------------------------

            cnv.restoreState()

        footer(self)
        header(self, current_page, page_count)


class AdvanceThirdPreviewF:
    preview_data = None

    @staticmethod
    def make_same_page_preview_pdf(preview_data):
        AdvanceThirdPreviewF.preview_data = preview_data
        default_decimals = AdvanceThirdPreviewF.preview_data['checkBook'][0]['ValueDecimals']

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')
        style_num_cero = ParagraphStyle('Normal')
        style_cta = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 8

        #estilo cta sub aux
        style_cta.fontName = 'Arial'
        style_cta.fontSize = 8
        style_cta.leading = 8
        style_cta.alignment = TA_CENTER

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        style_num.leading = 8
        style_num.alignment = TA_RIGHT

        #estilo cuando los detalles son  cero
        style_num_cero.fontName = 'Arial'
        style_num_cero.fontSize = 8
        style_num_cero.leading = 8
        style_num_cero.alignment = TA_CENTER

        data = []
        for dct_det in AdvanceThirdPreviewF.preview_data['info']:
            data.append([
                # Paragraph('', style),

                Paragraph("{0} {1} {2}".format(dct_det['CTA'], dct_det['SUB'], dct_det['AUX']), style),
                # Paragraph(dct_det['CTA'], style_cta),
                # Paragraph(dct_det['SUB'], style_cta),
                # Paragraph(dct_det['AUX'], style_cta),
                Paragraph(dct_det['CrossDocument'], style),
                Paragraph(dct_det['Name'], style),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['DEBITO'], default_decimals), default_decimals),
                          style_num),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['CREDITO'], default_decimals), default_decimals),
                          style_num)
            ])
        # Si no trae detalles se carga por defecto en vacio. (Esto pasa cuando es anulado el documento)

        if len(data) == 0:
            data.append([
                Paragraph('', style),
                Paragraph('', style),
                Paragraph('', style),
                Paragraph('0', style_num_cero),
                Paragraph('0', style_num_cero)
            ])

        table_style = TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('GRID', (0, 0), (-1, -1), 1, (0, 0, 1))
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
                            y1=10 * cm,
                            width=16 * cm,
                            height=10 * cm,
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
                [2.1 * cm, 2.8 * cm, 4.5 * cm, 3.8 * cm, 2.8 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )

        return "{0}".format(outfilename)

