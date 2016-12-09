import sys
import rpsBots
import simulation
import itertools

BOTS = {}
BOTS['baseline'] = rpsBots.Baseline()
BOTS['master'] = rpsBots.Master()
BOTS['human']  = rpsBots.Human()
BOTS['group'] = rpsBots.MasterEnsemble()
BOTS['group'].addMaster(rpsBots.Master())
BOTS['group'].addMaster(rpsBots.Master(16, 9))
BOTS['group'].addMaster(rpsBots.Master(23, 5))
BOTS['group'].addMaster(rpsBots.Master(23, 14))
BOTS['group'].addMaster(rpsBots.Master(40, 30))

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
                ('sim [bot1] master [rounds] [games]', 'Simulate bot1 playing against master'),
                ('record [bot1] master [rounds]', 'Records data of human vs. master for [x] rounds'),
            ])
            print ''
            print 'Enter empty line to quit'

        elif cmd == 'sim': # sim human master 1000 1
            if len(line.split()) != 4:
                print 'Need the following arguments:'
                print '\tUsage: sim [bot1] master [rounds] [games]'
                print ''
            else:
                name1, name2, rounds, games= line.split()
                bot1 = BOTS[name1]
                bot2 = BOTS[name2]
                if name2 == 'group':
                    bot2 = BOTS['group']
                    print 'Game against group of Masters!!\n'
                    game = simulation.SimulationAgainstMaster(bot1, bot2)
                if name2 == 'master':
                    bot2 = rpsBots.Master(16, 3)
                    print 'Game against the Master!!\n'
                    game = simulation.SimulationAgainstMaster(bot1, bot2)
                else:
                    game = simulation.Simulation(bot1, bot2)
                    print rounds, gamess
                game.simulate(int(rounds),int(games))
                print(game)

        elif cmd == 'record':
            if len(line.split()) != 3:
                print 'Need the following arguments:'
                print '\tUsage: record human master [rounds]'
                print ''
            else:
                _, name2, rounds = line.split()
                bot1 = rpsBots.Human()
                if name2 == 'master':
                    print 'Game against the Master!!\n'
                    bot2 = rpsBots.Master(16, 3)
                elif name2 == 'group':
                    print 'Game against group of Masters!!\n'
                    bot2 = BOTS['group']
                game = simulation.SimulationAgainstMaster(bot1, bot2, True)
                game.simulate(int(rounds),1)

        else:
            print 'Unrecognized command:', cmd

        print ''

def writeResults ():
    nMin = 5; nMax = 26; nStep = 1
    pMin = 3; pMax = 16; pStep = 1
    n = range(nMin, nMax, nStep)
    p = range(pMin, pMax, pStep)
    c = list(itertools.product(n, p))

    for i in c:
        # print i
        bot1 = rpsBots.BotV2()
        bot2 = rpsBots.Master(i[0], i[1])
        game = simulation.SimulationAgainstMaster(bot1, bot2)
        game.simulate(100,500)

        results = [100, 500, i[0], i[1], game.simulationResults]
        resultsString = ' '.join(str(x) for x in results).replace('[','').replace(']','').replace(',','')
        f = open("simResults.txt","a") #opens file with name of "test.txt"
        f.write(resultsString)
        f.write("\n")
        f.close()

if __name__ == '__main__':
    print '\n\tWelcome to our CS 221 Final Project!  Are you prepared to play Rock, Paper, Scissors against R2P5?\n'
    repl()
    # writeResults()
