import sys

# TODO : Add decimal support

operators = {
    '+':'PLUS',
    '-':'MINUS',
    '*':'MULT',
    '/':'DIV',
    '(':'LPAR',
    ')':'RPAR',
    '=':'EQUALS'
}

def main():
    
    #filename = sys.argv[1]
    filename = 'testinput.txt'

    output = []

    try:

        with open(filename,'r') as file:

            contents = file.read()

            ln_counter = 1
            cl_counter = 1

            i = 0
            while i < len(contents):
                char = contents[i]

                if char.isspace():

                    if char == '\n':

                        ln_counter += 1
                        cl_counter = 0

                    else:

                        cl_counter += 1

                    i += 1

                elif char.isalpha() or char == '_':

                    start = i

                    while i < len(contents) and (contents[i].isalnum() or contents[i] == '_'):

                        i += 1
                        cl_counter += 1
                    
                    identifier = contents[start:i]
                    output.append(('VAR',identifier)) 

                elif char.isdigit():

                    start = i

                    while i < len(contents) and contents[i].isdigit():

                        i += 1
                        cl_counter += 1

                    identifier = contents[start:i]
                    output.append(('NUM',identifier))

                elif char in operators:

                    output.append((operators[char],char))
                    cl_counter += 1
                    i += 1

                else:

                    # error for invalid character
                    raise ValueError(f"Invalid char '{char}' at line {ln_counter}, column {cl_counter}")

            output.append(('EOF',None))
            print(output)

    except FileNotFoundError as error:

        print('file not found!')

if __name__ == '__main__':

    main()