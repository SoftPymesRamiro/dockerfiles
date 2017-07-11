from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import cm


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