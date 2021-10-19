from fpdf import FPDF, HTMLMixin
class HTML2PDF(FPDF, HTMLMixin):
    pass
def html2pdf():
    html = '''<h1 align="center">PyFPDF HTML Demo</h1>
    <p>This is regular text mr sandy</p>
    <p>You can also <b>bold</b>, <i>italicize</i> or <u>underline</u>
    '''
    html2 = '''<p>sandy</p>'''
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.write_html(html2)
    pdf.output('html2pdf.pdf')
    
if __name__ == '__main__':
    html2pdf()