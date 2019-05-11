// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies the contents of R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R0   //A instruction referring to RAM[0]
D=M   // set the data memory to the value inserted by the user into RAM[0]

@n    // Declaring a variable, n
M=D   // making n hold the value of RAM[0]

@i    // Declaring the loop control variable i.
M=1   // Setting i=1

@R2   
M=0   // Ensuring that RAM[2] is initially 0.

(LOOP)  // LOOP Label, start of the loop

    // Loop Condition Checking
    @i
    D=M  // setting the data memory to the current value of i (after incrementing from previous iteration, if any)

    @n
    D=M-D   // setting the data memory to (RAM[0] - i)

    @END
    D;JLT   // breaking out of the loop if (RAM[0] - i < 0), as we are adding RAM[1] to itself RAM[0] number of times.

    // Updating the contents of RAM[2], i.e., adding value of RAM[1] to it. This addition is done RAM[0] number of times.
    @R2
    D=M
    @R1
    D=D+M
    @R2
    M=D

    // Increment i after each iteration.
    @i
    M=M+1
    @LOOP
    0;JMP

// Infinite loop to terminate the program.
(END)
    @END
    0;JMP

