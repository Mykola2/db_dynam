from datetime import *
from django.shortcuts import render
import os
from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from DYNAM.models import *
from db_dynam import settings
from django.db import connections
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.transaction import connections
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
import timeit
from django.db import connections

BASE_DIR = os.path.dirname(os.path.dirname(__file__))




def load (request):
    if request.method == 'POST':
        database_id = request.POST['id db']
        newDatabase = {}
        newDatabase["id"] = database_id
        newDatabase['ENGINE'] = request.POST['engine']
        newDatabase['NAME'] =request.POST['name']
        newDatabase['USER'] = request.POST['user']
        newDatabase['PASSWORD'] = request.POST['pass']
        newDatabase['HOST'] = request.POST['host']
        newDatabase['PORT'] = request.POST['port']

        settings.DATABASES[database_id] = newDatabase
        print settings.DATABASES.values()
        print Detail.objects.using(database_id).all().values()
    return render_to_response('load.html', context_instance=RequestContext(request))

def flood(request):
    global addtime
    global jointime
    global readtime
    global updatetime
    global deletetime
    addtime = {}
    jointime = {}
    readtime = {}
    updatetime = {}
    deletetime = {}
    if request.method == 'GET':
        return render_to_response('flood.html',context_instance=RequestContext(request))
    else:
        if request.POST['Q_FIRE']:
            for db in settings.DATABASES:
                Car.objects.using(db).all().delete()
                Category.objects.using(db).all().delete()
                start_time = timeit.default_timer()
                for x in range(0, int(request.POST['count'])):
                    c = Car()
                    c.title = "title"
                    c.german = False
                    c.engine_v = 1.5
                    c.release = datetime.now()
                    cat = Category()
                    cat.name = "First"
                    cat.save(using=db)
                    c.category = cat
                    det = Detail()
                    c.save(using=db)
                    det_list = [Detail.objects.using(db).get_or_create(producer = t.strip())[0] for t in "prod1,prod2,prod3".split(',')]
                    for det in det_list:
                        det.save(using=db)
                        c.details.add(det)
                addtime[db] = timeit.default_timer() - start_time
                jointime[db]=join(db)
                updatetime[db] = update(db)
                readtime[db] = read(db)
                deletetime[db] = delete(db)
        print "jointime" + `jointime`
        print "updatetime" + `updatetime`
        print "readtime" + `readtime`
        print "deletetime" + `deletetime`
        return render_to_response('flood.html',context_instance=RequestContext(request))

def join(db):
    start_time = timeit.default_timer()
    res = Car.objects.using(db).filter(category__name = 'First').select_related()
    jointime =  timeit.default_timer() - start_time
    print "res" + `res`
    return jointime


def update(db):
    c = Car.objects.using(db).all()
    start_time = timeit.default_timer()
    for car in c:
        car.title = "title_upd"
        car.german = 1
        car.engine = 2.0
        car.release = datetime.now()
        cat = Category()
        cat.name = "Second"
        cat.save(using=db)
        c.category = cat
        det = Detail()
        car.save(using=db)
        det_list = [Detail.objects.using(db).get_or_create(producer = t.strip())[0] for t in "prod1_upd,prod2_upd,prod3_upd".split(',')]
        for det in det_list:
            det.save(using=db)
            car.details.add(det)
    updatetime = timeit.default_timer() - start_time
    return updatetime

def read(db):
    start_time = timeit.default_timer()
    cars = Car.objects.using(db).all()
    readtime = timeit.default_timer() - start_time
    return readtime

def delete(db):
    start_time = timeit.default_timer()
    Car.objects.using(db).all().delete()
    Category.objects.using(db).all().delete()
    Detail.objects.using(db).all().delete()
    deletetime = timeit.default_timer() - start_time
    return deletetime

def chart1(request,):
    addtime1 = []
    deletetime1 = []
    readtime1  = []
    jointime1 = []
    updatetime1 = []
    for db in settings.DATABASES:
        addtime1.append([db,addtime[db]])
        deletetime1.append([db,deletetime[db]])
        readtime1.append([db,readtime[db]])
        updatetime1.append([db,updatetime[db]])
        jointime1.append([db,jointime[db]])
    print deletetime1
    aua = [['answered', 1], ['unanswered', 2]]
    return render_to_response('chart1.html', {'taginfo': addtime1,'delinfo':deletetime1 ,'selinfo':readtime1 ,'updinfo':updatetime1 ,'joininfo':jointime1}, context_instance=RequestContext(request))


