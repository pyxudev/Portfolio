import sys
import time
import datetime
import slackweb
from datetime import date as dt

args             = sys.argv
user_company     = args[1]
user_name        = args[2]
result           = args[3]
phone_number     = args[4]
column           = args[5]
row              = args[6]
url              = args[7]
frequency        = args[8]
delivery         = args[9]
data_order       = args[10]
deadline         = args[11] 

slack            = slackweb.Slack(url="https://hooks.slack.com/services/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")
# now              = str(dt.today())
clock_now        = datetime.datetime.now()
clock_hour       = clock_now.hour
clock_min        = clock_now.minute
clock            = str(clock_now.hour)+":"+str(clock_now.minute)


print_result     = clock + f"\n自動見積もりからお問い合わせ\n　形式：継続\n 会社名：{user_company}\n 担当者名：{user_name}\n 電話番号：{phone_number}\n 収集URL：{url}\n 行：{row}\n 列：{column}\n 納期：{deadline}\n 収集のタイミング：{frequency}\n データの受け取り方：{delivery}\n オプション：{data_order}\n お見積り金額：{result}\n"

slack.notify(text=print_result)