from django.db import models
import sys
from django.conf import settings

from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

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

    def __str__(self):
        return "Name: " + str(self.name) + "," + \
               "Description: " + str(self.description) + "," + \
               "Date:" + str(self.establish_date)


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    carMakeId = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    carMakeName = models.CharField(null=False, max_length=30, default='New Model')
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

    def __str__(self):
        return "Name: " + str(self.name) + "," + \
               "Carmake ID" + str(self.carMakeId) + "," + \
               "Car Make Name:" + str(self.carMakeName) + "," + \
               "Dealership ID" + str(self.dealership) + ","
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
