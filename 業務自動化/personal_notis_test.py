import sys
import time
import datetime
import slackweb
from datetime import date as dt

args             = sys.argv
column           = args[1]
row              = args[2]
deadline         = args[3]
task_type        = args[4]
url              = args[5]

slack            = slackweb.Slack(url="*****")
clock_now        = datetime.datetime.now()
clock_hour       = clock_now.hour
clock_min        = clock_now.minute
clock            = str(clock_now.hour)+":"+str(clock_now.minute)

print_result     = clock + f"\n自動見積もりからお問い合わせ\n 形式：{task_type}\n URL：{url}\n 行：{row}\n 列：{column}\n 納期：{deadline}\n"

slack.notify(text=print_result)