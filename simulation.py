import sys
import util
import datetime
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

class SimulationAgainstMaster():
    def __init__(self, bot1, bot2, record=False):
        """ ----------------------- """
        self.bot1 = bot1
        self.bot2 = bot2
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}
        self.results = []
        self.simulationResults = []
        self.record = record

    def reset(self):
        self.score = {'bot1': 0, 'bot2': 0, 'tie': 0}

    def printRound(self, play1, play2):
        if play1 == 'paper' and play2 == 'paper':
            print '     Human                Master'
            print '---------------      ---------------'
            print ''
            print '    --------             --------   '
            print '   /        /           /       /'
            print '  /        /     vs    /       /'
            print ' /        /           /       /'
            print '/        /           /       /'
            print '-------              --------'
            print ' Paper                 Paper'

        elif play1 == 'paper' and play2 == 'scissor':
            print '     Human                Master'
            print '---------------      ---------------'
            print ''
            print '     --------            \     /  '
            print '   /        /             \   /             '
            print '  /        /     vs        \ /       '
            print ' /        /                / \       '
            print '/        /               |  |  |     '
            print '-------                   -- --      '
            print ' Paper                   Scissor'

        elif play1 == 'paper' and play2 == 'rock':
            print '      Human               Master'
            print '---------------      ---------------'
            print ''
            print '     --------              _ _ _             '
            print '   /        /            /       \ '
            print '  /        /     vs     |         |'
            print ' /        /             |         |'
            print '/        /              |         |'
            print '-------                  \ _ _ _ /'
            print ' Paper                     Rock'

        elif play1 == 'rock' and play2 == 'paper':
            print '     Human                Master'
            print '---------------      ---------------'
            print ''
            print '    _ _ _                --------        '
            print '  /       \             /       /'
            print ' |         |     vs    /       /'
            print ' |         |          /       /'
            print ' |         |         /       /'
            print '  \ _ _ _ /          --------'
            print '    Rock              Paper'
            print '    '
            print '   '
            print ''

        elif play1 == 'rock' and play2 == 'scissor':
            print '      Human               Master'
            print '---------------      ---------------'
            print ''
            print '    _ _ _                \     /  '
            print '  /       \               \   /  '
            print ' |         |      vs       \ /   '
            print ' |         |               / \   '
            print ' |         |             |  |  | '
            print '  \ _ _ _ /               -- --  '
            print '    Rock                 Scissor '
        elif play1 == 'rock' and play2 == 'rock':
            print '      Human               Master'
            print '---------------      ---------------'
            print ''
            print '    _ _ _                 _ _ _      '
            print '  /       \             /       \     '
            print ' |         |      vs   |         |    '
            print ' |         |           |         |   '
            print ' |         |           |         |    '
            print '  \ _ _ _ /             \ _ _ _ /    '
            print '    Rock                  Rock'
        elif play1 == 'scissor' and play2 == 'paper':
            print '     Human                Master'
            print '---------------      ---------------'
            print ''
            print '    \     /              --------   '
            print '     \   /              /       /'
            print '      \ /        vs    /       /'
            print '      / \             /       /'
            print '    |  |  |          /       /'
            print '     -- --           --------'
            print '    Scissor            Paper'
        elif play1 == 'scissor' and play2 == 'scissor':
            print '     Human                Master'
            print '---------------      --------------- '
            print ''
            print '    \     /               \     / '
            print '     \   /                 \   /        '
            print '      \ /         vs        \ /  '
            print '      / \                   / \  '
            print '    |  |  |               |  |  |    '
            print '     -- --                 -- -- '
            print '    Scissor                Scissor'
        elif play1 == 'scissor' and play2 == 'rock':
            print '      Human               Master'
            print '---------------      --------------- '
            print ''
            print '    \     /                _ _ _         '
            print '     \   /               /       \     '
            print '      \ /         vs    |         |  '
            print '      / \               |         |  '
            print '    |  |  |             |         |  '
            print '     -- --               \ _ _ _ /       '
            print '    Scissor               Rock   '

    def simulate(self, rounds=1000, games = 1):
        self.reset() # reset the scores for new game

        # rounds = 1000 if rounds == None else rounds
        sys.stdout.write('Starting the %s-round simulation of %s games....\n' % (rounds,games))
        sys.stdout.flush()

        if self.record:
            print '\nFirst, please enter your name:'
            sys.stdout.write('>> ')
            humanName = sys.stdin.readline().strip()
            now = datetime.datetime.now()
            f = open('record/record-of-%s-%s%s%s.txt' % (humanName, now.year, now.month, now.day), 'a') #opens file with name of "test.txt"
            description = 'human: %s\nmaster: %s\n[human play] [master play] [winner] [human score]-[master score]\n' % (humanName, self.bot2.name)
            f.write(description)

        for _ in range(games):
            if self.bot1.name != 'Human':
                # print self.bot1.counts
                self.bot1.resetProb()
            self.reset()
            for _ in range(rounds):
                play_1 = self.bot1.playTurn()
                play_2 = self.bot2.playTurn()
                self.bot2.incorporatePlay(play_1)
                outcome = util.CHECK_WINNER[(play_1, play_2)]

                while outcome == 'tie':
                    if self.bot1.name == 'Human':
                        self.printRound(play_1, play_2)
                        print '\n'
                        print 'It\'s a tie'
                    play_1 = self.bot1.playTie()
                    play_2 = self.bot2.playTie()
                    self.bot2.incorporatePlay(play_1)
                    outcome = util.CHECK_WINNER[(play_1, play_2)]

                if self.bot1.name == 'BotV2':
                    self.bot1.incorporatePlay(play_1, outcome)

                self.results.append(outcome)
                self.score[outcome] += 1
                if self.bot1.name == 'Human':
                    winner = 'You win this round!' if outcome == 'bot1' else 'Master wins this round'
                    print '\n'
                    self.printRound(play_1, play_2)
                    print '\n'
                    print '%-22s --- Overall Score: You %i - %i Master' % \
                                (winner, self.score['bot1'], self.score['bot2'])

                if self.record:
                    current_result = '%s %s %s %s-%s\n' % (play_1, play_2, outcome, self.score['bot1'], self.score['bot2'])
                    f.write(current_result)

            percentageWon = float(self.score['bot2'])/rounds
            self.simulationResults.append(percentageWon)

        timesWon = sum(i > 0.5 for i in self.simulationResults)

        if self.record:
            f.close()

        print '\tThe master won %s of %s simulated games\n' % (timesWon,games)
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
