import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create a `get_request` to make HTTP GET requests
'''
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print(response.text)
    json_data = json.loads(response.text)
    return json_data
'''
def get_and_incr_id():
    global max_id
    max_id += 1
    return max_id - 1

def get_request(url, **kwargs):
    """
    Utility function to make HTTP GET requests
    """
    api_key = None
    params = dict()
    print("\nGET from {} with paramaters {}".format(url, kwargs))
    try:
        if 'apikey' in kwargs:
            # ...separate apikey from kwargs to submit separately
            api_key = kwargs.pop('apikey')
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # ...verify we just have the parameters now
            print("Updated parameters: {}".format(kwargs))
            # ...call the get method in request lib
            response = requests.get(url, headers={'Content-type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # ...calling the request lib's get method with URL + params and store it
            response = requests.get(url, headers={'Content-type': 'application/json'},
                                    params=kwargs)
            # params = kwargs? //I mean i guess it's working.
    except:
        # ...if that fails leave a general note.
        print("Network exception occurred")
    # relay status code info to console
    status_code = response.status_code
    print("Response Final URL {}".format(response.url))
    print("Response status {} \n".format(status_code))
    # package and return json data
    json_data = json.loads(response.text)
    return json_data


# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url,
                                 params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data


# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url)
    if dealers:
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer['doc']    #'doc'
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])

            results.append(dealer_obj)
    print(results)
    return results


# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
'''
def get_dealer_by_state(url, state):
    results = []
    json_result = get_request(url, dealer_state=state)
    if json_result:
        dealerships_list = json_result["dealershipslist"]
        for dealer_doc in dealerships_list:
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                state=dealer_doc["state"],
                zip=dealer_doc["zip"],
            )
            results.append(dealer_obj)

    return results
'''


def get_dealer_by_state(url, **kwargs):
    """
    This function calls get_request() w/ the specified args (state) then:
        1. Parses the json data returned from the request / "get-state-dealers" Cloud function
        2. Puts it into a proxy CarDealer obj
        3. Creates and returns a list of those proxies.
    """
    results = []
    json_result = get_request(url, **kwargs)
    # Check for "required" kwargs then make request
    if 'state' in kwargs:
        json_result = get_request(url, state=kwargs.get('state'))
        print(json_result)
    else:
        print('State is not supplied in kwargs.')
        results.append('Could not execute request: missing state ')
    return results

    # Continue with business


'''
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, **kwargs):
    # Call get_request with a URL parameter
    results = []
    json_result = get_request(url, **kwargs)
    if 'id' in kwargs:
        json_result = get_request(url, id=kwargs.get('id'))
        print(json_result)
    else:
        print('id is not supplied in kwargs.')
        results.append('Could not execute request: missing id')
    print(results)
    return results
'''

'''
def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        print(dealers)

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"],
                                       city=dealer_doc["city"],
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"],
                                       lat=dealer_doc["lat"],
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"],
                                       zip=dealer_doc["zip"])
                results.append(dealer_obj)

    return results

'''


def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 84', json_result)
    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"], full_name=dealer_doc["full_name"],

                               st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj



# def get_dealer_by_id_from_cf(url, dealerId):

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

# Check for "required" kwargs then make request/ the function must be completed



def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print(json_result)
    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                      name=dealer_review["name"],
                                      purchase=dealer_review["purchase"],
                                      review=dealer_review["review"],
                                      id=dealer_review["id"],
                                      purchase_date=dealer_review["purchase_date"],
                                      car_make=dealer_review["car_make"],
                                      car_model=dealer_review["car_model"],
                                      car_year=dealer_review["car_year"],
                                      sentiment=analyze_review_sentiments(dealer_review["review"]))


#            sentiment = analyze_review_sentiments(review_obj.review)
#            print(sentiment)
#            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/fa5b4f08-3331-42db-9b16-d8bea709fcc4"
    api_key = "1A-pbDCxIORohTIYyZeg4b7bddHET7RWk8kW8fBzYG79"
    authenticator = IAMAuthenticator(api_key)
    nlp_server = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    nlp_server.set_service_url(url)
    features = ["sentiment"]
    version = "2021-08-01"
    response = nlp_server.analyze(text=review, features=Features(
        sentiment=SentimentOptions(targets=[review]))).get_result()
    sentiment = response['sentiment']['document']['label']
    return sentiment

# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
