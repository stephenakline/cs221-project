import sys
import rpsBots
import simulation

# if __name__ == '__main__':
probs = {'rock': .33, 'paper': .33, 'scissor': (1-.33-.33)}
bot1 = rpsBots.ProbabilityRPSBot(probs)

probs = {'rock': 0.50, 'paper': 0.50, 'scissor': 0.0}
bot2 = rpsBots.OrderRPSBot(['rock', 'paper', 'scissor'])

game = simulation.Simulation(bot1, bot2, 10000)
