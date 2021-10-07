import requests
import json
from .models import CarDealer, DealerReview
from .api_settings import WATSON_NLU_API_KEY
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key is not None:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data, status_code

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    info = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None)
    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"], state=dealer["state"],
                                st=dealer["st"], zip=dealer["zip"])
            info.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result

def get_dealer_by_id(url, dealerId):
    # Call get_request with a URL parameter
    info = None
    result = "ok"
    json_result, status_code = get_request(url, None, dealerId=dealerId)
    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        dealer = dealers[0]
        # Create a CarDealer object with values in `doc` object
        info = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                        id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                        short_name=dealer["short_name"], state=dealer["state"],
                        st=dealer["st"], zip=dealer["zip"])
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result

def get_dealers_by_state (url, state):
    info = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None, state=state)
    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf (url, dealerId):
    info = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None, dealerId=dealerId)
    if status_code == 200 and json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["entries"]
        # For each review object
        for review in reviews:
            # Create a DealerReview object with values in object
            sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReview( id=review["id"], name=review["name"], review=review["review"],
                                   purchase=review["purchase"], car_make=review.get("car_make", None), 
                                   car_model=review.get("car_model", None), car_year=review.get("car_year", None),
                                   purchase_date=review.get("purchase_date", None), sentiment=sentiment)
            info.append(review_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result
    
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    try:
        API_KEY = WATSON_NLU_API_KEY
        NLU_URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/278fd18f-c293-471e-8f87-9d2c1ff46450/v1/analyze?version=2020-08-01"
        params = dict()
        params["text"] = text
        params["features"] = {"sentiment":[]}
        params["language"] = "en"
        json_result, status_code = get_request(NLU_URL, API_KEY, 
                text=text, features={"sentiment":[]}, language="en")
        if status_code != 200:
            return "undefined"
        return json_result["sentiment"]["document"]["label"]
    except:
        return "undefined"