from tokenizer import *
from parser import *
from evaluator import *
import sys

def main():

    filename = 'testinput.txt'

    tokens = tokenize(filename)

    #print(tokens)

    parser = Parser(tokens)

    ast = parser.parse_program()

    evaluate_program(ast)

if __name__ == '__main__':
    main()