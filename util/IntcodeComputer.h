#ifndef INTCODE_H
#define INTCODE_H

#include<iostream>
#include<deque>

using namespace std;

class IntcodeComputer {
    public:
    int res;
    int idx = 0;
    deque<int> program;
    void calculate(deque<int>& program, int start_input);
    int amplify(deque<int>& program, int phase_setting, int input);
    int amplifyloop(deque<int>& program, int phase_setting, int input);

    private:
    int interpretvalue(deque<int>& program, int mode, int value);
    int operate(deque<int>& program, int i, deque<int>& inputs);
};

#endif