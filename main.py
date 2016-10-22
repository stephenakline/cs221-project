import sys
import rpsBots
import simulation

'''
TODO: human can play a bot
      human can enter probabilities for their own bot
      add other bots
'''

BOTS = {}
BOTS['bot-basic'] = rpsBots.ProbabilityRPSBot({'rock': .33, 'paper': .33, 'scissor': (1-.33-.33)})
BOTS['bot-random'] = rpsBots.ProbabilityRPSBot({'rock': .5, 'paper': .2, 'scissor': (1-.5-.2)})
# probs = {'rock': 0.50, 'paper': 0.50, 'scissor': 0.0}
# bot2 = rpsBots.OrderRPSBot(['rock', 'paper', 'scissor'])
#
# game = simulation.Simulation(bot1, bot2, 10000)

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
                ('bot-basic', 'Bot who plays the uniform frequencies'),
                ('bot-random', 'Bot who plays with random frequencies'),
                ('bot-user', 'Bot who is defined by the user'),
                ('bot-oracle', 'Bot who knows the opponent\'s strategy'),
                ('simulate [bot1] [bot2] [number of rounds]', 'Simulate two bots playing'),
                ('single [bot1] [bot2]', 'Simulate 1 round between two bots'),
                ('user [bot1]', 'User plays against a bot'),
            ])
            print ''
            print 'Enter empty line to quit'

        elif cmd == 'single':
            # call single bot play
            if len(line.split()) != 2:
                print 'Need to provide two bots to play'
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
                print 'Need to provide two bots to play:'
                print '\tUsage: single [bot1] [bot2] [number of rounds]'
                print ''
            else:
                name1, name2, rounds = line.split()
                bot1 = BOTS[name1]
                bot2 = BOTS[name2]
                game = simulation.Simulation(bot1, bot2)
                game.simulate(int(rounds))
                print(game)

        # elif cmd == 'both':
        #     line = wordsegUtil.cleanLine(line)
        #     smoothCost = wordsegUtil.smoothUnigramAndBigram(unigramCost, bigramCost, 0.2)
        #     parts = [wordsegUtil.removeAll(w, 'aeiou') for w in wordsegUtil.words(line)]
        #     print '  Query (both):', ' '.join(parts)
        #     print ''
        #     print '  ' + ' '.join(
        #         submission.segmentAndInsert(part, smoothCost, possibleFills)
        #         for part in parts
        #     )
        #
        # elif cmd == 'fills':
        #     line = wordsegUtil.cleanLine(line)
        #     print '\n'.join(possibleFills(line))
        #
        # elif cmd == 'ug':
        #     line = wordsegUtil.cleanLine(line)
        #     print unigramCost(line)
        #
        # elif cmd == 'bg':
        #     grams = tuple(wordsegUtil.words(line))
        #     prefix, ending = grams[-2], grams[-1]
        #     print bigramCost(prefix, ending)

        else:
            print 'Unrecognized command:', cmd

        print ''

if __name__ == '__main__':

    repl()
