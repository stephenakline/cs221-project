import random
import copy
import numpy
import util

class Bot():
    def __init__(self, name):
        ''' initialize RPS Bot that is based only on order '''
        self.name = name
        self.strategy = []
        self.probs = {}
        self.index = 0
        self.readStrategy()

    def readStrategy(self):
        textFile = open('opponents/%s.txt' % self.name, 'r')
        self.name = textFile.readline().strip()
        self.probs['scissor'] = float(textFile.readline().split()[1])
        self.probs['paper'] = float(textFile.readline().split()[1])
        self.probs['rock'] = float(textFile.readline().split()[1])
        num = int(textFile.readline().strip())
        for _ in range(num):
            self.strategy.append(textFile.readline().strip())

    def playTurn(self):
        choice = self.strategy[self.index]
        self.index = self.index + 1 if self.index + 1 < len(self.strategy) else 0
        return choice

    def playTie(self):
        return self.playTurn()

    def __repr__(self):
        ''' overloading of print method '''
        string = '%s plays a random strategy with probabilities:\n'
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
        self.name = 'Baseline'
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
        self.name = 'Oracle'
        self.opponent = opponent
        self.oppProbs = None
        self.index = 0

    def deviseStrategy(self):
        self.oppProbs = copy.deepcopy(self.opponent.probs)
        self.oppProbs.update((x, y * self.opponent.probsWeight) for x, y in self.oppProbs.items())

    def playTurn(self):
        self.deviseStrategy()
        self.oppProbs[self.playStrategy()] += self.opponent.strategyWeight
        return max(self.oppProbs, key=self.oppProbs.get)

    def playTie(self):
        return self.playTurn()

    def playStrategy(self):
        opponentChoice = self.opponent.strategy[self.index]
        response = util.ORACLE_STRATEGY[opponentChoice]
        self.index = self.index + 1 if self.index + 1 < len(self.opponent.strategy) else 0
        return response

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Oracle plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.probs:
            string += '\t%s: %.2f\n' % (i, self.probs[i])
        return string

class Master():
    def __init__(self):
        ''' initialize Master Bot '''
        self.history = []

    def playTurn(self):
        raise Exception("Not implemented yet")

    def playTie(self):
        raise Exception("Not implemented yet")

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Master plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.probs:
            string += '\t%s: %.2f\n' % (i, self.probs[i])
        return string
