
"""
    SequentialLearner
"""

from classifier import Classifier

class SequentialLearner(Classifier):

    def __init__(self, treshold):  # pylint: disable=E1002
        self._treshold = treshold

