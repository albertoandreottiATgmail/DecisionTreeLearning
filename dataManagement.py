import random

# represents an attribute
class Attribute(object):

    def __init__(self, name):
        self._values = []
        self._name = name

    def add(self, *args):
        map(self._addSingle, args)
        
    def setName(self, name):
        self._name = name

    def _addSingle(self, value):
        #possible attribute values
        self._values.append(value)

    def getName(self):
        return self._name
    
    def getValues(self):
        return self._values

    def valueCount(self):
        return len(self._values)

    def __str__(self):
        return self._name

#generates attributes with random number of values, used for testing
class RandomAttributeFactory(object):

    def __init__(self, start):
        #The first attribute's id will be labeled 'start',
        #the second at start + 1, etc.
        self._next = start

    def getNext(self):
        #assign a random attribute name
        randomAtt = RandomAttribute('rand' + str(self._next))
        self._next = self._next + 1

        #assign a random number of values from 2 to 14
        str_list = map(str, range(1, random.randint(2, 5)))
        map(randomAtt.add, str_list)

        return randomAtt


class RandomAttribute(Attribute):

    def sample(self):
        return self._values[random.randint(0, self.valueCount() - 1)]
    
    def setValues(self, values):
        self._values = values

class SampleSet(object):

    def __init__(self):
        self._values = []

    def addDefinition(self, attribute):
        pass
