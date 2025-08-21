class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    
    def move(self):
        return f"The vehicle is moving."
    
class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        super().__init__(make, model, year)
        self.doors = doors

    def __str__(self):
        return f"{super().__str__()} with {self.doors} doors"
    
    def move(self):
        return f"The car is driving on the road."
    
class Boat(Vehicle):
    def __init__(self, make, model, year, length):
        super().__init__(make, model, year)
        self.length = length

    def __str__(self):
        return f"{super().__str__()} ({self.length} feet long)"
    
    def move(self):
        return f"The boat is sailing on the water."
    
class Plane(Vehicle):
    def __init__(self, make, model, year, wingspan):
        super().__init__(make, model, year)
        self.wingspan = wingspan

    def __str__(self):
        return f"{super().__str__()} with a wingspan of {self.wingspan} feet"
    
    def move(self):
        return f"The plane is flying in the sky."
    
c1 = Car("Toyota", "Camry", 2020, 4)
b1 = Boat("Yamaha", "242X", 2021, 24)
p1 = Plane("Boeing", "747", 2019, 68)

print(c1.move())
print(b1.move())
print(p1.move())