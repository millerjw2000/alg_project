import tokenizer as Tokenizer
import parser as p
import sys

def main():

    filename = 'testinput.txt'

    tokens = Tokenizer.tokenize(filename)

    print(tokens)

    parser = p.Parser(tokens)

    ast = parser.parse_program()

    print(ast)


if __name__ == '__main__':
    main()