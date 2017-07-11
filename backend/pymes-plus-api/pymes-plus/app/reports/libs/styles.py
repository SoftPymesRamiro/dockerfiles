from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold')

style_p_normal = ParagraphStyle('Normal')
style_p_normal.fontName = 'Arial'
style_p_normal.fontSize = 8
style_p_normal.leading = 8

style_p_normal_centred = ParagraphStyle('Normal')
style_p_normal_centred.fontName = 'Arial'
style_p_normal_centred.fontSize = 8
style_p_normal_centred.leading = 8
style_p_normal_centred.alignment = TA_CENTER

style_p_normal_right = ParagraphStyle('Normal')
style_p_normal_right.fontName = 'Arial'
style_p_normal_right.fontSize = 8
style_p_normal_right.leading = 8
style_p_normal_right.alignment = TA_RIGHT

style_p_header = ParagraphStyle('Normal')
style_p_header.fontName = 'Arial'
style_p_header.fontSize = 12
style_p_header.leading = 12
style_p_header.rightIndent = 2.8 * cm
style_p_header.leftIndent = 2.8 * cm
style_p_header.alignment = TA_CENTER

style_p_sub_header = ParagraphStyle('Normal')
style_p_sub_header.fontName = 'Arial'
style_p_sub_header.fontSize = 10
style_p_sub_header.leading = 10
style_p_sub_header.rightIndent = 2.8 * cm
style_p_sub_header.leftIndent = 2.8 * cm
style_p_sub_header.alignment = TA_CENTER

style_p_sub_header_medium = ParagraphStyle('Normal')
style_p_sub_header_medium.fontName = 'Arial'
style_p_sub_header_medium.fontSize = 9.5
style_p_sub_header_medium.leading = 9.5
style_p_sub_header_medium.alignment = TA_CENTER

style_p_header_small = ParagraphStyle('Normal')
style_p_header_small.fontName = 'Arial'
style_p_header_small.fontSize = 7
style_p_header_small.leading = 7

