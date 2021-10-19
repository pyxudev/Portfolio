import csv
from datetime import datetime
from uuid import uuid4
import codecs
from django.shortcuts import HttpResponse
from django.utils.translation import gettext_lazy

from ..dummy_api import delete_database_for_request, start_request, stop_request
from ..models import Request, User_dashboard, Data

"""-------------------------------------------------------------------------------------------------------------------------------------------"""
"""Support Functions for Main functions of backend STARTS here"""


def get_uuid():
    return str(uuid4())


# TODO : Fix the delete_database_for_request() function
def check_for_storage(dashboard):
    request_list = Request.objects.filter(connected_dashboard=dashboard, running_status=4, is_show=True).order_by('-time_end')
    storage_size = 3
    counter = 0
    for req in request_list:
        if counter < storage_size:
            counter += 1
        else:
            req.was_downloaded = True
            req.is_show = False
            req.save()
            delete_database_for_request(req.task_id)
            


def change_request_status(request, status, time):
    if status == 1:
        request.running_status = 1
        request.last_status = gettext_lazy("Request for scraping has been submitted.")
        request.save()
    elif status == 2:
        request.running_status = 2
        request.last_status = gettext_lazy("Scraping for data has started")
        request.time_start_scraping = time
        request.save()
    elif status == 3:
        request.running_status = 3
        request.last_status = gettext_lazy("Sorry error connecting to server. Please try again.")
        request.time_start_scraping = time
        request.time_end_scraping = time
        request.time_end = time
        request.save()
    elif status == 4:
        request.running_status = 4
        request.last_status = gettext_lazy("Data Scraping Complete. Click to download")
        request.time_end_scraping = time
        request.time_end = time
        request.is_download_ready = True
        request.save()
        check_for_storage(request.connected_dashboard)
    elif status == 5:
        request.last_status = gettext_lazy("Request has been canceled by user. Will shortly be canceled from server side.")
        request.time_end_scraping = time
        request.time_end = time
        request.running_status = 5
        request.save()
        delete_database_for_request(request.task_id)
    else:
        request.last_status = gettext_lazy("Unknown Error")
        request.time_end_scraping = time
        request.time_end = time
        request.running_status = 6
        request.save()


def delete_old_ongoing_requests(dashboard):
    for req in Request.objects.filter(connected_dashboard=dashboard, running_status=1):
        cancel_request(req.task_id)
    for req in Request.objects.filter(connected_dashboard=dashboard, running_status=2):
        cancel_request(req.task_id)


def create_new_request(dashboard):
    created_request = Request.objects.create(connected_dashboard=dashboard, unique_id=get_uuid())
    delete_old_ongoing_requests(dashboard)
    task_id = created_request.task_id
    change_request_status(created_request, 1, datetime.now())

    scrapy_task_id, status = start_request(created_request)
    created_request.scrapy_task_id = scrapy_task_id
    created_request.save()
    change_request_status(created_request, status, datetime.now())
    return created_request


def cancel_request(task_id):
    request = Request.objects.get(task_id=task_id)
    #_, status = stop_request(request)
    change_request_status(request, 5, datetime.now())
    _, status = stop_request(request)
    if status != 5:
        change_request_status(request, status, datetime.now())
    return request

def download_files(task_id):
    request = Request.objects.get(task_id=task_id)
    model_class = Data
    meta = model_class._meta
    field_names = [field.name for field in meta.fields]

    time = request.time_end
    filename = time.strftime("%Y%m%d_%H%M_NETIS.csv")
    print(filename)
    filestring = 'attachment; filename=' + filename
    response = HttpResponse(content_type='text/csv; charset=utf_8_sig')
    response['Content-Disposition'] = filestring.format(meta)
    #response.write(u'\ufeff'.encode('utf8'))
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in model_class.objects.filter(unique_id=request.unique_id):
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


def do_operation(request,action="start"):
    user = request.user
    dashboard = User_dashboard.objects.get(connected_user=user)
    check_for_storage(dashboard)
    if action == "start":
        create_new_request(dashboard)
    elif action == "stop":
        task_id = request.POST['task_id']
        task_id = int(task_id)
        cancel_request(task_id)
    requests_set = Request.objects.filter(connected_dashboard=dashboard,is_show=True).order_by('-task_id')
    requests = requests_set
    context = {"requests":requests}
    return context


""" Support functions for main functions of backend ENDS here"""
"""----------------------------------------------------------------------------------------------------------------------------------------------"""
