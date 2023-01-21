from django.db import models
import sys
from django.conf import settings
import datetime
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
import json


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default='New Model')
    description = models.CharField(max_length=1000)
    establish_date = models.DateField(null=True)


def __str__(self) -> str:
    return self.name + " - " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:

class CarModel(models.Model):
    carMakeId = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    carMakeName = models.CharField(null=False, max_length=30, default='Make')
    dealership = models.IntegerField(null=False, default=-1)
    name = models.CharField(null=False, max_length=30, default='New Car Model')
    SEDAN = 'sedan'
    SUV = "suv"
    WAGON = "wagon"
    MODEL_CHOICES = [
        (SEDAN, "sedan"),
        (SUV, "suv"),
        (WAGON, "wagon")
    ]
    model = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_CHOICES,
        default=SUV
    )
    year = models.IntegerField()
    YEAR_CHOICES = []
    for r in range(1969, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return "Name: " + str(self.name) + "," + \
                "Car Type: " + str(self.model) + "," + str(self.year)
'''
class CarModel(models.Model):
    mdid = models.SmallIntegerField(primary_key=True, default=1)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, default=1)
    name = models.CharField(null=False, max_length=25)
    dealership = models.IntegerField(null=False, default=0) # dealer id is "dealership" in the db.

    # define choices for car type
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    COUPE = 'coupe'
    HATCH = 'hatchback'
    CONVERT = 'convertible'
    VANS = 'vans'
    SPORTS = 'sports'
    MUSCLE = 'muscle'
    SUPER = 'super'
    ELECTRIC = 'electric'
    LIMO = 'limo'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Station Wagon'),
        (COUPE, 'Coupe'),
        (HATCH, 'Hatchback'),
        (CONVERT, 'Convertible'),
        (VANS, 'Van / Minivan'),
        (SPORTS, 'Sports Car'),
        (MUSCLE, 'Muscle Car'),
        (SUPER, 'Super Car'),
        (ELECTRIC, 'Electric Car'),
        (LIMO, 'Limousine')
    ]
    car_type = models.CharField(
        max_length = 15,
        choices = CAR_TYPE_CHOICES,
        default = COUPE
    )
    car_year = models.DateField() #DateTime obj and not a string..

    def __str__(self) -> str:
        return self.name + ": " + str(self.car_year.year) + " - " + self.car_type
'''


# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self) -> str:
        return self.dealership + ": " + self.name + " - " + self.review