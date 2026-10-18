import sys

def main():
    
    #filename = sys.argv[1]
    filename = 'testinput.txt'

    output = []

    try:

        with open(filename,'r') as file:

            contents = file.read()

            ln_counter = 0
            cl_counter = 0

            i = 0
            while i < len(contents):
                char = contents[i]


    except FileNotFoundError as error:

        print('file not found!')

if __name__ == '__main__':

    main()