cat /home/ubuntu/scripts/daily_mail.txt | /usr/sbin/sendmail -i -t
echo 'From: <***>' > /home/ubuntu/scripts/daily_mail.txt
echo 'To: <***>' >> /home/ubuntu/scripts/daily_mail.txt
echo 'Subject: daily_mail' >> /home/ubuntu/scripts/daily_mail.txt
/usr/bin/python3 /home/ubuntu/scripts/daily_mail.py
cat /home/ubuntu/scripts/email_content.txt | while read line
do
	echo $line
done