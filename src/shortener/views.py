from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import URLForm
from .models import ShawtyURL

from analytics.models import ClickEvent


"""Coding 'slug/shortcode=None', because if it's absent, shortcode comes in as a kwarg anyway, due to urls.py using r'^(?P<shortcode>[\w-]+)' regex.

So set the kwarg as an argument, and use the shortcode within the function
"""


# def shawty_redirect_view(request, slug=None, *args, **kwargs):
    # print(kwargs)
    # print(shortcode)
    # print(request.user) #Also comes with request data
    # print(request.user.is_authenticated())

    # obj = ShawtyURL.objects.get(shortcode=slug)
    # return HttpResponse('{sc}'.format(sc=obj.url))


"""Different ways to either return an existing instance's URL or handle a 'Does Not Exist' error page:

    # 1. Put query into try block. When exception is caught, return the first existing object. If slug does not exist, return first object.

    # try:
    #     obj = ShawtyURL.objects.get(shortcode=slug)
    # except:
    #     obj = ShawtyURL.objects.all().first()
    # return HttpResponse('{sc}'.format(sc=obj.url))


    # 2. Method to setting a 'None' default.
    # If the shortcode does not exist, return None. Else, return the instance's URL

    # obj_url = None
    # qs = ShawtyURL.objects.filter(shortcode__iexact=slug.upper()) #__iexact denotes a case-INsensitive exact match: Slug, sLUg, slug. The fact that it needs to match .upper() does not matter. .upper() coded as example.
    # if qs.exists() and qs.count()==1:
    #     obj = qs.first()
    #     obj_url = obj.url
    # return HttpResponse('{sc}'.format(sc=obj_url))


    # 3. Shortcut method. get_object_or_404: good method if a default or alternative action is not desired, and only want 404 page in case of bad request.

    obj = get_object_or_404(ShawtyURL, shortcode=slug)
    return HttpResponseRedirect(obj.url)
"""


"""in CBV, explicitly write the HTTP method you want to handle. GET or POST.
In contrast to above FBV which handles any method by default. in FBV, can print out print(request.method) anytime to see what youre handling.

CBV takes a bit more code to write, but is more portable bc explicit.

[description]
"""


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = URLForm()
        bg_image = 'https://images4.alphacoders.com/198/198248.jpg'
        context = {
            "title": "URL Shortener",
            "form": the_form,
            "bg_image": bg_image,
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        form_data = URLForm(request.POST)
        bg_image = 'https://images4.alphacoders.com/198/198248.jpg'
        context = {
            "title": "URL Shortener",
            "form": form_data,
            "bg_image": bg_image,
        }
        template = "shortener/home.html"
        if form_data.is_valid():
            url = form_data.cleaned_data.get('url')
            obj, created = ShawtyURL.objects.get_or_create(url=url)
            context = {
                "object": obj,
                "created": created,
            }

            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)



# class ShawtyCBView(View):
#     def get(self, request, shortcode=None, *args, **kwargs):
#         # obj = ShawtyURL.objects.get(shortcode=shortcode)
#         obj = get_object_or_404(ShawtyURL, shortcode=shortcode)
#         print(obj.url)
#         return HttpResponseRedirect(obj.url)


class ShawtyCBView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = ShawtyURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        print('hey')
        print(obj.url)
        print(str(HttpResponseRedirect(obj.url)))

        return HttpResponseRedirect(obj.url)