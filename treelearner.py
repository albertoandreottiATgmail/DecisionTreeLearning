
"""
    TreeLearner
"""
from classifier import Classifier
from math import log
from rule import Rule
import random


class TreeLearner(Classifier):
    
    def __init__(self, treshold, target, prate):  # pylint: disable=E1002
        
        self._treshold = treshold
        self._targetVal = target
        self._samples = []
        
        self._pruning_rate = prate
        self._prunset = []
         
        
    def addSample(self, sample):
        self._samples.append(sample)
    
    def setTarget(self, target):
        assert(target in self._samples[0][0].getValues())
        self._targetVal = target
        
    # 'parameters' would be used to tell which features we can use
    def infer(self, parameters):        
        
        self._parameters = parameters
        
        #TODO:this one should be in constructor
        self._targetAtt = parameters[0].getName()
        
        #mark the target as used
        used = [True] + [False]*(len(parameters) - 1)
        
        #separate the pruning dataset, is this really unbiased?
        size = int(self._pruning_rate * len(self._samples))
        for dummy in xrange(size):
            rndidx = random.randint(0, len(self._samples) - 1)
            self._prunset.append(self._samples[rndidx])
            self._samples.remove(self._samples[rndidx])
        
        #check the proportion of training and pruning
        assert(abs((float(len(self._samples))/len(self._prunset)) - 1.0) < 0.1)
        
        return self._growTree(self._samples, used)
        
    def _growTree(self, dataset, used):
        
        if(len(dataset) == 0):
            return Leaf(0, '','')
        #all positive
        if(len(filter(lambda x: x[0] != self._targetVal, dataset))==0):
            return Leaf(1, self._targetAtt, self._targetVal)    
        #all negative
        if(len(filter(lambda x: x[0] == self._targetVal, dataset))==0):
            return Leaf(1, self._targetAtt, 'other')
        
        #we run out of parameters and still classification is not good.
        #TODO: apply threshold 
        if(reduce(lambda x, y: x and y, used)):
            return Leaf(0, '', '')
        
        # idx: location of the attribute in _samples, 
        idx = self._chooseBestAttribute(dataset, used)
        node = Node()
        used[idx] = True
        
        #split the data in as many subsets as values has the attribute.
        for value in self._parameters[idx].getValues():
            chunk = [it for it in dataset if it[idx] == value] 
            child = self._growTree(chunk, list(used))
            child.addAttVal(self._parameters[idx].getName(), value)
            node.addChild(child)
       
        return node
     
    def _chooseBestAttribute(self, dataset, used):
        assert(used[0] == True)
        
        minfo = [0] * len(self._parameters)
        
        #compute mutual information between the class and each attribute
        for idx in range(0, len(self._parameters)):
            if not used[idx]:
                for value in self._parameters[idx].getValues():
                    subset = filter(lambda x: x[idx]==value, dataset)
                    val_prob = float(len(subset))/len(dataset)
                    if val_prob == 0:
                        continue
                    
                    #compute entropy
                    entropy = 0
                    for target in self._parameters[0].getValues():
                        prob = float(len(filter(lambda x: x[0] == target, subset)))/len(subset)
                        entropy += prob * log(prob + 0.00001) 
                    
                    #-P(B=b).H(A|B=b)
                    minfo[idx] += -val_prob * entropy
            else:
                #attributes already used must lose.
                minfo[idx] = float("inf")

        #do the actual choice according to minfo
        print minfo
        return min(enumerate(minfo), key=lambda x: x[1])[0]
    
    def prune(self, rules):
        prunedRules = map(lambda x: x.prune(self._prunset, self._parameters), rules)
        return list(set(prunedRules))

            
class Node(object):
    
    def __init__(self):
        self._children = []
        self._att = self._val = ''
        
    def addChild(self, child):
        self._children.append(child)
        
    #Depth first search to collect rules
    def _addClause(self):
        
        children_list = []
        for child in self._children:
            children_list = children_list + child._addClause()
        
        #children_list = filter(lambda x: x != None, children_list)
        #Add my clause to every rule
        local_result = []
        for rule in children_list:
            local_result.append(rule.addClause(self._att, self._val))        
        
        return local_result
    
    #Better interface to not expose recursion to clients
    def getRules(self):
        return self._addClause()
        
    def addAttVal(self, att, val):
        self._att = att
        self._val = val
    
class Leaf(Node):

    def __init__(self, pos, targetAtt, targetVal):
        self._outcome = pos
        self._targetAtt = targetAtt
        self._targetVal = targetVal
    
    def _addClause(self):
        
        if self._outcome is 1:
            rule = Rule(self._targetAtt, self._targetVal)
            return [rule.addClause(self._att, self._val)] 
        return []
        
