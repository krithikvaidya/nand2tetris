# THIS CODE IS NOT ENTIRELY WELL DOCUMENTED! SEE THE assembler.py FOR PROPER DOCUMENTATION

import sys  # for getting command line arguments
import os  # for deleting temporary files

symbols = {}  # an empty symbol table

# adding pre-defined symbols to the symbol table
# first add the Register symbols
for i in range(16):
    symbols.update({'R'+str(i): i})

# add SCREEN and KBD
symbols.update({'SCREEN': 16384, 'KBD': 24576})

# add the remaining five symbols
symbols.update({'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4})


# create 3 tables corresponding to each part of the C instruction -
# dest, comp, jump.
dest = {
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

comp = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

jump = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


def main():
    filename = sys.argv[1]  # getting the filename entered a command-line argument

    # open the entered file. TODO - check if the file exists.
    ASMFile = open(filename, "r")

    # first pass, to read only the labels and update the symbol table with these labels
    # firstpass(ASMFile)

    # second pass, actual translation
    # secondpass(ASMFile)

    # first stage, remove all whitespaces
    firststage(ASMFile)

    ASMFile.close()
    os.remove("temp.txt")


def firststage(ASMFile):
    ASMFile_RemovedWSpace = open("temp.txt", "w")
    for line in ASMFile:
        line = line.split('\n')[0]
        line = line.replace(" ", "")  # remove all spaces in the line
        
        # if line is empty, go to the next line 
        if line == '':
            continue
        
        # check for single line comment, ignore the rest of the line is it is.
        elif line[0] == '/' and line[1] == '/':
            continue

        else:
            inline_comment_location = line.find('//')
            if inline_comment_location != -1:
                line = line[0:inline_comment_location]
            
        ASMFile_RemovedWSpace.write(line + '\n')

    ASMFile_RemovedWSpace.close()
    parseInstructions()


def parseInstructions():
    ASMFile_RemovedWSpace = open('temp.txt', 'r')
    hackFile = open(".hack", 'w')

    for line in ASMFile_RemovedWSpace:
        # remove \n from end of line
        line = line.split('\n')[0]

        # first check if it's an A instruction -
        if line[0] == '@':
            binary_val = bin(int(line[1:]))[2:]  # get the binary value of the number
                                                 # after the @

            # pre-pend the required number of zeroes to make it 16-bit:
            for i in range(16-len(binary_val)):
                binary_val = '0' + binary_val

            # just directly add the above value to the .hack file, after pre-pending
            hackFile.write(binary_val+'\n')
            
        # now we will deal with C instructions -     
        else:
            # we will first parse the instruction as a list of strings
            # and then send this list, along with the .hack file to another method for processing

            subparts = []
            string = ''

            for character in line:
                if character != '=' and character != ';':
                    string += character
                elif character == '=' or character == ';':
                    subparts.append(string)
                    string = ''

            subparts.append(string)

            process_C_inst(hackFile, subparts)
    
    ASMFile_RemovedWSpace.close()
    hackFile.close()


def process_C_inst(hackFile, subparts):
    binary_val = '111'  # writing the first opcode and the
                        # next two unused but required bits.
    
    if len(subparts) == 2:
        if subparts[1][0] != 'J':  # not a jump instruction
            binary_val += comp[subparts[1]]
            binary_val += dest[subparts[0]]
            binary_val += '000'

        else:  # is a jump instruction
            binary_val += comp[subparts[0]]
            binary_val += '000'
            binary_val += jump[subparts[1]]

    else:  # the only other possibility of the list length is 3
           # this will be the assignment + jump instruction
        print()
        print(subparts)
        print()

        binary_val += comp[subparts[1]]
        binary_val += dest[subparts[0]]
        binary_val += jump[subparts[2]]

    # write the binary val to the file
    hackFile.write(binary_val + '\n')
        
                
""" def firstpass(ASMFile):
    instruction_no = 0

    # if the line is not (empty or a comment or a label), update instruction number
    for line in ASMFile.readline():
        line = line.replace(" ", "")  # remove all spaces in the line

        # if line is empty, go to the next line 
        if line == '':
            continue
        # check for single line comment, ignore the rest of the line is it is.
        elif line[0] == '/' and line[1] == '/':
            continue
        
        if line[0] == '(':
            i = 0
            label = ''
            
            while line[i] != ')':
                label += line[i]

            symbols.update({label: instruction_no})
            continue
        
        # finally if its neither of the above three, increment the instruction counter
        instruction_no = instruction_no + 1
    
    # this completes the first pass.

"""

def secondpass(ASMFile):
    for line in ASMFile.readline():
        line = line.replace(" ", "")  # remove all spaces in the line
        
        # if line is empty, go to the next line 
        if line == '':
            continue
        # check for single line comment, ignore the rest of the line is it is.
        elif line[0] == '/' and line[1] == '/':
            continue
        else:
            continue #placeholder



if __name__ == "__main__":
    main()