class Book:
    def __init__(self, title, author, edition, year):
        self.title = title
        self.author = author
        self.edition = edition
        self.year = year

    def __str__(self):
        return f"'{self.title}' by {self.author}"
    
    def condition(self):
        if self.edition < 1:
            return "Poor"
        elif self.edition < 3:
            return "Fair"
        elif self.edition < 5:
            return "Good"
        else:
            return "Excellent"
        
class Ebook(Book):
    def __init__(self, title, author, edition, year, file_size):
        super().__init__(title, author, edition, year)
        self.file_size = file_size

    def __str__(self):
        return f"{super().__str__()} (Ebook, {self.file_size}MB)"
    
class Audiobook(Book):
    def __init__(self, title, author, edition, year, duration):
        super().__init__(title, author, edition, year)
        self.duration = duration

    def __str__(self):
        return f"{super().__str__()} (Audiobook, {self.duration} hours)"

b1 = Book("OOP python", "George Orwell", 1, 1949)
e1 = Ebook("OOP python", "George Orwell", 2, 1949, 5)
print(b1.condition())
print(e1)