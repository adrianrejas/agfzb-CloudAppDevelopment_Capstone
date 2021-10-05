from django.db import models
from django.utils.timezone import now

# Car Make model:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='undefined')
    description = models.TextField(null=True)
    def __str__(self):
        return self.name + ": " + self.description

# Create a Car Model model:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(null=False, max_length=30, default='undefined')
    COUPE = 'Coupe'
    SEDAN = 'Sedan'
    SPORTS = 'Sports'
    SUV = 'SUV'
    TRUCK = 'TRUCK'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (COUPE, 'Coupe'),
        (SEDAN, 'Sedan'),
        (SPORTS, 'Sports'),
        (SUV, 'SUV'),
        (TRUCK, 'TRUCK'),
        (WAGON, 'Wagon'),
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=COUPE
    )
    year = models.DateField(null=False)
    def yearpublished(self):
        return self.year.strftime('%Y')
    def __str__(self):
        return self.car_make.name + " " + self.name + ", " + \
                str(self.yearpublished()) + " " + self.type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
