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
        self.branchtable = {
            0b00000001: self.halt,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b10100000: self.add,
            0b10000010: self.ldi,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b00010001: self.ret,
            0b01010000: self.call
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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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