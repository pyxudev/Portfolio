from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic
from django.urls import reverse_lazy
from .forms import LoginForm, SignupForm, PasswordResetForm, PasswordResetConfirmForm, ProfileForm
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from dashboard.models import User_dashboard,Request
User = get_user_model()

def create_demo_request(dashboard):
    req = Request.objects.create(connected_dashboard=dashboard)
    print(req)
    return req

def create_user_dashboard(user):
    if User_dashboard.objects.filter(connected_user=user).exists():
        dashboard = User_dashboard.objects.get(connected_user=user)
    else:
        dashboard = User_dashboard.objects.create(connected_user=user)
    # create_demo_request(dashboard)
    return dashboard

#Login

class Login(LoginView):
    form_class = LoginForm
    template_name = 'pages/login.html'


#Signup
class Signup(generic.CreateView):
    template_name = 'pages/signup.html'
    form_class = SignupForm
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
            'settings': settings,
        }
        subject = render_to_string('email/account_activation_confirm_subject.txt', context).strip()
        message = render_to_string('email/account_activation_confirm_message.txt', context)
        print(subject)
        print(message)
        user.email_user(subject,message)
        return redirect('accounts:signup_activation_confirm')

class SignupActivationConfirm(generic.TemplateView):
    template_name = 'pages/signup_activation_confirm.html'

class SignupActivationComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_anme = 'pages/signup_activation_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24*10000) # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        print(token)
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
            user = User.objects.get(pk=user_pk)
            print(user, user.is_active)
            user.is_active=True
            create_user_dashboard(user)
            user.save()
            return redirect('dashboard:index')
    
        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    create_user_dashboard(user)
                    return redirect('dashboard:index')
        return HttpResponseBadRequest()


# Password Reset
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    form_class = PasswordResetForm
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_message.txt'
    template_name = 'pages/password_reset.html'
    # user.email_user(subject,message)
    success_url = reverse_lazy('accounts:password_reset_done')
    extra_email_context = {
        'settings' : settings,
    }

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'pages/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'pages/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'pages/password_reset_complete.html'


# What use of this ???? 
# Where is pages-user-profile.html ????
@login_required
def profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect("/accounts/profile")
    else:
        profile_form = ProfileForm(instance=request.user)

    return render(request, "pages/pages-user-profile.html", context={"form": profile_form})




        




