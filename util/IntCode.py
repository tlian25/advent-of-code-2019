
from typing import List
from collections import deque, defaultdict



class IntCode:
    def __init__(self, program:List[int], inputs:List[int]=[]):
        self.prog = program
        self.progoverflow = {}
        self.log_enabled = False
        self.i = 0
        self.inputs = deque(inputs)
        self.outputs = deque()
        self.relative_base = 0
        self.ended = False

        
    def run(self) -> bool:
        # Return bool to indicate if run has finished or is waiting for input
        while self.i != -1 and (self.i < len(self.prog) or self.i in self.progoverflow):
            try:
                self.i = self.operate(self.i)
            except AwaitInput as e:
                self.log(e)
                return False
            
        self.ended = True
        return True 


    def operate(self, i) -> int:
        self.log('\nOperation:', 'idx:', i, '>> value:', self.getidx(i))
        self.log('Program:', self.prog, self.progoverflow)
        self.log('Inputs:', self.inputs, 'Outputs:', self.outputs)
        self.log('Base:', self.relative_base, '\n')
        op, m1, m2, m3 = self.parse_operation(i)

        if op == 1: # add
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2)
            idx = self.getidx(i+3)
            if m3 == 2: idx += self.relative_base
            self.add(v1, v2, idx)
            return i+4

        elif op == 2: # multiply
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2) 
            idx = self.getidx(i+3)
            if m3 == 2: idx += self.relative_base
            self.multiply(v1, v2, idx)
            return i+4

        elif op == 3: # input
            idx = self.getidx(i+1)
            if m1 == 2: idx += self.relative_base
            self.read_input(idx)
            return i+2

        elif op == 4: # ouptut
            v1 = self.interp_value(self.getidx(i+1), m1)
            self.write_output(v1)
            return i+2

        elif op == 5: # jump-if-true
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2) 
            if self.jumptrue(v1, v2, i): return v2
            return i+3
            
        elif op == 6: # jump-if-false
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2) 
            if self.jumpfalse(v1, v2, i): return v2
            return i+3

        elif op == 7: # less than
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2) 
            idx = self.getidx(i+3)
            if m3 == 2: idx += self.relative_base
            self.lessthan(v1, v2, idx)
            return i+4
            
        elif op == 8: # equals
            v1 = self.interp_value(self.getidx(i+1), m1)
            v2 = self.interp_value(self.getidx(i+2), m2) 
            idx = self.getidx(i+3)
            if m3 == 2: idx += self.relative_base
            self.equals(v1, v2, idx)
            return i+4
        
        elif op == 9: # adjust relative base
            v1 = self.interp_value(self.getidx(i+1), m1)
            self.adjust_relative_base(v1)
            return i+2
        
        elif op == 99: # end
            return -1

        else:
            raise ValueError(f"Unknown operation: {op}")





    def parse_operation(self, idx:int) -> List[int]:
        n = self.getidx(idx)
        op = n % 100
        m1 = (n // 100) % 10
        m2 = (n // 1000) % 10
        m3 = (n // 10000) % 10
        return op, m1, m2, m3

    def interp_value(self, val:int, mode:int) -> int:
        if mode == 0: # position
            return self.getidx(val)
        elif mode == 1: # value
            return val
        elif mode == 2: # relative position
            return self.getidx(val + self.relative_base)

    def read_input(self, idx):
        if len(self.inputs) == 0:
            raise AwaitInput("No Input. Awaiting input.")
        inp = self.inputs.popleft()
        self.log("Read Input", inp, idx)
        self.setidx(idx, inp)

    def write_output(self, val):
        self.log("Write Output:", val)
        self.outputs.append(val)
        
    def add(self, v1:int, v2:int, idx:int) -> None:
        self.log("Add", v1, v2, '>>', idx)
        self.setidx(idx, v1+v2)
        
    def multiply(self, v1:int, v2:int, idx:int) -> None:
        self.log("Multiply", v1, v2, '>>', idx)
        self.setidx(idx, v1*v2)

    def jumptrue(self, v1:int, v2:int, idx:int) -> bool:
        istrue = (v1 != 0)
        self.log("JumpTrue", v1, istrue, v2, idx)
        # if istrue: self.setidx(idx, v2)
        return istrue

    def jumpfalse(self, v1:int, v2:int, idx:int) -> bool:
        isfalse = (v1 == 0)
        self.log("JumpFalse", v1, isfalse, v2, idx)
        # if isfalse: self.setidx(idx, v2)
        return isfalse
    
    def lessthan(self, v1:int, v2:int, idx:int) -> None:
        self.log("LessThan", v1, v2, idx)
        istrue = v1 < v2
        self.setidx(idx, int(istrue))

    def equals(self, v1:int, v2:int, idx:int) -> None:
        self.log("Equals", v1, v2, idx)
        istrue = v1 == v2
        self.setidx(idx, int(istrue))
        
    def adjust_relative_base(self, v1:int) -> None:
        self.relative_base += v1
        self.log("Adjust Rel Base", v1, self.relative_base)
    
    def getidx(self, idx:int) -> int:
        if idx < len(self.prog):
            return self.prog[idx]
        elif idx in self.progoverflow:
            return self.progoverflow[idx]
        else:
            return 0

    def setidx(self, idx:int, val:int) -> None:
        if idx < len(self.prog):
            self.prog[idx] = val
        else:
            self.progoverflow[idx] = val
        
    def get_outputs(self) -> deque:
        return self.outputs

    def pop_output(self) -> int:
        return self.outputs.popleft()

    def add_inputs(self, *vals:List[int]) -> None:
        for v in vals:
            self.inputs.append(v)
            
    def is_ended(self) -> bool:
        return self.is_ended

    def log(self, *args):
        if self.log_enabled:
            print(*args)
            
            
            
class AwaitInput(Exception):
    pass