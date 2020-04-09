class person:

    def __init__(self, age, gender, name):
        self.age = age
        self.gender = gender
        self.name = name

    def sayName(self):
        print("My name is {}".format(self.name))

    def sayAge(self):
        print("I am {} years old.".format(self.age))

if __name__ == "__main__":
    chenelle = person(22, 'FEMALE', 'Chenelle')
    chenelle.sayName()
