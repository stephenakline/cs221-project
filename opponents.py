import random, numpy

LENGTH = [20, 200, 1000]
NUM_PEOPLE = 5
PEOPLE = ['person-%d' % i for i in range(1, NUM_PEOPLE)]

textFile = open('opponents/details.txt', 'a')
textFile.write(' '.join([str(i) for i in LENGTH]))
textFile.write('\n%s %s\n' % (1, len(PEOPLE)))
textFile.close()

for i in PEOPLE:
    choices = {}
    choices['rock']    = random.uniform(0, 1)
    choices['paper']   = 1 - random.uniform(choices['rock'], 1)
    choices['scissor'] = 1 - choices['rock'] - choices['paper']
    textFile = open('opponents/%s.txt' % i,'a')
    textFile.write('%s\n' % i)
    for x, y in choices.items():
        textFile.write('%s-prob: %f\n' % (x, y))
    amount = random.choice(LENGTH)
    textFile.write('%s\n' % amount)
    for _ in range(amount):
        c = numpy.random.choice(numpy.arange(1, 4), p = choices.values())
        textFile.write('%s\n' % choices.keys()[c - 1])
    textFile.close()
