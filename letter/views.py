from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SubscriberForm, MailMessageForm
from django.contrib import messages
from django.core.mail import send_mail
from django_pandas.io import read_frame
from .models import Subscribers
from django.core.mail import EmailMessage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Create your views here.

def index(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription successfully')
            return redirect('/')
    else:
        form = SubscriberForm()
    context = {
        'form': form,
    }
    return render(request, 'letter/index.html', context)


def mail_letter(request):
    emails = Subscribers.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            form.save()
            subject = 'check if it works'
            html_content = get_template('newsletter.html').render({'title': title, 'message': message})
            from_email = 'koracodeafrica@gmail.com'
            msg = EmailMessage(subject, html_content, from_email, ['byiringoroscar@gmail.com'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'message has been sent to the mail list')
            return redirect('mail_letter')
    else:
        form = MailMessageForm()
    context = {
        'form': form

    }
    return render(request, 'letter/mail_letter.html', context)

# def mail_letter(request):
#     emails = Subscribers.objects.all()
#     df = read_frame(emails, fieldnames=['email'])
#     mail_list = df['email'].values.tolist()
#     if request.method == 'POST':
#         form = MailMessageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             title = form.cleaned_data.get('title')
#             message = form.cleaned_data.get('message')
#             send_mail(
#                 title,
#                 message,
#                 '',
#                 mail_list,
#                 fail_silently=False,
#             )
#             messages.success(request, 'message has been sent to the mail list')
#             return redirect('mail_letter')
#     else:
#         form = MailMessageForm()
#     context = {
#         'form': form
#
#     }
#     return render(request, 'letter/mail_letter.html', context)
