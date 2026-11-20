import sys

# TODO : Add decimal support

operators = {
    '+':'PLUS',
    '-':'MINUS',
    '*':'MULT',
    '/':'DIV',
    '(':'LPAR',
    ')':'RPAR',
    '=':'ASSIGN',
    '>':'GT',
    '<':'LT',
    '>=':'GTE',
    '<=':'LTE',
    '==':'EQ',
    '!=':'NEQ',
    ',':'COM',
    ';':'SEMICOL'
}

keywords = ['IF','THEN','ELSE','AND','OR','NOT','END']

def tokenize(filename):
    
    #filename = sys.argv[1]
    #filename = 'testinput.txt'

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
                        cl_counter = 1

                    else:

                        cl_counter += 1

                    i += 1

                elif char.isalpha() or char == '_':

                    start = i

                    while i < len(contents) and (contents[i].isalnum() or contents[i] == '_'):

                        i += 1
                        cl_counter += 1
                    
                    identifier = contents[start:i]
                    
                    if identifier.upper() in keywords:
                        output.append((identifier.upper(),identifier))
                    else:
                        output.append(('VAR',identifier)) 

                elif char.isdigit():

                    start = i

                    while i < len(contents) and contents[i].isdigit():
                        i += 1
                        cl_counter += 1

                    if i < len(contents) and contents[i] == '.':
                        i += 1
                        cl_counter += 1

                        if i >= len(contents) or not contents[i].isdigit():
                            raise ValueError(
                                f"Invalid number at line {ln_counter}, column {cl_counter}"
                            )

                        while i < len(contents) and contents[i].isdigit():
                            i += 1
                            cl_counter += 1

                    number = contents[start:i]
                    output.append(('NUM', number))
                
                elif char in '+-*/()=<>!,;':

                    op = contents[i:i+2]

                    if op in operators:
                        output.append((operators[op], op))
                        i += 2
                        cl_counter += 2

                    elif char in operators:
                        output.append((operators[char], char))
                        i += 1
                        cl_counter += 1

                    else:
                        raise ValueError(f"Invalid char '{char}' at line {ln_counter}, column {cl_counter}")

                else:

                    # error for invalid character
                    raise ValueError(f"Invalid char '{char}' at line {ln_counter}, column {cl_counter}")

            output.append(('EOF',None))
            #print(output)

            return output

    except FileNotFoundError as error:

        print('file not found!')

if __name__ == '__main__':

    pass