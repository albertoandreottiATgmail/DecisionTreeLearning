"""
    Testing: very basic test of interfaces.

"""

from dataManagement import Attribute, SampleSet
from ruleslearner import RulesLearner

mySet = SampleSet()


#declare attributes
att = Attribute("WiFi")
att.add("off", "on")

att2 = Attribute("time")
att2.add("morning", "afternoon", "evening", "night")

att3 = Attribute("location")
att3.add("home", "work", "other")

#add the attributes
mySet.addDefinition(att)   # wifi
mySet.addDefinition(att3)  # location

#select classifier
learner = RulesLearner('full_likelihood', mySet)
learner.setTemplateRuleLearnerName("[WiFi] <= When [Location] ")

#not necessary as learner already has the set
#rule.learner = FullLikelihood(mySet)

print("Action " + learner.getAction())

parameters = [att.getName(), att3.getName()]

learner.setFieldNames(parameters)

learner.setTreshold(0.7)
learner.setMinSamples(2)

#add "on" <- "home", 4 times
sn1 = ["on", "home"]
map(learner.addSample, [sn1] * 4)

#add "off" <- "home", 1 times
s4 = ["off", "home"]
learner.addSample(s4)

#add "on" <- "work", 1 times
sn3 = ["on", "work"]
learner.addSample(sn3)

#add "off" <- "work", 2 times
s5 = ["off", "work"]
map(learner.addSample, [s5] * 2)

print("Likelihood: " + learner.getLearner.infer(parameters))

# Parameters: WiFi->location
learner.computeLearning(parameters)
learner.getLearner().getSamplesTable()
print("Likelihood: " + learner.infer(parameters))
