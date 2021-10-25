#require: pip install python-dateutil 

import sys
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
today = datetime.today()
this_y = str(today.year)
this_m = str(today.month)
one_month_before  = today - relativedelta(months=1)
last_y = str(one_month_before.year)
last_m = str(one_month_before.month)
lastday = str(calendar.monthrange(int(this_y), int(this_m))[1])
if len(last_y) == 1:
  last_y = '0' + last_y
if len(last_m) == 1:
  last_m = '0' + last_m

# ファイルの指定
# 既存のテンプレートPDF
template_file = '/home/ubuntu/scripts/業務完了報告書_雛形.pdf' 
# 完成したPDFの保存先
output_file = '/home/ubuntu/scripts/業務完了報告書.pdf'
# 一時ファイル
tmp_file = '/***.pdf' 
# A4縦のCanvasを作成 -- (*1)
w, h = portrait(A4)
cv = canvas.Canvas(tmp_file, pagesize=(w, h))

# フォントを登録しCanvasに設定 --- (*2)
font_size = 10
pdfmetrics.registerFont(TTFont('msgothic', '/***/msgothic.ttc'))
cv.setFont('msgothic', font_size)
cv.drawString(150.8*mm, h-18.7*mm, this_y)
cv.drawString(163.6*mm, h-18.7*mm, this_m)
cv.drawString(172*mm, h-18.7*mm, str(today.day))
#---------------------------------------------------^part1-------------------------
cv.drawString(55*mm, h-71.3*mm, this_y)
cv.drawString(65.3*mm, h-71.3*mm, this_m)
cv.drawString(72.5*mm, h-71.3*mm, str(today.day))
#---------------------------------------------------^part2-------------------------
cv.drawString(116.5*mm, h-211*mm, last_y)
cv.drawString(128.6*mm, h-211*mm, last_m)
#---------------------------------------------------^part3.1-------------------------
cv.drawString(152*mm, h-211*mm, this_y)
cv.drawString(163.7*mm, h-211*mm, this_m)
cv.drawString(172.5*mm, h-211*mm, lastday)
#---------------------------------------------------^part3.2-------------------------

# 一時ファイルに保存 --- (*4)
cv.showPage()
cv.save()

# テンプレートとなるPDFを読む --- (*5)
template_pdf = PdfFileReader(template_file)
template_page = template_pdf.getPage(0)

# 一時ファイルを読んで合成する --- (*6)
tmp_pdf = PdfFileReader(tmp_file)
template_page.mergePage(tmp_pdf.getPage(0))

# 書き込み先PDFを用意 --- (*7)
output = PdfFileWriter()
output.addPage(template_page)
with open(output_file, "wb") as fp:
  output.write(fp)
