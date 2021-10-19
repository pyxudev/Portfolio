from datetime import datetime
from uuid import uuid4

from django.core.mail import send_mail
from scrapyd_api import ScrapydAPI
from .models import Request, Data
scrapyd = ScrapydAPI("http://localhost:6800")


# TODO : delete all the entries in database that belongs to request Job Id = Task Id
def delete_database_for_request(task_id):
    r = Request.objects.get(task_id=task_id)
    Data.objects.filter(unique_id=r.unique_id).delete()
    return True


def get_uuid():
    return str(uuid4())


def start_request(created_request):
    try:
        task_id = scrapyd.schedule(project="bukka", spider="data", unique_id=created_request.unique_id,
                                   request_id=created_request.task_id)
    except Exception as e:
        print(e)
        time = datetime.now().strftime("%Y%m%d_%H%M")
        message = "Scraping Error Occured at "+time
        # send_mail('New Request Start Error', message, None, ["****","***@****"])
        return None, 3
    return task_id, 2


def stop_request(request):
    try:
        task_id = scrapyd.cancel(project="bukka", job=request.scrapy_task_id)
    except Exception as e:
        print(e)
        return None, 6
    return None, 5
