import sys
import util
import rpsBots

class Simulation():
    def __init__(self, bot1, bot2):
        """ ----------------------- """
        self.bot1 = bot1
        self.bot2 = bot2
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}
        self.results = []

    def reset(self):
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}

    def simulate(self, rounds=1000):
        self.reset() # reset the scores for new game

        # rounds = 1000 if rounds == None else rounds
        sys.stdout.write('\tStarting the %s-round simulation....' % rounds)
        sys.stdout.flush()

        for _ in range(rounds):
            outcome = util.CHECK_WINNER[(self.bot1.playTurn(),
                                         self.bot2.playTurn())]
            while outcome == 'tie':
                outcome = util.CHECK_WINNER[(self.bot1.playTie(),
                                             self.bot2.playTie())]
            self.results.append(outcome)
            self.score[outcome] += 1
        print 'Done!\n'

    def singleGame(self):
        sys.stdout.write('Starting the single game of simulation....\n\n')
        sys.stdout.flush()

        cleanOutcome = {}
        cleanOutcome['bot1'] = '%s Wins!' % self.bot1.name
        cleanOutcome['bot2'] = '%s Wins!' % self.bot2.name
        cleanOutcome['tie'] = 'It\'s a tie!'

        play1 = self.bot1.playTurn()
        play2 = self.bot2.playTurn()
        outcome = util.CHECK_WINNER[(play1, play2)]
        print '\t%s played: %s \t\t%s played: %s' % (self.bot1.name, play1, self.bot2.name, play2)
        print '\t\t\tOutcome: %s' % cleanOutcome[outcome]

    def __repr__(self):
        ''' overloading of print method for Simulation class '''
        string = '\tAnd the winner is...\n'
        string += '\t\t%s: \t%s\n' % (self.bot1.name, self.score['bot1'])
        string += '\t\t%s: \t%s\n' % (self.bot2.name, self.score['bot2'])
        return string
