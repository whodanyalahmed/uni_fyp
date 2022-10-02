from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from django.urls import resolve
from scraper_and_analyzer import urls
from numpy import Infinity
from scraper_and_analyzer.backend.pakmobizone import pakmobizone_main
from scraper_and_analyzer.backend.priceoye import priceOye_main
from scraper_and_analyzer.backend.daraz import daraz_main
# Create your views here.


def get_min_max_price(daraz, priceOye, pakmobizone):

    price_array = [daraz['price'],
                   priceOye['price'], pakmobizone['price']]
    lowest_price = min(price_array)
    # find the highest price
    highest_price = max(price_array)
    # get the index of the lowest price
    lowest_index = price_array.index(lowest_price)
    # get the index of the highest price
    highest_index = price_array.index(highest_price)
    if(lowest_index == 0):
        min_price_product = daraz
    elif(lowest_index == 1):
        min_price_product = priceOye
    else:
        min_price_product = pakmobizone

    if(highest_index == 0):
        max_price_product = daraz
    elif(highest_index == 1):
        max_price_product = priceOye
    else:
        max_price_product = pakmobizone
    return min_price_product, max_price_product


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):

    current_url = resolve(request.path_info).url_name
    return render(request, 'index.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Minimum(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'minimum.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def maximum(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'maximum.html', context={'current_url': current_url})


def result(request):
    # get browser session storage value

    # get request values
    if request.method == 'POST':

        keyword = request.POST.get('keyword')
        current_url = request.POST.get('url')
        print(keyword)
        if(not bool(keyword)):
            return render(request, 'results.html', context={'msg': "error", "text": "No keyword entered!"})
        else:
            # call scrapper function
            print("current_url: ", current_url)
            if (current_url != 'list' and current_url != 'prediction'):

                request.session['current_url'] = current_url
                try:
                    try:
                        priceOye = priceOye_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        priceOye = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/data-not-found.gif"
                        }
                    try:
                        daraz = daraz_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        daraz = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/data-not-found.gif"
                        }
                    try:

                        pakmobizone = pakmobizone_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        pakmobizone = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/data-not-found.gif"
                        }

                    if(daraz['name'] == "No Product found" and priceOye['name'] == "No Product found" and pakmobizone['name'] == "No Product found"):
                        return render(request, 'results.html', context={'msg': "error", "text": "No result found!"})

                    # find the lowest price

                    # set values in session
                    request.session['daraz'] = daraz
                    request.session['priceOye'] = priceOye
                    request.session['pakmobizone'] = pakmobizone
                    # if anyone is infinity
                    min_price_product, max_price_product = get_min_max_price(
                        daraz, priceOye, pakmobizone)
                    print("min_price_product: ", min_price_product)
                    print("max_price_product: ", max_price_product)
                    return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "min_price_product": min_price_product, "max_price_product": max_price_product, "current_url": current_url})
                except Exception as e:
                    return render(request, 'results.html', context={'msg': "error", "text": "Can't find the product or may not exist!"})

    if request.method == 'GET':
        # get values fromm session

        current_url = request.session['current_url']
        try:

            if current_url != 'list' and current_url != 'prediction':
                daraz = request.session['daraz']
                priceOye = request.session['priceOye']
                pakmobizone = request.session['pakmobizone']
                min_price_product, max_price_product = get_min_max_price(
                    daraz, priceOye, pakmobizone)
                return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "min_price_product": min_price_product, "max_price_product": max_price_product, "current_url": current_url})
        except:
            return redirect('Dashboard')


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def _list(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'list.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def prediction(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'prediction.html', context={'current_url': current_url})
