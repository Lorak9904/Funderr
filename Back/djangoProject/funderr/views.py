import html.parser
from time import sleep
from django.http import HttpResponse, JsonResponse
from .forms import GeneralInquiryForm, EachCargoDimsForm, GeneralInquiry, TestTinyMCEForm
from .models import EachCargoDims, Airlines_contacts, Airports

from django.forms import formset_factory, modelformset_factory
from openai import APIConnectionError
from traceback import format_exc
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import QueryDict
from django.http import HttpResponse, QueryDict
from django.urls import reverse 
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage as DjangoCoreEmailMessage, EmailMultiAlternatives, send_mass_mail, get_connection, send_mail
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import json
import requests
from django.contrib import messages


from email.message import EmailMessage
from email.parser import BytesParser
from email.mime.image import MIMEImage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import message_from_string, policy


def home(request):
	return render(request, "home.html")