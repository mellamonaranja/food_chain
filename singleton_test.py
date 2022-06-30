class Counter():
    def __init__(self, value=0): #instance 1, self is variable
        self.value=value 
    def increment(self, delta=1): #instance 2
        self.value+=delta
    def decrement(self, delta=1): #instance 3
        self.value-=delta
        
# instance method must create instance first
# and then call that instance
# auto allocates first variable

class User:
    def __init__(self, email, password):
        self.email=email
        self.password=password
        
    @classmethod #declare the method to class, this is class method
    def fromTuple(cls, tup): #class is variable, it called as cls
        return cls(tup[0], tup[1])
    
    @classmethod
    def fromDictionary(cls, dic):
        return cls(dic['email'], dic['password'])
    
# user=User('google@google.com','1234')
# print(user.email, user.password)

# user=User.fromTuple(('google@google.com','1234'))
# print(user.email, user.password)

class StringUtils: #there is no init variable
    @staticmethod
    def toCamelcase(text):
        words=iter(text.split("_"))
        return next(words)+"".join(i.title() for i in words)
    
    @staticmethod
    def toSnakecase(text):
        letters=["_"+i.lower() if i.isupper() else i for i in text]
        return "".join(letters).lstrip("_")
    
print(StringUtils.toCamelcase('last_modified_date'))
print(StringUtils.toSnakecase('last_modified_date'))