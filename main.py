import sys
import rpsBots
import simulation

'''
TODO: human can play a bot
      human can enter probabilities for their own bot
      add other bots
'''

BOTS = {}

def addPlayers():
    detailFile = open('opponents/details.txt', 'r')
    lenghts = detailFile.readline().strip().split()
    first, last = detailFile.readline().strip().split()
    for i in range(int(first), int(last) + 1):
        BOTS['person-%s' % i] = rpsBots.Bot('person-%s' % i)
    BOTS['baseline'] = rpsBots.Baseline()
    BOTS['botV2'] = rpsBots.BotV2()
    BOTS['master'] = rpsBots.Master()
    BOTS['human']  = rpsBots.Human()
    detailFile.close()

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
                ('peroson-[#]', 'Play Person-[#]. Can choose from [X] to [Y]'),
                ('sim [bot1] master [rounds]', 'Simulate bot1 playing against master'),
                ('single [bot1] [bot2]', 'Simulate 1 round between two bots'),
                ('oracle [bot1] [rounds]', 'Oracle plays against the given bot'),
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

        elif cmd == 'sim':
            if len(line.split()) != 4:
                print 'Need the following arguments:'
                print '\tUsage: simulate [bot1] [bot2] [rounds] [games]'
                print ''
            else:
                name1, name2, rounds, games = line.split()
                bot1 = BOTS[name1]
                bot2 = BOTS[name2]
                if name2 == 'master':
                    print 'Game against master!!\n'
                    game = simulation.SimulationAgainstMaster(bot1, bot2)
                else:
                    game = simulation.Simulation(bot1, bot2)
                game.simulate(int(rounds),int(games))
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
    print '\n\tWelcome to our CS 221 Final Project!  Are you prepared to play Rock, Paper, Scissors against R2P5?\n'
    addPlayers()
    repl()
