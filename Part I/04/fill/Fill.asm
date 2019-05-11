// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
    @KBD // The address of the register which the keyboard is connected to
    D=M  // Storing the value in this register

    @FILLSCREEN  // If the value stored in the KBD register is not equal to zero, it means a key has been
                 // pressed and the screen needs to be blackened.
    D;JNE

    @CLEARSCREEN  // If values in KBD = 0, no key is being pressed. Clear Screen.
    D;JEQ

    @LOOP  // Repeat these sequence of statements infinitely
    0;JMP

(FILLSCREEN) // The logic for filling this screen

    // First we will check if the screen is already filled
    @SCREEN  // The base address of the registers which the monitor is connected to
    D=M  // Storing the value at this address
    
    @LOOP  // If this value is non-zero, it means that the monitor is already filled, no need to perform the filling again
    D;JNE

    // Else do the filling
    @SCREEN  // The base address of the registers which the monitor is connected to
    D=A  // Storing this address

    @addr  // Variable to store the address of each monitor register
    M=D  // Initially the variable will hold the base address.

    @i  // loop control variable
    M=0

    (LOOP2)  // Loop through all the monitor registers

        @i
        D=M  // Stores the value of i

        @8192  // The loop needs to repeat 8192 times, since there are 8192 registers that the monitor is connected to
        D=A-D  

        @LOOP  // Stops the filling if i>8191
        D;JEQ

        @addr
        A=M   // Stores the address of the register to be manipulated in A
        M=-1  // M will be the value of the register whose address is stored in A
              // M=-1 will set all its 16bits to 1, making all the pixels of that section black.

        @addr 
        M=M+1  // Increment the addr variable by 1

        @i
        M=M+1  // Increment i by 1

        @LOOP2  // Repeat this Loop
        0;JMP

// Similar logic applies for clearing the screen when no key pressed
(CLEARSCREEN)
    @SCREEN  
    D=M  
    
    @LOOP  
    D;JEQ

    @SCREEN
    D=A

    @addr2
    M=D

    @i
    M=0

    (LOOP3)

        @i
        D=M

        @8192
        D=A-D

        @LOOP
        D;JEQ

        @addr2
        A=M
        M=0

        @addr2
        M=M+1

        @i
        M=M+1

        @LOOP3
        0;JMP

