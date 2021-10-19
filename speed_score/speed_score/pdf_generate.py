import sys
import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

args              = sys.argv
user_company      = args[1]
result            = args[2]
user_id           = args[3]
collect_type      = args[4]
column            = args[5]
row               = args[6]
deadline          = args[7]
url               = args[8]

detail            = row + "/" + column
date              = datetime.datetime.now()
today             = str(date.year) + '/' + str(date.month) + '/' + str(date.day)
deadline          = str(deadline.replace('-', '/'))

if len(user_id)   < 5 :
	id_number       = user_id.rjust(4, "0")
elif len(user_id) >= 5:
	id_number       = user_id.rjust(len(user_id)+1, "0")

if collect_type   == "一回きりの収集":
	temp_result     = int(result)
else:
	temp_result       = int(result) + 200000
sum_result        = temp_result*1.1
tax               = temp_result*0.1
sum_result        = str(sum_result)
tax               = str(tax)
temp_result       = str(temp_result)
result            = str(result)
n                 = len(result)

if n              == 6:
	tax           = "￥" + tax[:2] + ",000"
	sum_result    = "￥" + sum_result[:3] + ",000"
	temp_result   = "￥" + temp_result[:2] + "0,000"
	result        = "￥" + result[:2] + "0,000"

elif n            == 7:
	tax           = "￥" + tax[:3] + ",000"
	sum_result    = "￥" + sum_result[0] + "," + sum_result[1:4] + ",000"
	temp_result   = "￥" + temp_result[0] + "," + temp_result[1:4] + ",000"
	result        = "￥" + result[0] + "," + result[1:4] + ",000"

file_id           = "PIG-AUT " + str(date.year)[2:] + "-" + id_number

# ファイルの指定
# 既存のテンプレートPDF
if collect_type   == "一回きりの収集":
	template_file     = '/srv/www/public_html/speed_score/speed_score/見積書_雛形.pdf' 
else:
	template_file     = '/srv/www/public_html/speed_score/speed_score/見積書_雛形_options.pdf' 
# 完成したPDFの保存先
output_file       = '/srv/www/public_html/speed_score/speed_score/見積書_' + user_company + '様_' + collect_type + '.pdf' 
# 一時ファイル
tmp_file          = '/srv/www/public_html/speed_score/speed_score/見積書_' + user_company + '様_' + collect_type + '_tmp.pdf' 

# A4縦のCanvasを作成 -- (*1)
w, h              = portrait(A4)
cv                = canvas.Canvas(tmp_file, pagesize=(w, h))

# フォントを登録しCanvasに設定 --- (*2)
font_size         = 18
b_file            = '/srv/www/public_html/speed_score/speed_score/YuGothB.ttc'
ttc_file          = '/srv/www/public_html/speed_score/speed_score/YuGothL.ttc'
pdfmetrics.registerFont(TTFont('YuGothB', b_file))
cv.setFont('YuGothB', font_size)
# 文字列を描画する --- (*3)
cv.setFillColorRGB(0, 0, 0)
cv.drawString(28*mm, h-48.7*mm, user_company)
if collect_type   == "一回きりの収集":
	tax           = tax + "-"
	sum_result    = sum_result + "-"
	temp_result   = temp_result + "-"
	result        = result + "-"
	cv.drawString(60*mm, h-74.7*mm, sum_result)
else:
	cv.drawString(57*mm, h-74.7*mm, sum_result + "～")

if collect_type   == "一回きりの収集":
	font_size     = 12
	pdfmetrics.registerFont(TTFont('YuGothB', b_file))
	cv.setFont('YuGothB', font_size)
	if n          == 6:
		cv.drawString(161.5*mm, h-192.1*mm, temp_result)
		cv.drawString(164*mm, h-197.6*mm, tax)
		cv.drawString(161.5*mm, h-203.2*mm, sum_result)
	if n          == 7:
		cv.drawString(158*mm, h-192.1*mm, temp_result)
		cv.drawString(161.5*mm, h-197.6*mm, tax)
		cv.drawString(158*mm, h-203.2*mm, sum_result)

	font_size     = 12
	pdfmetrics.registerFont(TTFont('YuGothL', ttc_file))
	cv.setFont('YuGothL', font_size)
	if n          == 6:
		cv.drawString(132*mm, h-129.4*mm, result)
		cv.drawString(162.7*mm, h-129.4*mm, result)
	elif n          == 7:
		cv.drawString(129*mm, h-129.4*mm, result)
		cv.drawString(159.5*mm, h-129.4*mm, result)
else :
	font_size     = 12
	pdfmetrics.registerFont(TTFont('YuGothB', b_file))
	cv.setFont('YuGothB', font_size)
	if n          == 6:
		cv.drawString(157.6*mm, h-192.1*mm, temp_result + "～")
		cv.drawString(160*mm, h-197.6*mm, tax + "～")
		cv.drawString(157.6*mm, h-203.2*mm, sum_result + "～")
	elif n          == 7:
		cv.drawString(153.5*mm, h-192.1*mm, temp_result + "～")
		cv.drawString(157*mm, h-197.6*mm, tax + "～")
		cv.drawString(153.5*mm, h-203.2*mm, sum_result + "～")

	font_size     = 12
	pdfmetrics.registerFont(TTFont('YuGothL', ttc_file))
	cv.setFont('YuGothL', font_size)
	if n          == 6:
		cv.drawString(128*mm, h-129.4*mm, result + "～")
		cv.drawString(158.7*mm, h-129.4*mm, result + "～")
	elif n          == 7:
		cv.drawString(124.5*mm, h-129.4*mm, result + "～")
		cv.drawString(155.2*mm, h-129.4*mm, result + "～")

font_size         = 10
pdfmetrics.registerFont(TTFont('YuGothL', ttc_file))
cv.setFont('YuGothL', font_size)
cv.drawString(58*mm, h-91.7*mm, deadline)
cv.drawString(58*mm, h-137.2*mm, collect_type)
cv.drawString(53*mm, h-155.2*mm, detail)
cv.drawString(130*mm, h-41.3*mm, today)
cv.drawString(155*mm, h-41.3*mm, file_id)

font_size         = 6
pdfmetrics.registerFont(TTFont('YuGothL', ttc_file))
cv.setFont('YuGothL', font_size)
if len(url)       > 51 and len(url) < 101:
	cv.drawString(55*mm, h-144*mm, url[0:50])
	cv.drawString(55*mm, h-146*mm, url[50:])
elif len(url)     > 101 and len(url) < 151:
	cv.drawString(55*mm, h-142.5*mm, url[0:50])
	cv.drawString(55*mm, h-145*mm, url[50:100])
	cv.drawString(55*mm, h-147.5*mm, url[100:])
else:
	cv.drawString(55*mm, h-145*mm, url)

# 一時ファイルに保存 --- (*4)
cv.showPage()
cv.save()

# テンプレートとなるPDFを読む --- (*5)
template_pdf      = PdfFileReader(template_file)
template_page     = template_pdf.getPage(0)

# 一時ファイルを読んで合成する --- (*6)
tmp_pdf           = PdfFileReader(tmp_file)
template_page.mergePage(tmp_pdf.getPage(0))

# 書き込み先PDFを用意 --- (*7)
output            = PdfFileWriter()
output.addPage(template_page)
with open(output_file, "wb") as fp:
  output.write(fp)