from tokenizer import *
from parser import *
from evaluator import *
from data_reader import *

import sys

def main():

    away_id = 1
    home_id = 2

    away_stats = get_data_from_db('away',away_id)
    home_stats = get_data_from_db('home',home_id)

    #print(home_stats,away_stats)

    stats = {**away_stats, **home_stats}

    #print(stats)
    
    filename = 'evaluator/testinput.txt'

    tokens = tokenize(filename)

    #print(tokens)

    parser = Parser(tokens)

    ast = parser.parse_program()

    evaluate_program(ast,stats)

if __name__ == '__main__':
    main()