
from typing import List
from collections import deque



class IntCode:
    def __init__(self, program:List[int], inputs:List[int]=[]):
        self.prog = program
        self.log_enabled = False
        self.i = 0
        self.inputs = deque(inputs)
        self.outputs = deque()

        
    def run(self) -> bool:
        # Return bool to indicate if run has finished or is waiting for input
        while self.i != -1 and self.i < len(self.prog):
            try:
                self.i = self.operate(self.i)
            except AwaitInput as e:
                self.log(e)
                return False
        return True 

        
    def operate(self, i) -> int:
        self.log(self.prog, i)
        op, m1, m2 = self.parse_operation(i)

        if op == 1: # add
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            idx = self.prog[i+3]
            self.add(v1, v2, idx)
            return i+4
            
        elif op == 2: # multiply
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            idx = self.prog[i+3]
            self.multiply(v1, v2, idx)
            return i+4
        
        elif op == 3: # input
            idx = self.prog[i+1]
            self.read_input(idx)
            return i+2

        elif op == 4: # ouptut
            idx = self.prog[i+1]
            self.write_output(idx)
            return i+2
        
        elif op == 5: # jump-if-true
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            if self.jumptrue(v1, v2, i): return v2
            return i+3
            
        elif op == 6: # jump-if-false
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            if self.jumpfalse(v1, v2, i): return v2
            return i+3

        elif op == 7: # less than
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            idx = self.prog[i+3]
            self.lessthan(v1, v2, idx)
            return i+4
            
        elif op == 8: # equals
            v1 = self.interp_value(self.prog[i+1], m1)
            v2 = self.interp_value(self.prog[i+2], m2) 
            idx = self.prog[i+3]
            self.equals(v1, v2, idx)
            return i+4
        
        elif op == 99: # end
            return -1
        else:
            raise ValueError(f"Unknown operation: {op}")


    def parse_operation(self, idx):
        n = self.prog[idx]
        op = n % 100
        m1 = (n // 100) % 10
        m2 = (n // 1000) % 10
        return op, m1, m2

    def read_input(self, idx):
        if len(self.inputs) == 0:
            raise AwaitInput("No Input. Awaiting input.")
        inp = self.inputs.popleft()
        self.log("Read Input", inp, idx)
        self.prog[idx] = inp 

    def write_output(self, idx):
        self.log("Write Output:", self.prog[idx], idx)
        self.outputs.append(self.prog[idx])
        

    def interp_value(self, idx, mode):
        if mode == 0: # position
            return self.prog[idx]
        elif mode == 1: # value
            return idx

    def add(self, v1:int, v2:int, idx:int) -> None:
        self.log("Add", v1, v2, idx)
        self.prog[idx] = v1 + v2
        
    def multiply(self, v1:int, v2:int, idx:int) -> None:
        self.log("Multiply", v1, v2, idx)
        self.prog[idx] = v1 * v2

    def jumptrue(self, v1:int, v2:int, idx:int) -> bool:
        istrue = v1 != 0 
        self.log("JumpTrue", v1, istrue, v2, idx)
        if istrue: self.prog[idx] = v2
        return istrue

    def jumpfalse(self, v1:int, v2:int, idx:int) -> bool:
        isfalse = v1 == 0 
        self.log("JumpFalse", v1, isfalse, v2, idx)
        if isfalse: self.prog[idx] = v2
        return isfalse
    
    def lessthan(self, v1:int, v2:int, idx:int) -> None:
        self.log("LessThan", v1, v2, idx)
        istrue = v1 < v2
        self.prog[idx] = int(istrue)

    def equals(self, v1:int, v2:int, idx:int) -> None:
        self.log("Equals", v1, v2, idx)
        istrue = v1 == v2
        self.prog[idx] = int(istrue)
    
    def getidx(self, idx:int) -> int:
        return self.prog[idx]
    
    def get_outputs(self) -> List[int]:
        return self.outputs

    def add_inputs(self, *vals:List[int]) -> None:
        for v in vals:
            self.inputs.append(v)
    
    def log(self, *args):
        if self.log_enabled:
            print(*args)
            
            
            
class AwaitInput(Exception):
    pass