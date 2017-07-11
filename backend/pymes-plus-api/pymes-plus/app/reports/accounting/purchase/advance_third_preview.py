from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, BaseDocTemplate, PageTemplate, TableStyle, FrameBreak, KeepTogether, NextPageTemplate, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER,TA_JUSTIFY
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
        preview_data = AdvanceThirdPreview.preview_data

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
            preview_data = AdvanceThirdPreview.preview_data['checkBook'][0]
            # INFORMACIÓN DEL FIRMA -----------------------------------------------------------------------------------

            par_comments = paragraph_over_flow_height(text=preview_data['Comments'].capitalize(),
                                                      width=13,
                                                      no_par=5,
                                                      font_size=8,
                                                      leading=8)

            data_footer_sing = [
                [
                  Paragraph("<b>Observaciones:</b> {0}".format(par_comments),
                            style_p_footer_left)
                ],
                [
                    Paragraph('Elaborado por', style_p_footer_left),
                    Paragraph('Autorizado por', style_p_footer_left),
                    Paragraph('Revisado por', style_p_footer_left),
                    Paragraph('Recibido', style_p_footer_left),
                ],
                [
                    Paragraph(preview_data['CreatedBy'].title(), style_p_footer_left),
                    '',
                    '',
                    Paragraph('Firma y Sello - CC ó NIT', style_p_footer_centred),
                ]
            ]

            # Tabla con datos de despacho
            table_footer_sing = Table(
                data_footer_sing,  # Contenido de la tabla
                [3.8 * cm, 3.6 * cm, 3.6 * cm, 5 * cm],  # Ancho de las columnas
                [1 * cm, 0.5 * cm, 0.7 * cm],
                style=table_style_footer_sing  # Estilos de la tabla
            )

            # Denota el contenor de la tabla
            table_footer_sing.wrap(16 * cm, 1.2 * cm)
            # Dibuja la tabla en las coordenadas indicadas
            table_footer_sing.drawOn(cnv, 2.8 * cm, 3.4 * cm)

            # INFORMACIÓN DEL FIRMA - FIN -----------------------------------------------------------------------------
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


        def header(cnv, current_page, page_count):
            cnv.saveState()

            preview_header = AdvanceThirdPreview.preview_data['checkBook'][0]
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
                default_decimals = AdvanceThirdPreview.preview_data['checkBook'][0]['ValueDecimals']
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
                        Paragraph("<b>{0} - {1}</b>".format(preview_header['Comp_Name'], preview_header['Branch_Name']),
                                  style_p_header_provider),
                        Paragraph('<b>COMPROBANTE DE EGRESO Nº</b>', style_p_header_provider),
                        Paragraph("<b>{0}</b>".format(preview_header['Comprobante_N']), style_p_header_provider)
                    ],
                    [
                        Paragraph('<b>NIT:   {0}-{1}</b>'.format('{:,}'.format(int(preview_header['CC_Comp'])),
                                                                 preview_header['IdentificationDVComp']),
                                  style_p_header_provider),
                        Paragraph('{0} Nº'.format('DESEMBOLSO A FONDO/CAJA MENOR' if preview_header['ShortWord'] == 'DS'
                                                  else preview_header['Nombre_Documento']), style_p_header_provider),
                        Paragraph(preview_header['DocNum'], style_p_header_provider)
                    ]
                ],
                [9 * cm, 4.6 * cm, 2.4 * cm],
                [0.4 * cm, 0.6 * cm],
                style=table_style_header
            )
            table_header_data.wrap(14.5 * cm, 2 * cm)
            table_header_data.drawOn(cnv, 2.8 * cm, 18.3 * cm)

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL - FIN -----------------------------------------------------

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL -----------------------------------------------------------
            # paymentMet = '<br/><br/><b>TOTAL</b>'
            # paymentMetValue = '<br/>{0}<br/>'.format(format_decimal_values(preview_header['Total'],
            #                                                                preview_header['ValueDecimals']))paymentMet = '<br/><br/><b>TOTAL</b>'
            paymentMet = ''
            paymentMetValue = ''
            total_payment = '<b>TOTAL</b>'
            total_payment_value = '${0}'.format(format_decimal_values(preview_header['Total'],
                                                                     preview_header['ValueDecimals']))
            total_check_str = ''
            total_cash_str = ''
            total_credit_str = ''
            total_transfer_str = ''
            total_gift_str = ''
            sum_checks = ''
            sum_cash = ''
            sum_credit = ''
            sum_transfer = ''
            sum_gift = ''
            total = ''
            decimals = ''

            if self._pageNumber == 1:
                total_headers = AdvanceThirdPreview.preview_data['checkBook']
                sum_checks = sum(c['Cheque'] for c in total_headers)
                sum_cash = sum(c['Efectivo'] for c in total_headers)
                sum_credit = sum(c['Tarjeta_Credito'] for c in total_headers)
                sum_transfer = sum(c['Transferencia'] for c in total_headers)
                sum_gift = sum(c['Bono'] for c in total_headers)
                total = preview_header['Total']
                decimals = preview_header['ValueDecimals']

                total_check_str = '<b>CHEQUE</b>'
                total_cash_str = '<b>EFECTIVO</b>'
                total_credit_str = '<b>TARJETA DE CRÉDITO</b>'
                total_transfer_str = '<b>TRANSFERENCIA</b>'
                total_gift_str = '<b>BONOS</b>'

                paymentMet = '<b>CHEQUE</b> <br/> <b>EFECTIVO</b> <br/> <b>TARJETA DE CRÉDITO</b> <br/> ' \
                             '<b>TRANSFERENCIA</b> <br/> <b>BONOS</b> <br/><br/>'
                paymentMetValue = '{0} <br/> {1} <br/> {2} <br/> {3} <br/> {4} <br/>'.format(
                    format_decimal_values(sum_checks, decimals), format_decimal_values(sum_cash, decimals),
                    format_decimal_values(sum_credit, decimals), format_decimal_values(sum_transfer, decimals),
                    format_decimal_values(sum_gift, decimals)
                )

            third = ''
            identification = ''
            if preview_header['CC_Third'] is None:
                third = preview_header['Employee_Name'] or preview_header['Beneficiary']
                identification = '{0}-{1}'.format('{:,}'.format(int(preview_header['Employee_IdentificationNumber'])),
                                                  preview_header['Employee_IdentificationDV'])
            else:
                identification = '{0}-{1}'.format('{:,}'.format(int(preview_header['CC_Third'])),
                                                  preview_header['IdentificationDVThird'])
                if preview_header['TradeName']:
                    third = preview_header['Beneficiary'] or preview_header['TradeName']
                else:
                    third = (preview_header['LastName']+' ' if preview_header['LastName'] else preview_header['LastName'] + ' ') \
                            + (preview_header['MaidenName']+' ' if preview_header['MaidenName'] else preview_header['MaidenName'] + ' ') \
                            + (preview_header['FirstName']+' ' if preview_header['FirstName'] else preview_header['FirstName'] + ' ') \
                            + (preview_header['SecondName'])

            # Validacion para llenar el campo CHEQUE/DOC N que corresponde a la informacion de cada cheque
            check_doc = ''
            if current_page > 0 or page_count == 1:
                check = AdvanceThirdPreview.preview_data['checkBook'][current_page-1]
                check_doc = '{0} {1} {2}'.format(check['PrefixCheck'] if check['PrefixCheck']
                                                 else '', check['DocNumCheque'], check['Financial_Entity'])
            table_header_provider = Table(
                [
                    [
                        Paragraph('<b>FECHA</b>', style_p_header_provider),
                        Paragraph(preview_header['DocumentDate'].strftime('%d %b. %Y').upper(), style_p_header_provider),
                        # Paragraph(paymentMet, style_p_header_provider),
                        Paragraph(total_check_str, style_p_header_provider),
                        # Paragraph(paymentMetValue, style_p_header_calc)
                        Paragraph('' if sum_checks == '' else format_decimal_values(sum_checks, decimals),
                                  style_p_header_calc)
                    ],
                    [
                        Paragraph('<b>PAGADO A</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=third, width=6, font_size=8, leading=8),
                                  style_p_header_provider),
                        Paragraph(total_cash_str, style_p_header_provider),
                        Paragraph('' if sum_cash == '' else format_decimal_values(sum_cash, decimals),
                                  style_p_header_calc)
                    ],
                    [
                        Paragraph('<b>CC ó NIT</b>', style_p_header_provider),
                        Paragraph(identification, style_p_header_provider),
                        Paragraph(total_credit_str, style_p_header_provider),
                        Paragraph('' if sum_credit == '' else format_decimal_values(sum_credit, decimals),
                                  style_p_header_calc)
                    ],
                    [
                        Paragraph('<b>CHEQUE/DOC N</b>', style_p_header_provider),
                        Paragraph(paragraph_over_flow(text=check_doc, width=6, font_size=8, leading=8),
                                  style_p_header_provider),
                        Paragraph(total_transfer_str, style_p_header_provider),
                        Paragraph('' if sum_transfer == '' else format_decimal_values(sum_transfer, decimals),
                                  style_p_header_calc)
                    ],
                    [
                        '',
                        '',
                        Paragraph(total_gift_str, style_p_header_provider),
                        Paragraph('' if sum_gift == '' else format_decimal_values(sum_gift, decimals),
                                  style_p_header_calc)
                    ],
                    [
                        Paragraph("<b>SON:</b> {0}".format(total_to_letter(preview_header['Total'],
                                                                           preview_header['Currency'], 'M/L')),
                                  style_p_header_provider),
                        '',
                        Paragraph(total_payment, style_p_header_provider),
                        Paragraph(total_payment_value, style_p_header_calc)
                    ],
                ],
                [2.6 * cm, 7 * cm, 3.4 * cm, 3 * cm],
                [0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.8 * cm],
                style=table_style_header_general
            )
            table_header_provider.wrap(14.5 * cm, 2 * cm)
            table_header_provider.drawOn(cnv, 2.8 * cm, 15.5 * cm)

            # INFORMACION DE LA TABLA INFORMACION PRINCIPAL - FIN -----------------------------------------------------

            # INFORMACION DE LA TABLA DESCRIPTION ---------------------------------------------------------------------

            table_header_description = Table(
                [
                    [
                        Paragraph('<b>CTA SUB AUX</b>', style_p_sub_header_centred),
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
        header(self, current_page, page_count)


class AdvanceThirdPreview:
    preview_data = None

    @staticmethod
    def make_same_page_preview_pdf(preview_data):
        AdvanceThirdPreview.preview_data = preview_data
        default_decimals = AdvanceThirdPreview.preview_data['checkBook'][0]['ValueDecimals']

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
        for dct_det in AdvanceThirdPreview.preview_data['info']:
            data.append([
                Paragraph("{0} {1} {2}".format(dct_det['CTA'], dct_det['SUB'], dct_det['AUX']), style),
                # Paragraph(dct_det['CTA'], style_cta),
                # Paragraph(dct_det['SUB'], style_cta),
                # Paragraph(dct_det['AUX'], style_cta),
                Paragraph(dct_det['CrossDocument'], style),
                Paragraph(dct_det['Name'], style),
                Paragraph(
                    '{:20,.{}f}'.format(_round(dct_det['Percentage'], default_decimals), default_decimals), style_num),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['DEBITO'], default_decimals), default_decimals),
                          style_num),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['CREDITO'], default_decimals), default_decimals),
                          style_num)
            ])
        # Si no trae detalles se carga por defecto en vacio. (Esto pasa cuando es anulado el documento)

        if len(data) == 0:
            data.append([
                Paragraph(' ', style),
                Paragraph(' ', style),
                Paragraph(' ', style),
                Paragraph('0', style_num_cero),
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
                            y1=5 * cm,
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
                # [0.7 * cm, 0.7 * cm, 0.7 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
                [2.1 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
                style=table_style
            )],
            canvasmaker=NumberedCanvas
        )

        return "{0}".format(outfilename)

    @staticmethod
    def make_preview_pdf(preview_data):
        AdvanceThirdPreview.preview_data = preview_data
        default_decimals = AdvanceThirdPreview.preview_data['checkBook'][0]['ValueDecimals']

        outfilename = "{0}.pdf".format(uuid.uuid1())
        outfiledir = os.getcwd().replace('pymes-plus-api/pymes-plus', 'WebClient/assets/documents')
        outfilepath = os.path.join(outfiledir, outfilename)

        style = ParagraphStyle('Normal')
        style_num = ParagraphStyle('Normal')
        style_cta = ParagraphStyle('Normal')

        style.fontName = 'Arial'
        style.fontSize = 8
        style.leading = 8

        # estilo cta sub aux
        style_cta.fontName = 'Arial'
        style_cta.fontSize = 8
        style_cta.leading = 8
        style_cta.alignment = TA_CENTER

        style_num.fontName = 'Arial'
        style_num.fontSize = 8
        style_num.leading = 8
        style_num.alignment = TA_RIGHT

        data = []
        for dct_det in AdvanceThirdPreview.preview_data['info']:
            data.append([
                Paragraph("{0}  {1}  {2}".format(dct_det['CTA'], dct_det['SUB'], dct_det['AUX']), style),
                # Paragraph(dct_det['CTA'], style_cta),
                # Paragraph(dct_det['SUB'], style_cta),
                # Paragraph(dct_det['AUX'], style_cta),
                Paragraph(dct_det['CrossDocument'], style),
                Paragraph(dct_det['Name'], style),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['Percentage'], default_decimals), default_decimals),
                          style_num),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['DEBITO'], default_decimals), default_decimals),
                          style_num),
                Paragraph('{:20,.{}f}'.format(_round(dct_det['CREDITO'], default_decimals), default_decimals),
                          style_num)
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
                            y1=5 * cm,
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
            # [0.7 * cm, 0.7 * cm, 0.7 * cm, 2.8 * cm, 4.5 * cm, 1.2 * cm, 2.6 * cm, 2.8 * cm],
            style=table_style
        ))

        story.append(NextPageTemplate('checkFrame'))
        story.append(PageBreak())

        check_books = preview_data['checkBook']
        for i in check_books:
            story.append(Paragraph(total_to_letter(i['Cheque'], i['Currency'], 'M/L'), style))
            story.append(FrameBreak())
            story.append(Paragraph(i['Beneficiary'] if not i['Beneficiary'] is None else '', style))
            story.append(FrameBreak())
            story.append(Paragraph(str(i['Fecha_Cheque'].year) if not i['Fecha_Cheque'] is None else '', style))
            story.append(FrameBreak())
            story.append(Paragraph(str(i['Fecha_Cheque'].month) if not i['Fecha_Cheque'] is None else '', style))
            story.append(FrameBreak())
            story.append(Paragraph(str(i['Fecha_Cheque'].day) if not i['Fecha_Cheque'] is None else '', style))
            story.append(FrameBreak())
            story.append(Paragraph("{0}{1}".format('******', '{:20,.{}f}'.format(
                _round(i['Cheque'] if not i['Cheque'] is None else 0, default_decimals), default_decimals)), style_num))

        story.append(NextPageTemplate('bodyFrame'))
        story.append(PageBreak())
        doc.build(
            story,
            canvasmaker=NumberedCanvas
        )

        return "{0}".format(outfilename)
