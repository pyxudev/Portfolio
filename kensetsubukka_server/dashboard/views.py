from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Request, User_dashboard
from .subviews.home_subviews import change_request_status, create_new_request, cancel_request, download_files, do_operation

""" ----------------------------------------------------------------------------------------------------------------------------------------"""
""" Main functions of backend STARTS here"""

@login_required
@csrf_exempt
def index(request):
    context = do_operation(request,action="")
    return render(request, 'index.html', context)



@login_required
@csrf_exempt
def request_scraping(request):
    context = do_operation(request,action="start")
    template = render_to_string('table.html',context,request=request)
    return JsonResponse(template, safe=False)


@login_required
@csrf_exempt
def stop(request):
    context = do_operation(request,action="stop")
    template = render_to_string('table.html',context,request=request)
    return JsonResponse(template, safe=False)


@login_required
@csrf_exempt
def download(request):
    user = request.user
    dashboard = User_dashboard.objects.get(connected_user=user)
    task_id = request.GET['task_id']
    task_id = int(task_id)
    task = Request.objects.get(task_id=task_id)
    if(task.connected_dashboard == dashboard):
        task_id = int(task_id)
        response = download_files(task_id)
        return response
    else:
        return HttpResponse(gettext_lazy("Task ID doesn't belong to this User"))



@login_required
@csrf_exempt
def update_status(request):
    requests = Request.objects.filter(running_status__in=[3,5,6])
    for req in requests:
        req.is_show=False
        req.save()
    requests = Request.objects.filter(running_status=5)
    return JsonResponse({"message":gettext_lazy("Successfully removed request from database.")})



@login_required
@csrf_exempt
def see_logs(request):
    user = request.user
    dashboard = User_dashboard.objects.get(connected_user=user)
    requests_set = list(Request.objects.filter(connected_dashboard=dashboard).order_by('-task_id'))
    requests = requests_set
    context = {"requests":requests}
    template = render_to_string('logs.html',context,request=request)
    return JsonResponse(template, safe=False)



@login_required
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        # print(request.POST)
        form = PasswordChangeForm(request.user, request.POST)
        # print(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            message = gettext_lazy("Password Changed Successfully.")
            # messages.success(request, 'Your password was successfully updated!')
            # context={"message":"Password changed successfully"}
        else:
            message = gettext_lazy("Incorrect Entries")
            # messages.error(request, 'Please correct the error below.')
            
    else:
        form = PasswordChangeForm(request.user)
        message = ""
    
    context={"form":form,"message":message}

    template = render_to_string('password_form.html',context,request=request)
    return JsonResponse(template, safe=False)


""" Main fucntion of backend ENDS here """
""" ----------------------------------------------------------------------------------------------------------------------------------------"""
""" Function for API access of backend STARTS here"""


@api_view(['GET', 'POST'])
@csrf_exempt
def update_database(request):
    if request.method == 'POST':
        try :
            print(request.data)
            task_id = request.data['task_id']
            status = request.data['status']
            print(task_id,status)
            task_id = int(task_id)
            status = int(status)
            request = Request.objects.get(task_id=task_id)
            change_request_status(request,status,datetime.now())
        except :
            print ("error occured")
            return Response({"message": "Data format incorrect."})
        return Response({"message": "requested data updated successfully"})
    return Response({"message": "API successfully accessed"})


""" Function for API access of backend ENDS here. """
""" ----------------------------------------------------------------------------------------------------------------------------------------"""
