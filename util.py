CHECK_WINNER = {}
CHECK_WINNER[('rock', 'rock')] = 'tie'
CHECK_WINNER[('paper', 'paper')] = 'tie'
CHECK_WINNER[('scissor', 'scissor')] = 'tie'
CHECK_WINNER[('rock', 'paper')] = 'bot2'
CHECK_WINNER[('rock', 'scissor')] = 'bot1'
CHECK_WINNER[('paper', 'rock')] = 'bot1'
CHECK_WINNER[('paper', 'scissor')] = 'bot2'
CHECK_WINNER[('scissor', 'rock')] = 'bot2'
CHECK_WINNER[('scissor', 'paper')] = 'bot1'

ORACLE_STRATEGY = {}
ORACLE_STRATEGY['rock'] = 'paper'
ORACLE_STRATEGY['paper'] = 'scissor'
ORACLE_STRATEGY['scissor'] = 'rock'
