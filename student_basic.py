student = {"name": "Alice", "age": 20, "grade": "A"}  #dictionary
print(student["name"])

def greet(name):                #def is a built-in function in python that is used to define a function.
    print("Hello", name)

greet("Bob")

user_name = input("Enter your name: ")     #
print("Hello", user_name)

age = 18    #if and else are built-in functions in python that are used to check if a condition is true or false.
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")


#range is a built-in function in python that returns a sequence of numbers.
for i in range(5):
    print("Number:", i)

for i in range(1,6):
    print("Number:", i)

fruits = ["apple", "banana", "mango"]    #list
print(fruits[0])
fruits.append("cherry")
print(fruits)


class Person:
    def __init__(self, name, age):  # constructor
        self.name = name
        self.age = age

    def introduce(self):            #self is a built-in function in python that is used to refer to the object itself.  
        print("Hi, I'm", self.name)

p1 = Person("satheesh", 25)         #p1 is an object of the class Person.
p1.introduce()

class Person:
    def __init__(self, name, age):  
        self.name = name
        self.age = age

    def introduce(self):
        print("Hi, I'm", self.name, "and I'm", self.age, "years old.")

# Create multiple objects
p1 = Person("Satheesh", 25)
p2 = Person("Deepika", 24)
p3 = Person("Ananth", 30)

# Each object keeps its own values
p1.introduce()
p2.introduce()
p3.introduce()

num1 = float(input("Enter first number: ")) #calculator
num2 = float(input("Enter second number: "))
operation = input("Choose (+, -, *, /): ")

if operation == "+":
    print("Result:", num1 + num2)
elif operation == "-":
    print("Result:", num1 - num2)
elif operation == "*":
    print("Result:", num1 * num2)
elif operation == "/":
    print("Result:", num1 / num2)
else:
    print("Invalid operation")


word = input("Enter a word: ") #reverse a word
print("Reversed:", word[::-1])


fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple
print(fruits[1])   # banana
fruits.append("mango")   # add
print(fruits)

fruits.remove("banana")  # remove
print(fruits)