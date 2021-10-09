from django.db import models
from django.utils.timezone import now

# Car Make model:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=40, default='undefined')
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
    # Dealer ID has been defined as a string both here and in the IBM clodclud functions
    # This has been a deliberate change in order to take advantage of the autogeneration of IDs
    # done by Cloudant database
    dealer_id = models.CharField(null=False, max_length=40, default='undefined')
    name = models.CharField(null=False, max_length=40, default='undefined')
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
class CarDealer:
    def __init__(self, id, short_name, full_name, address, city, st, state, zip, lat, long):
        # Dealer ID has been defined as a string both here and in the IBM clodclud functions
        # This has been a deliberate change in order to take advantage of the autogeneration of IDs
        # done by Cloudant database
        self.id = id
        self.short_name = short_name
        self.full_name = full_name
        self.address = address
        self.city = city
        self.st = st
        self.state = state
        self.zip = zip
        self.lat = lat
        self.long = long

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, name, review, purchase, car_make, car_model, car_year, purchase_date, sentiment):
        # Dealer ID has been defined as a string both here and in the IBM clodclud functions
        # This has been a deliberate change in order to take advantage of the autogeneration of IDs
        # done by Cloudant database
        self.id = id
        self.name = name
        self.review = review
        self.purchase = purchase
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.purchase_date = purchase_date
        self.sentiment = sentiment

    def __str__(self):
        return "Dealer name: " + self.full_name
