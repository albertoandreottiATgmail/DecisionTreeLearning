"""
    Testing: random data, arbitrary rules.

"""
from dataManagement import Attribute, RandomAttribute, SampleSet, RandomAttributeFactory
from ruleslearner import RulesLearner

#prepare the data set
mySet = SampleSet()

#the set of attributes that are correlated
att1 = RandomAttribute("WiFi")
att2 = RandomAttribute("time")
att3 = RandomAttribute("location")

#declare attributes
att1.add("off", "on")
att2.add("morning", "afternoon", "evening", "night")
att3.add("home", "work", "other")

#add the attributes
mySet.addDefinition(att1)  # wifi
mySet.addDefinition(att2)  # time
mySet.addDefinition(att3)  # location
parameters = [att1, att2, att3]

#add 10 random attributes
random_factory = RandomAttributeFactory(1000)
for idx in range(1, 10):
    rndatt = random_factory.getNext()
    parameters.append(rndatt)
    mySet.addDefinition(rndatt)
    
#select classifier
learner = RulesLearner('tree_learner', mySet, 'on')
learner.setTemplateRuleLearnerName("[WiFi] <= When [Location] ")
learner.setFieldNames(map(str, parameters))

print map(str, parameters)

# [on] <= When [morning, home] 
for a in range(1,300):
    learner.addSample(['on', 'morning', 'home'] + map( lambda x: x.sample(), parameters[3:]), parameters)

# [off] <= When [morning, work] 
for a in range(1,200):
    learner.addSample(['off', 'morning', 'work'] + map( lambda x: x.sample(), parameters[3:]), parameters)

# [on] <= When [afternoon, work] 
for a in range(1,200):
    learner.addSample(['on', 'afternoon', 'work'] + map( lambda x: x.sample(), parameters[3:]), parameters)

# [off] <= When [night, home]
for a in range(1,200):
    learner.addSample(['off', 'night', 'home'] + map( lambda x: x.sample(), parameters[3:]), parameters)

# add some random noise 
for a in range(1, 70):
    learner.addSample(map( lambda x: x.sample(), parameters), parameters)
    
rules = learner.infer(parameters)
for rule in rules:
    print rule
    