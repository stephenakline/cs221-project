import sys
import rpsBots
import simulation

'''
TODO: human can play a bot
      human can enter probabilities for their own bot
      add other bots
'''

BOTS = {}
BOTS['bot-baseline'] = rpsBots.Baseline()
BOTS['bot-strategy'] = rpsBots.Bot({'rock': .33, 'paper': .33, 'scissor': (1-.33-.33)},
                                ['rock', 'paper', 'scissor', 'paper'],
                                probWeight = 0.0, strategyWeight = 1.0)
BOTS['bot-mix'] = rpsBots.Bot({'rock': 0.3, 'paper': 0.3, 'scissor': 0.4},
                                ['rock', 'paper', 'paper', 'rock'],
                                probWeight = 1, strategyWeight = 0)

# REPL and main entry point
def repl(command=None):
    '''REPL: read, evaluate, print, loop'''

    while True:
        sys.stdout.write('>> ')
        line = sys.stdin.readline().strip()
        if not line:
            break

        if command is None:
            cmdAndLine = line.split(None, 1)
            cmd, line = cmdAndLine[0], ' '.join(cmdAndLine[1:])
        else:
            cmd = command
            line = line

        print ''

        if cmd == 'help':
            print 'Usage: <command> [arg1, arg2, ...]'
            print ''
            print 'Commands:'
            print '\n'.join(a + '\t\t\t' + b for a, b in [
                ('bot-baseline', 'Bot who only plays the uniform frequencies'),
                ('bot-strategy', 'Bot who only plays the simple strategy'),
                # ('bot-random', 'Bot who plays with random frequencies'),
                # ('bot-user', 'Bot who is defined by the user'),
                # ('bot-oracle', 'Bot who knows the opponent\'s strategy'),
                ('simulate [bot1] [bot2] [# rounds]', 'Simulate two bots playing'),
                ('single [bot1] [bot2]', 'Simulate 1 round between two bots'),
                ('oracle [bot1] [# rounds]', 'Oracle plays against the given bot'),
            ])
            print ''
            print 'Enter empty line to quit'

        elif cmd == 'single':
            if len(line.split()) != 2:
                print 'Need the following arguments:'
                print '\tUsage: single [bot1] [bot2]'
                print ''
            else:
                name1, name2 = line.split()
                bot1 = BOTS[name1]
                bot2 = BOTS[name2]
                game = simulation.Simulation(bot1, bot2)
                game.singleGame()

        elif cmd == 'simulate':
            if len(line.split()) != 3:
                print 'Need the following arguments:'
                print '\tUsage: simulate [bot1] [bot2] [# rounds]'
                print ''
            else:
                name1, name2, rounds = line.split()
                bot1 = BOTS[name1]
                bot2 = BOTS[name2]
                game = simulation.Simulation(bot1, bot2)
                game.simulate(int(rounds))
                print(game)

        elif cmd == 'oracle':
            if len(line.split()) != 2:
                print 'Need the following arguments:'
                print '\tUsage: oracle [bot1] [# rounds]'
                print ''
            else:
                name1, rounds = line.split()
                bot1 = BOTS[name1]
                bot2 = rpsBots.Oracle(bot1)
                game = simulation.Simulation(bot1, bot2)
                game.simulate(int(rounds))
                print(game)

        else:
            print 'Unrecognized command:', cmd

        print ''

if __name__ == '__main__':
    print '\n\tWelcome to HELL - Prepare to lose a game of Rock, Paper, Scissor to R2P5!\n'
    repl()
