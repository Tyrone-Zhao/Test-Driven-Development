from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.filter(email=email).first()
    if not token:
        token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )
    message_body = f"请使用此链接登录: \n\n{url}"
    send_mail(
        "你的超级表登录链接",
        message_body,
        "tyrone-zhao@qq.com",
        [email],
    )
    messages.success(
        request,
        "请在你的邮箱中查收邮件，我们会把登录链接发送给你。"
    )
    return redirect("/")


def login(request):
    user = auth.authenticate(uid=request.GET.get("token"))
    if user:
        auth.login(request, user)
    return redirect("/")
