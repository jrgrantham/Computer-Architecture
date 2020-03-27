"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # reg is 8 
        self.reg = [0] * 8
        # ram is 256
        self.reg[7] = 0xf4
        self.ram = [0] * 256
        # add pc to 0
        self.operand_a = 0
        self.operand_b = 0
        self.program_counter = 0
        self.stack_pointer = 0
        self.running = True
        self.flag: 0
        self.branchtable = {
            0b00000001: self.halt,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b10100000: self.add,
            0b10000010: self.ldi,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b00010001: self.ret,
            0b01010000: self.call,
            0b10100111: self.cmp,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b10101000: self.AND,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b10101011: self.XOR,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b10100100: self.mod,
        }

    def halt(self):
        self.running = False

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # split line before and after comment symbol
                    comment_split = line.split("#")

                    # extract our number
                    num = comment_split[0].strip() # trim whitespace

                    if num == '':
                        continue # ignore blank lines

                    # convert our binary string to a number
                    val = int(num, 2)

                    # print the val in bin and dec
                    # print(f"{val:08b}: {val:d}")
                    # program.append(val)
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def mul(self):
        self.alu('MUL', self.operand_a, self.operand_b)

    def add(self):
        self.alu('ADD', self.operand_a, self.operand_b)

    def mod(self):
        self.alu('MOD', self.operand_a, self.operand_b)

    def cmp(self):
        self.alu('CMP', self.operand_a, self.operand_b)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == 'MOD':
            if self.reg[reg_b] == 0:
                print('Error')
                self.halt()
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self):
        self.reg[self.operand_a] = self.operand_b

    def prn(self):
        print(self.reg[self.operand_a])

    def pop(self):
        self.stack_pointer = self.reg[7]
        val = self.ram[self.stack_pointer]
        self.reg[self.operand_a] = val
        self.reg[7] += 1

    def push(self):
        self.reg[7] -= 1
        self.stack_pointer = self.reg[7]
        self.ram[self.stack_pointer] = self.reg[self.operand_a]

    def call(self):
        self.reg[7] -= 1
        self.stack_pointer = self.reg[7]
        self.ram[self.stack_pointer] = (self.program_counter + 2)
        # self.ram_write(self.program_counter + 2, self.stack_pointer)
        self.program_counter = (self.reg[self.operand_a])

    def ret(self):
        self.stack_pointer = self.reg[7]
        val = self.ram_read(self.stack_pointer)
        # val = self.ram[self.stack_pointer]
        self.program_counter = val
        self.reg[7] += 1

    def jmp(self):
        self.program_counter = self.reg[self.operand_a]

    def jeq(self):
        if self.flag == 0b00000001:
            self.jmp()
        else:
            self.program_counter += 2

    def jne(self):
        if f'{self.flag:08b}'[-1] == '0':
            self.jmp()
        else:
            self.program_counter += 2

    def AND(self):
        self.alu('AND', self.operand_a, self.operand_b)

    def NOT(self):
        self.alu('NOT', self.operand_a, self.operand_b)

    def OR(self):
        self.alu('OR', self.operand_a, self.operand_b)

    def XOR(self):
        self.alu('XOR', self.operand_a, self.operand_b)

    def SHL(self):
        self.alu('SHL', self.operand_a, self.operand_b)

    def SHR(self):
        self.alu('SHR', self.operand_a, self.operand_b)

    def run(self):
        """Run the CPU."""
        # running = True
        while self.running:
        # needs to read mem address stores in register PC and store in IR - local variable
            IR = self.ram_read(self.program_counter)
            self.operand_a = self.ram_read(self.program_counter + 1)
            self.operand_b = self.ram_read(self.program_counter + 2)
            self.branchtable[IR]()
            # print(f'{IR:08b}'[3])
            if f'{IR:08b}'[3] == '0':
                self.program_counter += (IR >> 6) + 1