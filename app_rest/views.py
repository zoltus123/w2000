from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, Http404
from django.shortcuts import  get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from app_regiony.models import Wojewodztwo, Powiat, Gmina
from app_wybory.models import Obwod, Kandydat

from app_wybory.views import podajDaneKraju, podajDaneObwodu, podajDaneGminy, podajDanePowiatu, podajDaneWojewodztwa
from app_wybory.views import znajdzGminy, edytujWynik, dajEdycjaDane


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def restIndexView(request):
    return JsonResponse(podajDaneKraju(), safe=False)


def restWojView(request, woj_id):
    woj = get_object_or_404(Wojewodztwo, id=woj_id)
    return JsonResponse(podajDaneWojewodztwa(woj), safe=False)


def restPowView(request, pow_id):
    pow = get_object_or_404(Powiat, id=pow_id)
    return JsonResponse(podajDanePowiatu(pow), safe=False)


def restGmiView(request, gmi_id):
    gmi = get_object_or_404(Gmina, id=gmi_id)
    return JsonResponse(podajDaneGminy(gmi), safe=False)


def restObwView(request, obw_id):
    obw = get_object_or_404(Obwod, id=obw_id)
    return JsonResponse(podajDaneObwodu(obw), safe=False)


def restSzukajView(request):
    try:
        return JsonResponse(znajdzGminy(request.GET['wzorzec']))
    except KeyError:
        raise Http404('Brak wzorca do wyszukania')


def restLoginView(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        except KeyError:
            return JsonResponse({'komunikat' : 'źle'})
        if user is not None:
            return JsonResponse({'komunikat' : 'ok'})
    return JsonResponse({'komunikat' : 'źle'})


def restEdycjaDaneView(request):
    try:
        obwod = get_object_or_404(Obwod, id=request.GET['obw_id'])
        kandydat = get_object_or_404(Kandydat, id=request.GET['kand_id'])
        return JsonResponse(dajEdycjaDane(obwod, kandydat))
    except KeyError:
        raise Http404('Podaj id obwodu i kandydata')


def restEdytujView(request):
    if request.method == 'POST':
        try:
            obwod = get_object_or_404(Obwod, id=request.POST['obw_id'])
            kand = get_object_or_404(Kandydat, id=request.POST['kand_id'])
            username = request.POST['username']
            password = request.POST['password']
            wynik = int(request.POST['wynik'])
        except KeyError:
            return JsonResponse({'komunikat' : 'podaj dane'})
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'komunikat': 'zaloguj się'})
        return JsonResponse({'komunikat' : edytujWynik(obwod, kand, wynik)})
    return JsonResponse({'komunikat' : 'podaj dane'})