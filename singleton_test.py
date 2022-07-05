# from abc import ABCMeta, abstractclassmethod 

# class IPerson(metaclass=ABCMeta):
#     @abstractclassmethod
#     def print_data():
#         """implement in child class
#         """

# class PersonSingleton(IPerson):
#     __instance=None 

#     @staticmethod
#     def get_instance():
#         if PersonSingleton.__instance==None:
#             PersonSingleton('Default name', 0)
#         return PersonSingleton.__instance 
 

#     def __init__(self, name, age): #this constructor cannot be used multiple times then we would always override the instance
#         if PersonSingleton.__instance!=None:
#             raise Exception('Signgleton cannot be instantiated more than once')
#         else:
#             self.name=name
#             self.age=age
#             PersonSingleton.__instance=self #it gets assigned above as '__instance=None'
    
#     @staticmethod        
#     def print_data():
#         print(f"Name:{PersonSingleton.__instance.name}, Age:{PersonSingleton.__instance.age}")
        
# p=PersonSingleton('joohyun',30)
# print(p)
# p.print_data()

# # p2=PersonSingleton('joo',31)
# # print(p2)
# # p2.print_data()

# p3=PersonSingleton.get_instance()
# print(p3)
# p3.print_data()

class Point():
    def __new__(cls, *args, **kwargs):
        print('__new__')
        print(cls)
        print(args)
        print(kwargs)
        obj=super().__new__(cls)
        return obj
    def __init__(self, x=0, y=0):
        print('__init__')
        self.x=x
        self.y=y
        
p=Point(3,4)
print(p)

class RectPoint(Point):
    MAX_Inst=4
    Inst_created=0
    def __new__(cls, *args, **kwargs):
