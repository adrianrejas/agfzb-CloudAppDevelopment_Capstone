from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles GET request
    if request.method == "GET":
        return redirect('djangoapp:index')
    # Handles POST request
    elif request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context['error_login'] = "Bad username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        context['error_login'] = "Malformed request."
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
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
def get_dealerships(request):
    if request.method == "GET":
        # Create context
        context=dict()
        # Get dealers from the URL
        url = "https://8ce99a88.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships, result = get_dealers_from_cf(url)
        # Add dealerships and result to the context
        context["dealerships"] = dealerships
        context["result"] = result
        # Render template
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Create context
        context=dict()
        # Get URLs for managing dealers and reviews
        url = "https://8ce99a88.eu-gb.apigw.appdomain.cloud"
        dealer_url = url + "/api/dealership"
        review_url = url + "/api/review"
        # Get dealer details from the URL and add result to the context
        dealer, dealer_status = get_dealer_by_id(dealer_url, dealer_id)
        context["dealer"]=dealer
        context["dealer_result"]=dealer_status
        # Get review list for dealer from the URL and add result to the context
        reviews, review_status = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"]=reviews
        context["review_result"]=review_status
        # Render template
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        # Create context
        context=dict()
        # Get URLs for managing dealers
        url = "https://8ce99a88.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealer details from the URL and add result to the context
        dealer, dealer_status = get_dealer_by_id(url, dealer_id)
        context["dealer"]=dealer
        context["result"]=dealer_status
        # Get cars available at dealer and add result to the context
        cars= CarModel.objects.all().filter(dealer_id=dealer_id)
        context['cars'] = cars
        # Render template
        return render(request, 'djangoapp/add_review.html', context)   
    elif request.method == "POST":
        if request.user.is_authenticated:
            url = "https://8ce99a88.eu-gb.apigw.appdomain.cloud/api/review"
            review = dict()
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = True if (request.POST.get('purchasecheck', "False") == "on") else False
            car_id = request.POST.get("car", None)
            if car_id != None:
                car = CarModel.objects.get(id=car_id)
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"] = int(car.yearpublished())
                review["purchase_date"] = request.POST["purchasedate"]
            json_payload = dict()
            json_payload["review"] = review
            result, status_code = post_request(url, json_payload, dealerId=dealer_id)
            print(result)
            if (result["ok"]):
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            else:
                context=dict()
                context["error"] = result["message"]
                return render(request, 'djangoapp/add_review.html', context)  
        else:
            # Create context
            context=dict()
            # Add user not authenticated error
            context["error"] = "User is not authenticated"
            # Get URLs for managing dealers
            url = "https://8ce99a88.eu-gb.apigw.appdomain.cloud/api/dealership"
            # Get dealer details from the URL and add result to the context
            dealer, dealer_status = get_dealer_by_id(url, dealer_id)
            context["dealer"]=dealer
            context["result"]=dealer_status
            # Get cars available at dealer and add result to the context
            cars= CarModel.objects.all().filter(dealer_id=dealer_id)
            # Render template
            return render(request, 'djangoapp/add_review.html', context)   


