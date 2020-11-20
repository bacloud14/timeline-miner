from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import requests
import logging
import json
from cache_memoize import cache_memoize
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hello.forms import NameForm
import en_core_web_sm


@cache_memoize(60 * 60 * 24)
def load_model():
    logging.debug("@@@@@ LOADING MODEL @@@@@")
    return en_core_web_sm.load()

# Create your views here.
def index(request):
    form = NameForm(request.POST)
    return render(request, "upload.html", {'form': form})

# Create your views here.
def donate(request):
    return render(request, "donate.html")

from .process import get_best_split, extract_events_spacy

def upload(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = NameForm(request.POST)
        logging.debug(request.POST.get("g-recaptcha-response"))
        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6Ldq5uMZAAAAAOH24Nryg--mMldNq2mIT-d57Ct8"
        captcha_data= {"secret": captcha_secret, "response": captcha_token}
        captcha_server_response = requests.post(url=captcha_url, data=captcha_data)
        captcha_json = json.loads(captcha_server_response.text)
        if captcha_json['success'] == False:
            return render(request, "upload.html", {'errors': "You must verify captcha !", 'form': form})
        
        if form.is_valid():
            nlp = load_model()
            text = (form.cleaned_data['your_text'])
            timeline = extract_events_spacy(text, nlp)
            gold = (get_best_split(timeline, text))
            return render(request, "upload.html", {'result': str(gold), 'form': form, 'json_result':gold})
            #return HttpResponseRedirect('/upload.html/')
    else:
        form = NameForm()
    return render(request, "upload.html", {'form': form})

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})