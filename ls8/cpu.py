"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7 # stack pointer
        self.running = True
        self.operand_a = self.ram_read(self.pc + 1)
        self.operand_b = self.ram_read(self.pc + 2)

        self.branchtable = {HLT: self.hlt , LDI: self.ldi , PRN: self.prn}
        # self.branchtable[HLT] = self.hlt
        # self.branchtable[LDI] = self.ldi
        # self.branchtable[PRN] = self.prn
        # self.branchtable[MUL] = self.mul
        # self.branchtable[PUSH] = self.push
        # self.branchtable[POP] = self.pop

    ## RAM Functions
    # Memory Address Register, holds the memory address we're 
    # reading or writing
    #  Memory Data Register, holds the value to write or the 
    # value just read
    def ram_read(self,MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""
        address = 0

        try:
            with open(file) as f:
                for line in f:
                    try:
                        line = line.strip()
                        line = line.split('#', 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {file}")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ldi(self):
        self.reg[self.operand_a] = self.operand_b
        self.pc += 3
    
    def prn(self):
        print(self.reg[self.operand_a])
        self.pc += 2

    def mul(self):
        self.alu("MUL", self.operand_a, self.operand_b)
        self.pc += 3
    
    def push(self):
        # securement the sp
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[self.operand_a]
        self.pc += 2

    def pop(self):
        self.reg[self.operand_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc += 2

    def run(self):
        """Run the CPU."""
        
        # self.trace()
        while self.running:
            ir = self.pc
            inst = self.ram[ir]
            self.operand_a = self.ram_read(ir + 1)
            self.operand_b = self.ram_read(ir + 2)
            self.branchtable[inst]()
