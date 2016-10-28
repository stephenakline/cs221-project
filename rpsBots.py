import random
import numpy

# IDEA: change this to 1 class where a bot has
#	- dictionary of frequencies
#	- strategy [an order of playing]
#	- a tie strategy
#	and a probability for each of the above
#	(to turn any bot into a strictly probability or strategy bot)

class Bot():
    def __init__(self, probs, probWeight, strategy, strategyWeight):
        ''' initialize RPS Bot that is based only on order '''
        self.probs       = probs
        self.strategy    = strategy
        self.probsWeight    = probWeight
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

# class OrderRPSBot():
#     def __init__(self, order):
#         ''' initialize RPS Bot that is based only on order '''
#         self.order = order
#         self.prior = list(order)
#
#     def playTurn(self):
#         choice = self.prior.pop(0)
#         self.prior.append(choice)
#         return choice
#
#     def playTie(self):
#         return self.playTurn()
#
#     def __repr__(self):
#         ''' overloading of print method '''
#         string = 'OrderRPSBot plays the following order:\n\t'
#         for i in self.order:
#             string += i + ' '
#         return string
#
# class ProbabilityRPSBot():
#     def __init__(self, probs):
#         ''' initialize RPS Bot that is based only on probabilities '''
#         self.probs = probs
#
#     def playTurn(self):
#         choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
#         return self.probs.keys()[choice - 1]
#
#     def playTie(self):
#         return self.playTurn()
#
#     def __repr__(self):
#         ''' overloading of print method '''
#         string = 'ProbabilityRPSBot plays with the following probabilities:\n'
#         for i in self.probs:
#             string += '\t%s: %.2f\n' % (i, self.probs[i])
#         return string
#
# class RandomProbabilityRPSBot():
#     def __init__(self):
#         ''' initialize RPS Bot that is based only on probabilities '''
#         rock = random.uniform(0, 1)
#         paper = random.uniform(0, 1 - rock)
#         scissor = 1 - rock - paper
#         self.probs = {'rock': rock, 'paper': paper, 'scissor': scissor}
#
#     def playTurn(self):
#         choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
#         return self.probs.keys()[choice - 1]
#
#     def playTie(self):
#         return self.playTurn()
#
#     def __repr__(self):
#         ''' overloading of print method '''
#         string = 'ProbabilityRPSBot plays with the following probabilities:\n'
#         for i in self.probs:
#             string += '\t%s: %.2f\n' % (i, self.probs[i])
#         return string
#
# class ProbabilityTieRPSBot():
#     def __init__(self, probs, tieStrategy):
#         ''' initialize RPS Bot that is based only on probabilities and tie strategy '''
#         self.probs = probs
#         self.tieStrategy = tieStrategy
#
#     def playTurn(self):
#         choice = numpy.random.choice(numpy.arange(1, 4), p = self.probs.values())
#         return self.probs.keys()[choice - 1]
#
#     def playTie(self):
#         return self.tieStrategy
#
#     def __repr__(self):
#         ''' overloading of print method '''
#         string = 'ProbabilityTieRPSBot plays with the following probabilities:\n'
#         for i in self.probs:
#             string += '\t%s: %.2f\n' % (i, self.probs[i])
#         string = 'Always plays %s after a tie.' % self.tieStrategy
#         return string
