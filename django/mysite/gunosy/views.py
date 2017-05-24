from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse

import gunosy.naivebayes
import pickle



def gunosy_naivebayes(request):


    try:
        siteurl = request.GET.get('site_url')
        text = gunosy.naivebayes.url_to_sepatext(siteurl)
        category = gunosy.naivebayes.classify(text)
        correct_in=True
        d = {
            'correct_in':correct_in,
            'category':category,
        }
        return render(request,'get_url.html',d)
    except:
        false='正しくURLを入力してください'
        correct_in=False
        d = {
            'correct_in':correct_in,
            'false':false,
        }
        return render(request,'get_url.html',d)
