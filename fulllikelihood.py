
"""
    FullLikelihood
"""
from classifier import Classifier


class FullLikelihood(Classifier):

    def __init__(self, treshold):  # pylint: disable=E1002
        self._treshold = treshold
