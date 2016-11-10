import random, numpy
import util

MAX_LENGTH = 1000
PEOPLE = ['person-%d' % i for i in range(1, 5)]

for i in PEOPLE:
    choices = {}
    choices['rock']    = random.uniform(0, 1)
    choices['paper']   = 1 - random.uniform(choices['rock'], 1)
    choices['scissor'] = 1 - choices['rock'] - choices['paper']
    textFile = open('opponents/%s.txt' % i,'a')
    textFile.write('%s\n' % i)
    for x, y in choices.items():
        textFile.write('%s-prob: %f\n' % (x, y))
    for _ in range(MAX_LENGTH):
        c = numpy.random.choice(numpy.arange(1, 4), p = choices.values())
        textFile.write('%s\n' % choices.keys()[c - 1])
    textFile.close()
