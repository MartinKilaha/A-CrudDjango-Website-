from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .form import ClientForm
from .models import Client


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def services(request):
    return render(request, 'services.html')


# def register(request):
#     return render(request, 'register.html')


# def login(request):
#     return render(request, 'login.html')


# def logout(request):
#     return render(request,'logout.html')

def register(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        else:
            form = ClientForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        Client = authenticate(username=username, password=password)

        if Client is not None:
            login(request, Client)
            return redirect('/')

        else:
            return redirect('/login')

    return render(request, "login.html")


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Erick were",
            "TransactionDesc": "Web Development Charges"
        }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")


def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})
