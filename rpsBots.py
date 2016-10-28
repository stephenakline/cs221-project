import random
import numpy
import util

class Bot():
    def __init__(self, probs, strategy, probWeight, strategyWeight):
        ''' initialize RPS Bot that is based only on order '''
        self.probs = probs
        self.strategy = strategy
        self.probsWeight = probWeight
        self.strategyWeight = strategyWeight
        self.index = 0

    def playTurn(self):
        playType = numpy.random.choice(numpy.arange(1, 3), \
                p = [self.probsWeight, self.strategyWeight])
        choice = self.playProbabilities() if playType == 1 else self.playStrategy()
        return choice

    def playTie(self):
        return self.playTurn()

    def playStrategy(self):
        choice = self.strategy[self.index]
        self.index = self.index + 1 if self.index + 1 < len(self.strategy) else 0
        return choice

    def playProbabilities(self):
        choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
        return self.probs.keys()[choice - 1]

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Bot plays the following way:\n'
        if self.probsWeight != 0:
            string += '- the following frequencies:\n'
            for i in self.probs:
                string += '\t%s: %.2f\n' % (i, self.probs[i])
        if self.strategyWeight != 0:
            string += '- the following strategy:\n\t'
            for i in self.strategy:
                string += i + ' '
        return string

class Baseline():
    def __init__(self):
        ''' initialize Baseline Bot '''
        self.probs = {'rock': .33, 'paper': .33, 'scissor': (1-.33-.33)}
        self.strategy = None
        self.probsWeight = 1
        self.strategyWeight = 0
        self.index = 0

    def playTurn(self):
        choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
        return self.probs.keys()[choice - 1]

    def playTie(self):
        return self.playTurn()

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Basline plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.probs:
            string += '\t%s: %.2f\n' % (i, self.probs[i])
        return string

class Oracle():
    def __init__(self, opponent):
        ''' initialize Oracle Bot '''
        self.opponent = opponent
        self.probsDecision = None
        self.probsWeight = None
        self.strategyWeight = None
        self.index = 0
        self.deviseStrategy()

    def deviseStrategy(self):
        if self.opponent.probsWeight == 1:
            opponentChoice = max(self.opponent.probs, key=self.opponent.probs.get)
            self.probsDecision = util.ORACLE_STRATEGY[opponentChoice]
            self.probsWeight = 1; self.strategyWeight = 0
        elif self.opponent.strategyWeight == 1:
            self.probsWeight = 0; self.strategyWeight = 1

    def playTurn(self):
        playType = numpy.random.choice(numpy.arange(1, 3), \
                p = [self.probsWeight, self.strategyWeight])
        choice = self.probsDecision if playType == 1 else self.playStrategy()
        return choice

    def playTie(self):
        return self.playTurn()

    def playStrategy(self):
        opponentChoice = self.opponent.strategy[self.index]
        response = util.ORACLE_STRATEGY[opponentChoice]
        self.index = self.index + 1 if self.index + 1 < len(self.opponent.strategy) else 0
        return response

    def playProbabilities(self):
        choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
        return self.probs.keys()[choice - 1]

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Oracle plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.probs:
            string += '\t%s: %.2f\n' % (i, self.probs[i])
        return string
