"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True

    ## RAM Functions
    # Memory Address Register, holds the memory address we're  reading or writing
    #  Memory Data Register, holds the value to write or the 
    # value just read
    def ram_read(self,MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def hlt(self):
        self.running = False

    def ldi(self, operand_a, operand_b):

        self.reg[operand_a] = operand_b
        self.pc += 3
    
    def prn(self, operand_a):
        print(self.reg[operand_a])
        self.pc += 2

    def run(self):
        """Run the CPU."""
        
        # self.trace()
        while self.running:
            ir = self.pc
            inst = self.ram[ir]
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)
            if inst == HLT:  # 0b00000001
                self.hlt()
            elif inst == LDI:  # 0b10000010
                self.ldi(operand_a, operand_b)
            elif inst == PRN:  # 0b01000111
                self.prn(operand_a)
