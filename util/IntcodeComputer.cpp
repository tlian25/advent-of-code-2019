#include "IntcodeComputer.h"
#include<iostream>
#include<deque>

using namespace std;

/*
Opcode - first int, 1, 2, 99
99 - finishes
1 - add togther numbers read from two positions and stores in third position
2 - multiply
3 - takes single int as input and sames to position
4 - outputs value of position
5 - jump-if-true, if first param != 0, then set instruction point to value from second param
6 - jump-if-false, if first param == 0
7 - less-than, if first param < second param, then stores 1 in position in third param
8 - greater-than
*/

void IntcodeComputer::calculate(deque<int>& program, int start_input) {
    deque<int> inputs = {start_input};
    int i = 0;
    while (i < program.size()) {
        // cout << i << ' ' << inputs[i] << endl;
        // printvector(inputs);
        if (program[i] == 99) {
            break;
        }
        i = operate(program, i, inputs);
    }
}


int IntcodeComputer::amplify(deque<int>& program, int phase_setting, int input) {
    deque<int> inputs = {phase_setting, input};
    idx = 0;
    while (idx < program.size()) {
        // cout << i << ' ' << inputs[i] << endl;
        // printvector(inputs);
        if (program[idx] == 99) {
            return res;
        }
        idx = operate(program, idx, inputs);
    }
    return INT_MIN;
}


// TODO
int IntcodeComputer::amplifyloop(deque<int>& program, int phase_setting, int input) {
    deque<int> inputs = {phase_setting, input};
    // reset res
    res = INT_MIN;
    while (idx < program.size() && res != INT_MIN) {
        // cout << i << ' ' << inputs[i] << endl;
        // printvector(inputs);
        if (program[idx] == 99) {
            return res;
        }
        idx = operate(program, idx, inputs);
    }
    return res;
}


int IntcodeComputer::interpretvalue(deque<int>& program, int mode, int value) {
    if (mode == 0) return program[value]; // position mode
    return value; // immediate mode
}


int IntcodeComputer::operate(deque<int>& program, int i, deque<int>& inputs) {
    int base = program[i];
    int op = base % 100;
    int mode1 = (base % 1000) / 100;
    int mode2 = (base % 10000) / 1000;

    if (op == 1) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        int v3 = program[i+3];
        program[v3] = v1 + v2;
        return i+4;

    } else if (op == 2) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        int v3 = program[i+3];
        program[v3] = v1 * v2;
        return i+4;

    } else if (op == 3) {
        // Assuming mode will be position
        // Assume input of 1 to start
        int v1 = program[i+1];
        // cout << "User input: ";
        // cin >> start;
        program[v1] = inputs.front();
        inputs.pop_front();
        return i+2;

    } else if (op == 4) {
        int v1 = program[i+1];
        cout << "Output: " << program[v1] << endl;
        res = program[v1];
        return i+2;

    } else if (op == 5) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        if (v1 != 0) {
            program[i] = v2;
            return v2;
        }
        return i+3;

    } else if (op == 6) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        if (v1 == 0) {
            program[i] = v2;
            return v2;
        }
        return i+3;

    } else if (op == 7) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        int v3 = program[i+3];
        if (v1 < v2) program[v3] = 1;
        else program[v3] = 0;
        return i+4;

    } else if (op == 8) {
        int v1 = interpretvalue(program, mode1, program[i+1]);
        int v2 = interpretvalue(program, mode2, program[i+2]);
        int v3 = program[i+3];
        if (v1 == v2) program[v3] = 1;
        else program[v3] = 0;
        return i+4;

    } else {
        cerr << "Unknown operation: " << base << endl;
        return INT_MAX;
    }
}