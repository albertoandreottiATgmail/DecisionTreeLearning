

class Classifier(object):

    def infer(self):
        raise NotImplementedError("Please Implement this method")

    def addSample(self, sample):
        raise NotImplementedError("Please Implement this method")

    def getNumberOfSamples(self):
        raise NotImplementedError("Please Implement this method")

    def getAction(self):
        #raise NotImplementedError("Please Implement this method")
        return "Any"
