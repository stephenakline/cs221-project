import sys
import util
import rpsBots

class Simulation():
    def __init__(self, bot1, bot2, rounds):
        """ ----------------------- """
        self.bot1 = bot1
        self.bot2 = bot2
        self.rounds = rounds
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}
        self.results = []

    def reset(self):
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}

    def simulate(self, rounds=None):
        self.reset() # reset the scores for new game

        rounds = self.rounds if rounds == None else rounds
        sys.stdout.write('Starting the %s-round simulation....' % rounds)
        sys.stdout.flush()

        for _ in range(rounds):
            outcome = util.CHECK_WINNER[(self.bot1.playTurn(),
                                         self.bot2.playTurn())]
            while outcome == 'tie':
                outcome = util.CHECK_WINNER[(self.bot1.playTie(),
                                             self.bot2.playTie())]
            self.results.append(outcome)
            self.score[outcome] += 1
        print 'Done!'

    def singleGame(self):
        sys.stdout.write('Starting the single game of simulation....\n\n')
        sys.stdout.flush()

        cleanOutcome = {}
        cleanOutcome['bot1'] = 'Player 1 Wins!'
        cleanOutcome['bot2'] = 'Player 2 Wins!'
        cleanOutcome['tie'] = 'It\'s a tie!'

        play1 = self.bot1.playTurn()
        play2 = self.bot2.playTurn()
        outcome = util.CHECK_WINNER[(play1, play2)]
        self.score[outcome] += 1
        print '\tPlayer 1 played: %s \t\tPlayer 2 played: %s' % (play1, play2)
        print '\t\t\tOutcome: %s' % cleanOutcome[outcome]
        print '\nCurrent Score:'
        print '\tPlayer 1: %s wins \t\tPlayer 2: %s wins' % (self.score['bot1'], self.score['bot2'])

    def __repr__(self):
        ''' overloading of print method for Simulation class '''
        string = 'And the winner is...\n'
        string += '\tBot1: %s\n' % self.score['bot1']
        string += '\tBot2: %s\n' % self.score['bot2']
        return string
