import random
import copy
import numpy
import util
import operator
import sys

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

class BotV2():
    def __init__(self):
        ''' initialize BotV2 '''
        self.name = 'BotV2'
        self.counts = {'rock': 100, 'paper': 100, 'scissor': 100}
        self.delta = 1

    def resetProb(self):
        self.counts = {'rock': 100, 'paper': 100, 'scissor': 100}

    def incorporatePlay(self, play, outcome):
        oldTotal = sum(self.counts.values())
        if outcome == 'bot1':
            self.counts[play] += (win * self.delta)
        else:
            for i in self.counts:
                if i != play:
                    self.counts[play] += (self.delta / float(2))
        newTotal = sum(self.counts.values())
        for i in self.counts:
            self.counts[i] = float(oldTotal * self.counts[i]) / float(newTotal)
        print self.counts, sum(self.counts.values())

    def playTurn(self):
        probs = [float(i) / sum(self.counts.values()) for i in self.counts.values()]
        choice = numpy.random.choice(numpy.arange(1, 4), p = probs)
        return self.counts.keys()[choice - 1]

    def playTie(self):
        return self.playTurn()

    def __repr__(self):
        ''' overloading of print method '''
        string = 'BotV2 plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.counts:
            string += '\t%s: %.2f\n' % (i, self.counts[i])
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

class Human():
    def __init__(self):
        self.name = 'Human'

    def playTurn(self):
        sys.stdout.write('\n>> Enter your next play: ')
        line = sys.stdin.readline().strip()
        if line == 'r' or line == 'rock':
            return 'rock'
        if line == 'p' or line == 'paper':
            return 'paper'
        if line == 's' or line == 'scissor':
            return 'scissor'

    def playTie(self):
        return self.playTurn()

class Master():
    def __init__(self, n = 10, p = 4):
        ''' initialize Master Bot '''
        self.history = []
        self.name = 'Master R2P5'
        self.memoryLength = int(n)
        self.totalNumRounds = 1000
        self.state = ([],0,{'rock':0, 'paper':0, 'scissor': 0})
        self.patternLength = int(p)

    def isEnd(self, state):
        return state[1] == self.totalNumRounds

    def incorporatePlay(self, play):
        prevPlays = self.state[0]
        countPlays = self.state[1]
        dictPlays = self.state[2]
        prevPlays += [play]
        if len(prevPlays) > self.memoryLength:
            prevPlays.pop(0)
        countPlays += 1
        dictPlays[play] += 1
        self.state = (prevPlays, countPlays, dictPlays)

    def playTurn(self):
        def play(p):
            state = self.state
            if p == 0:
                probs = state[2]

                if sum(probs.values()) != 0:
                    maxPlayed, _ = sorted(probs.items(), key=operator.itemgetter(1), reverse = True)[0]
                    # print 'most played:', maxPlayed
                    resp1 = util.ORACLE_STRATEGY[maxPlayed]
                    # print 'will play:', resp1
                    return resp1
                else:
                    choice = numpy.random.choice([0,1,2])
                    resp2 = probs.keys()[choice]
                    # print 'will randomly play:', resp2
                    return resp2
            elif len(state[0]) < p:
                return play(p-1)
            else:
                # print 'p == ', p
                n = len(state[0])
                count = {'rock':0, 'paper':0, 'scissor': 0}
                curr = state[0][-p:]
                # print 'analyzing current pattern of size %i: %s' %(p, curr)
                for k in range(n-p-1):
                    if state[0][k : (k + p)] == curr:
                        count[state[0][k+p]] += 1
                # print 'count', count
                if sum(count.values()) != 0:
                    nextPlay, _ = sorted(count.items(), key=operator.itemgetter(1), reverse = True)[0]
                    resp = util.ORACLE_STRATEGY[nextPlay]
                    # print 'pattern of size %i: %s recognized, will thus play %s to beat expected play of %s' % (p, curr, resp, nextPlay)
                    return resp
                else:
                    # print 'pattern not found'
                    return play(p-1)

        # print '\nMaster is thinking'
        p_init = self.patternLength
        return play(p_init)


    def playTie(self):
        return self.playTurn()

    def __repr__(self):
        ''' overloading of print method '''
        string = 'Master plays the following way:\n'
        string += '- the following frequencies:\n'
        for i in self.probs:
            string += '\t%s: %.2f\n' % (i, self.probs[i])
        return string
