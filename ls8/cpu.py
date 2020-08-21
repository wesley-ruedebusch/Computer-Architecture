"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
## Flag Locations
EQ = 7
LT = 5
GT = 6

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.fl = [0] * 8  # flag register

        self.pc = 0
        self.sp = 7 # stack pointer
        self.running = True
        self.operand_a = self.ram_read(self.pc + 1)
        self.operand_b = self.ram_read(self.pc + 2)

        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[ADD] = self.add
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp
        self.branchtable[JMP] = self.jmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne


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
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[EQ] = 1
                # self.fl[LT] = 0self.reg[reg_b]
                # self.fl[GT] = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                # self.fl[EQ] = 0
                self.fl[LT] = 1
                # self.fl[GT] = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                # self.fl[EQ] = 0
                # self.fl[LT] = 0
                self.fl[GT] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print("KEY:   PC |        FL       | RAM: PC PC+1 PC+2 | REG[0]...REG[7]")
        print(f"TRACE: %02X | %s |      %02X  %02X  %02X   |" % (
            self.pc,
            ' '.join([str(elem) for elem in self.fl]),
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
    
    def push(self):
        # decrement the sp
        self.reg[self.sp] -= 1
        # self.reg[self.sp] &= 0xff
        self.ram[self.reg[self.sp]] = self.reg[self.operand_a]
        self.pc += 2

    def pop(self):
        self.reg[self.operand_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        # self.reg[self.sp] &= 0xff

        self.pc += 2
    
    def call(self):
        
        # Get address of the next instruction
        return_addr = self.pc + 2

        # Push that on the stack
        self.reg[self.sp] -= 1
        address_to_push_to = self.reg[self.sp]
        self.ram[address_to_push_to] = return_addr

        # Set the PC to the subroutine address
        reg_num = self.ram[self.pc + 1]
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr

    def ret(self):
        # Get return address from the top of the stack
        address_to_pop_from = self.reg[self.sp]
        return_addr = self.ram[address_to_pop_from]
        self.reg[self.sp] += 1

        # Set the PC to the return address
        self.pc = return_addr
    
    ### ALU functions
    def mul(self):
        self.alu("MUL", self.operand_a, self.operand_b)
        self.pc += 3

    def add(self):
        self.alu("ADD", self.operand_a, self.operand_b)
        self.pc += 3

    #### Sprint
    def cmp(self):
        self.alu("CMP", self.operand_a, self.operand_b)
        self.pc += 3

    #### Sprint
    def jmp(self):
        self.pc = self.reg[self.operand_a]

    def jeq(self):
        if self.fl[EQ]: # equal flag is true
            # self.jmp()
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def jne(self):
        if not self.fl[EQ]:  # equal flag is false
            # self.jmp()
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    ####

    def run(self):
        """Run the CPU."""
        
        # self.trace()
        while self.running:
            # self.trace()
            ir = self.pc
            inst = self.ram[ir]
            self.operand_a = self.ram_read(ir + 1)
            self.operand_b = self.ram_read(ir + 2)
            self.branchtable[inst]()
