"""

Rules Learner

"""

from fulllikelihood import FullLikelihood
from treelearner import TreeLearner
from sequentiallearner import SequentialLearner


class RulesLearner(object):

    _supported = {'full_likelihood': FullLikelihood,
                  'tree_learner': TreeLearner,
                  'sequential_learner': SequentialLearner}

    def __init__(self, classifier_type, set, tvalue):  # pylint: disable=E1002

        self._tvalue = tvalue
        self._target = 'target'
        
        #fail if wrong argument
        if classifier_type not in self._supported.keys():
            raise ValueError("Classifier must be one of" + self._supported.keys())
        
        #This should be done only with tree learner
        prunning_rate = 0.5
        self._learner = self._supported.get(classifier_type)(1, tvalue, prunning_rate)
        

    def setTemplateRuleLearnerName(self, name):
        pass

    def getLearner(self):
        return self._learner

    def getAction(self):
        pass  # should ask the classifier

    def setTreshold(self, value):
        pass

    def setMinSamples(self, value):
        pass

    def addSample(self, value, parameters):
        assert(len(value) == len(parameters))
        self._learner.addSample(value)

    # update rules states
    def computeLearning(self, params):
        pass

    # return the most best rule
    def infer(self, params):
        
        node = self._learner.infer(params)
        node.addAttVal('root', 'node')
        return self._learner.prune(node.getRules())

    def setFieldNames(self, names):
        pass
