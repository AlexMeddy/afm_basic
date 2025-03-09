import json

# a Python object (dict):

car = {
  "name": "honda",
  "age": 30,
  "price": 8000
}
person = {
    "name": "john",
    "age": 30,
    "city": "gold coast",
    "mycar": {"name": "honda",
              "age": 30,
              "price": 8000}, 
    
}
person2 = {
    "name": "john",
    "age": 30,
    "city": "gold coast",
    "mycar": car
    
}
# convert into JSON:
person2['mycar']['price'] = 10000

person_json = json.dumps(person2)
car_json = json.dumps(car)

# the result is a JSON string:
f2 = open("car_file.txt", "w")
f3 = open("person_file.txt", "w")
f2.write(car_json)
f3.write(person_json)
f2.close()
f3.close()
