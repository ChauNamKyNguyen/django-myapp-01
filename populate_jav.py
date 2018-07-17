import datetime
import random

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jav_with_django.settings')

import django
django.setup()

from jav.models import Actress, Movie

from django.utils.text import slugify

def populate():
    ai_uehara = add_actress("Ai Uehara")

    add_movie(actress = ai_uehara, title = "BBAN-034 Lesbian Gangbang in high school", url = "http://pics.dmm.co.jp/mono/movie/adult/bban034/bban034pl.jpg")

    add_movie(actress = ai_uehara, title = "FSET-529 I and my friend turn on because of neighbor's moaning", url = "http://pics.dmm.co.jp/mono/movie/adult/1fset529/1fset529pl.jpg")
   
    akiho_yoshizawa = add_actress("Akiho Yoshizawa")
    
    add_movie(actress = akiho_yoshizawa, title = "SNIS-665 Fucking day of the main caster Acky", url = "http://pics.dmm.co.jp/mono/movie/adult/snis665/snis665pl.jpg")

    add_movie(actress = akiho_yoshizawa, title = "SNIS-460 Let's matchmaking Acky teach you fuck", url = "http://pics.dmm.co.jp/mono/movie/adult/snis460/snis460pl.jpg")
    
    add_movie(actress = akiho_yoshizawa, title = "MXGS-561 Beauty office lady is molested everyday on train", url = "http://pics.dmm.co.jp/mono/movie/adult/h_068mxgs561/h_068mxgs561pl.jpg")
    
    uehara_mizuho = add_actress("Uehara Mizuho")

    add_movie(actress = uehara_mizuho, title = "ABP-454 My romance sex in office with Mizuho", url = "http://pics.dmm.co.jp/mono/movie/adult/118abp454/118abp454pl.jpg")

    add_movie(actress = uehara_mizuho, title = "ABP-440 Our club advisor is a sex slaver", url = "http://pics.dmm.co.jp/mono/movie/adult/118abp440/118abp440pl.jpg")

    yui_hatano = add_actress("Yui Hatano")
    
    add_movie(actress = yui_hatano, title = "GVG-699 Family Techer Yui lust her students", url = "http://pics.dmm.co.jp/mono/movie/adult/13gvg699/13gvg699pl.jpg")
    
    for a in Actress.objects.all():
        for m in Movie.objects.filter(actress = a):
            print ("- {0} - {1}".format(str(a), str(m)))

def add_movie(actress, title, url, views=0, like=0):
    views = random.randint(1,10)
    like = random.randint(1,10)
    m = Movie.objects.get_or_create(actress = actress, title = title, url = url, views = views, like = like, date = datetime.datetime.now())[0]
    m.save()
    return m

def add_actress(name):
    view = random.randint(1,10)
    like = random.randint(1,10)
    a = Actress.objects.get_or_create(name = name, view = view, like = like)[0]
    return a

# Start execution here!
if __name__ == '__main__':
    print ("Starting Jav population script ...")
    populate()
