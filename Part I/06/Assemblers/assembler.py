import sys  # for getting command line arguments
import os  # for deleting temporary files

symbols = {}  # initializing an empty symbol table

# add pre-defined symbols to the symbol table
# first add the Register symbols R1 to R15
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

variable_address = 16

def main():
    filename = sys.argv[1]  # getting the filename entered a command-line argument

    # open the entered file.
    with open(filename, "r") as ASMFile:

        # first stage, remove all whitespaces
        firststage(ASMFile)

        # first pass, after removing whitespaces
        # to read only the labels and update the symbol table with these labels
        firstpass()

        # parsing and processing all the instructions in the file - 
        # the parameter being passed is the name of the file.
        parse_and_process(filename.split('.')[0] + ".hack")

        os.remove("temp.txt")

def firststage(ASMFile):  # removes all whitespaces
    with open("temp.txt", "w") as ASMFile_RemovedWSpace:
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


def firstpass():
    with open("temp.txt", "r") as ASMFile_RemovedWSpace:
        instruction_no = 0

        # if the line is not (empty OR a comment OR a label), update instruction number
        for line in ASMFile_RemovedWSpace:
            if line[0] == '(':
                i = 1
                label = ''
                
                while line[i] != ')':
                    label += line[i]
                    i += 1
                
                symbols.update({label: instruction_no})
                continue
            
            # finally if its neither of the above three, increment the instruction counter
            instruction_no = instruction_no + 1
    
    # this completes the first pass.

def parse_and_process(fileName):
    with open('temp.txt', 'r') as ASMFile_RemovedWSpace:

        with open(fileName, 'w') as hackFile:

            for line in ASMFile_RemovedWSpace:
                # remove \n from end of line
                line = line.split('\n')[0]

                # first check if it's an A instruction -
                if line[0] == '@':
                    if line[1:].isdigit():  # if the part of the address after the @ is a number
                        binary_val = bin(int(line[1:]))[2:]  # get the binary value of the number
                                                            # after the @

                        # pre-pend the required number of zeroes to make it 16-bit:
                        for i in range(16-len(binary_val)):
                            binary_val = '0' + binary_val

                        # just directly add the above value to the .hack file
                        hackFile.write(binary_val+'\n')

                    # if the segment after the @ is not an integer, then its either a variable
                    # or a jump label thing.

                    # first check the symbol table
                    else:
                        flag = 0
                        for symbol,value in symbols.items():
                            if symbol == line[1:]:  # the symbol pre-exists in the table
                                flag = putSymbolValue(value, hackFile)  # flag = 1 after this step

                        if(not flag):
                            # the symbol does not exist in the table => new variable created    
                            # pre-pend the required number of zeroes to make it 16-bit:
                            createNewVariable(hackFile, line)

                # now we will deal with C instructions -     
                elif line[0] != '(':
                    # we will first parse the instruction as a list of strings
                    # and then send this list, along with the .hack file to another method for processing

                    subparts = []  # will hold each subpart of the given instruction
                    subpart = ''   # holds each subpart as a string, will be added to the list

                    for character in line:
                        if character != '=' and character != ';':
                            subpart += character
                        elif character == '=' or character == ';':
                            subparts.append(subpart)
                            subpart = ''

                    subparts.append(subpart)

                    process_C_inst(hackFile, subparts)


def putSymbolValue(value, hackFile):
    binary_val = bin(value)[2:]  # get the binary value of the number
                                 # after the @

    # pre-pend the required number of zeroes to make it 16-bit:
    for i in range(16-len(binary_val)):
        binary_val = '0' + binary_val

    # just directly add the above value to the .hack file
    hackFile.write(binary_val+'\n')  
    return 1

def createNewVariable(hackFile, line):  # for creating a new variable
    global variable_address
 
    symbols[line[1:]] = variable_address  # adding the variable name: variable address pair to the symbol table

    binary_str_var_addr = bin(variable_address)[2:]  # getting the binary value of the variable address

    for i in range(16-len(binary_str_var_addr)):  # pre-pending 0's
        binary_str_var_addr = '0' + binary_str_var_addr

    hackFile.write(binary_str_var_addr+'\n')  # writing 16-bit variable address in binary to the hack file.

    variable_address = variable_address + 1  # next variable will be stored in next register.

def process_C_inst(hackFile, subparts):
    binary_val = '111'  # writing the first opcode and the
                        # next two unused but required bits.
    
    if len(subparts) == 2:
        if subparts[1][0] != 'J':  # not a jump instruction
            binary_val += comp[subparts[1]]
            binary_val += dest[subparts[0]]
            binary_val += '000'

        else:  # a jump instruction
            binary_val += comp[subparts[0]]
            binary_val += '000'
            binary_val += jump[subparts[1]]

    else:  # the only other possibility of the list length is 3
           # this will be the assignment + jump instruction
        binary_val += comp[subparts[1]]
        binary_val += dest[subparts[0]]
        binary_val += jump[subparts[2]]

    # write the binary val to the file
    hackFile.write(binary_val + '\n')

if __name__ == "__main__":
    main()