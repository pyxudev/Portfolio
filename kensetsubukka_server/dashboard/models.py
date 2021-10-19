from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class User_dashboard(models.Model):
    dashboard_id = models.AutoField(auto_created = True, primary_key = True, serialize = False)
    connected_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Request(models.Model):
    task_id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=100, null=True, default=None)
    scrapy_task_id = models.CharField(max_length=100, null=True, default=None)
    connected_dashboard = models.ForeignKey(User_dashboard, on_delete=models.CASCADE)
    time_received = models.DateTimeField(default=datetime.now)
    time_start_scraping = models.DateTimeField(default=None, null=True)
    time_end_scraping = models.DateTimeField(default=None, null=True)
    time_end = models.DateTimeField(default=None, null=True)
    last_status = models.TextField(default="Request Received")
    Status = [
        (1, 'Submitted'),
        (2, 'Scraping'),
        (3, 'Error'),
        (4, 'Complete'),
        (5, 'Interrupted'),
        (6, 'Unknown'),
    ]
    running_status = models.IntegerField(default=0, choices=Status)
    filename = models.TextField(default=None, null=True, blank=True)
    was_downloaded = models.BooleanField(default=False)
    is_download_ready = models.BooleanField(default=False)
    is_show = models.BooleanField(default=True)






class Data(models.Model):
    unique_id = models.TextField(default=None, null=True, blank=True)
    count = models.TextField(default=None, null=True, blank=True)
    NETIS登録番号 = models.TextField(default=None, null=True, blank=True)
    技術名称 = models.TextField(default=None, null=True, blank=True)
    事後評価 = models.TextField(default=None, null=True, blank=True)
    受賞等_建設技術審査証明 = models.TextField(default=None, null=True, blank=True)
    受賞等_国土技術開発賞 = models.TextField(default=None, null=True, blank=True)
    受賞等_ものづくり日本大賞 = models.TextField(default=None, null=True, blank=True)
    受賞等_他機関の評価結果 = models.TextField(default=None, null=True, blank=True)
    事前審査_事後評価_試行実証評価 = models.TextField(default=None, null=True, blank=True)
    事前審査_事後評価_活用効果評価 = models.TextField(default=None, null=True, blank=True)
    事前審査_事後評価_事前審査 = models.TextField(default=None, null=True, blank=True)
    技術の位置付け_推奨技術 = models.TextField(default=None, null=True, blank=True)
    技術の位置付け_準推奨技術 = models.TextField(default=None, null=True, blank=True)
    技術の位置付け_評価促進技術 = models.TextField(default=None, null=True, blank=True)
    技術の位置付け_活用促進技術 = models.TextField(default=None, null=True, blank=True)
    level1 = models.TextField(default=None, null=True, blank=True)
    level2 = models.TextField(default=None, null=True, blank=True)
    level3 = models.TextField(default=None, null=True, blank=True)
    level4 = models.TextField(default=None, null=True, blank=True)
    技術会社 = models.TextField(default=None, null=True, blank=True)
    技術_担当部署 = models.TextField(default=None, null=True, blank=True)
    技術_担当者 = models.TextField(default=None, null=True, blank=True)
    技術部署_住所 = models.TextField(default=None, null=True, blank=True)
    技術部署_Tel = models.TextField(default=None, null=True, blank=True)
    技術部署_FAX = models.TextField(default=None, null=True, blank=True)
    技術部署_Email = models.TextField(default=None, null=True, blank=True)
    技術部署_URL = models.TextField(default=None, null=True, blank=True)
    営業会社 = models.TextField(default=None, null=True, blank=True)
    営業_担当部署 = models.TextField(default=None, null=True, blank=True)
    営業部署_担当者 = models.TextField(default=None, null=True, blank=True)
    営業部署_住所 = models.TextField(default=None, null=True, blank=True)
    営業部署_Tel = models.TextField(default=None, null=True, blank=True)
    営業部署_FAX = models.TextField(default=None, null=True, blank=True)
    営業部署_Email = models.TextField(default=None, null=True, blank=True)
    営業部署_URL = models.TextField(default=None, null=True, blank=True)

