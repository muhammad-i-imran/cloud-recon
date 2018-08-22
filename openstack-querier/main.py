from openstackqueryapi import Object

import json

class Bar(object):
    def __init__(self):
        self.nested = 100

class Foo(object):
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 500
        bar1 = Bar()
        bar1.nested = 500000
        self.bar = json.dumps(bar1.__dict__)
        # self.bar.abc = 10001

foo = Foo()
# s = json.dumps(foo) # raises TypeError with "is not JSON serializable"

s = json.dumps(foo.__dict__) # s set to: {"x":1, "y":2}

print(s)
#
# if __name__ == '__main__':
#     me = Object()
#     me.name = "Onur"
#     me.age = 35
#     me.dog = Object()
#     me.dog.name = "Apollo"
#
#     print(me.toJSON())
#
