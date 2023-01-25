from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request, get_dealer_reviews_from_cf, \
    post_request, get_dealer_by_state, get_and_incr_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
# def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships


# the function returns all dealerships using http response / no template
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # return HttpResponse(dealer_names)


#        context["dealerships"] = dealerships
#        print(dealerships)
#        return render(request, 'djangoapp/index.html', context)
# the function returns dealerships by state using http response as there are no templates
def get_dealer_state(request, state):
    context = {}

    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership/dealership?state=" + str(
            state)
        dealerships = get_dealer_by_state(url, state=state)
        # context['dealers'] = dealerships
        # return render(request, 'djangoapp/state.html', context)
        return HttpResponse(dealerships)


# the function returns dealers by id using an Http response/ no templates
def get_dealer_id(request, id):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership/dealership?id=" + str(
            id)
        dealer = get_dealer_by_id_from_cf(url, id=id)
        context["dealer"] = dealer



    # return render(request, 'djangoapp/dealership.html', context)
    return HttpResponse(dealer)


def get_dealer_details(request, id):
    context = {}

    if request.method == "GET":
        dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership?id=" + str(
            id)

        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
        #context["id"] = id
        review_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/review-dealer-id?id =" + str(
            id)
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        #context[id] = id

        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

        # Get dealers from the URL


# Create a `add_review` view to submit a review
'''
def add_review(request, id):
    context = {}
    dealer_url = "https://2e991945.eu-gb.apigw.appdomain.cloud/api/dealership"
    dealer_fullname = get_dealers_from_cf(dealer_url, id=id)[0].full_name
    context["dealer_fullname"] = dealer_fullname
    context["dealer_id"] = id
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)

            review = dict()
            if "purchase" in request.POST:
                review["purchase"] = True
                review["purchase_date"] = request.POST["purchasedate"]
            else:
                review["purchase"] = False
                review["purchase_date"] = "01/01/2000"

            review["dealership"] = id
            review["id"] = -1
            review["name"] = user.username
            review["review"] = request.POST["content"]
            review["car_make"] = car.carMakeName
            review["car_model"] = car.name
            review["car_year"] = int(car.year)

            json_payload = {}
            json_payload["review"] = review

            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/post-review"

            post_request(url, json_payload)
        elif request.method == "GET":
            cars = CarModel.objects.filter(id=id)
            context["cars"] = cars
            return render(request, 'djangoapp/add_review.html', context)
    if request.method == "GET":
        cars = CarModel.objects.filter(id=id)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    return redirect("djangoapp:dealer_details", id=id)
    
 
    '''
'''
def add_review(request, id):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in, could not add review")

    context = {}

    if request.method == "POST":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/post-review" 
        review = {
            "dealership": id,
            "name": request.user.get_short_name(),
            "purchase": request.POST["car"],
            "review": request.POST["review"],
            "purchase_date": datetime.utcnow().isoformat(),
            "id": get_and_incr_id(),
        }
        car = CarModel.objects.get(id=request.POST['car'])
        if car:
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
        json_payload = {
            "review": review
        }
        result = post_request(url, json_payload, id=id)
        return redirect('djangoapp:dealer_details', id=id)

    if request.method == "GET":
        context["id"] = id
        context["cars"] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)


'''
'''
def add_review(request, id):
    context = {}
    dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False

            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            print(payload)
            review_post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/post-review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)
'''

# try this code
def add_review(request, id):
    context = {}
    dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars

        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["review"]
            print(payload['review'])
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchase_date"]
            payload["car_make"] = car.make
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year)

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/a5d11e3e-c856-4d91-80a6-652d47e081a9/dealership-package/post-review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)
