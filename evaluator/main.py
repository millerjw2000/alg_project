from tokenizer import *
from parser import *
from evaluator import *
from data_reader import *

import sys

def main():

    if len(sys.argv) < 4:
        print('Invalid command useage. /python main.py [filename] [awayteam id] [hometeam id]')
        return 0 # i guess return 0 if execution fails

    filename = sys.argv[1]
    away_id = int(sys.argv[2])
    home_id = int(sys.argv[3])

    try:
        print('Getting stats from db . . .')
        away_stats = get_data_from_db('away',away_id)
        home_stats = get_data_from_db('home',home_id)

        #print(home_stats,away_stats)

        stats = {**away_stats, **home_stats}

        print('Tokenizing file . . .')
        tokens = tokenize(filename)

        #print(tokens)

        parser = Parser(tokens)

        print('Parsing tokens . . .')
        ast = parser.parse_program()

        print('Evaluating AST tree . . .')
        result = evaluate_program(ast,stats)

        print('Finished.')
        for var in result:

            if var in stats:

                continue

            else:

                print(f'{var}: {result[var]}')

        return 1

    except Exception as e: # eventually support more specific exceptions

        print(f'Execution error: {e}')
        return 0

if __name__ == '__main__':
    print(main())