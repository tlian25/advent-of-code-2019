// Day 2. 1202 Program Alarm
// https://adventofcode.com/2019/day/2
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<deque>

using namespace std;

auto read_input() {
    string line;
    deque<int> lines;
    ifstream input("./inputs/day02_input.txt");
    while (getline(input, line, ',')) {
        lines.push_back(stoi(line));
    }
    
    input.close();
    return lines;
}

/*
Opcode - first int, 1, 2, 99
99 - finishes
1 add togther numbers read from two positions and stores in third position
2 -
*/

int operate(deque<int>& inputs, int i) {
    int idx1 = inputs[i+1];
    int idx2 = inputs[i+2];
    int idx3 = inputs[i+3];
    if (inputs[i] == 1) {
        inputs[idx3] = inputs[idx1] + inputs[idx2];
    } else if (inputs[i] == 2) {
        inputs[idx3] = inputs[idx1] * inputs[idx2];
    }
    return i+4;
}



int operate_search(int a, int b) {
    deque<int> inputs = read_input();
    // replace
    inputs[1] = a;
    inputs[2] = b;

    int i = 0;

    while (i < inputs.size()) {
        if (inputs[i] == 99) {
            break;
        }
        i = operate(inputs, i);
    }

    return inputs[0];
}



void part1() {
    deque<int> inputs = read_input();
    // replace
    int res = operate_search(12, 2);

    cout << "Solution 1: " << res << endl;
}


void part2() {
    int res;
    for (int a = 0; a < 100; a++) {
        for (int b = 0; b < 100; b++) {
            res = operate_search(a, b);
            if (res == 19690720) {
                cout << "Solution 2: " << 100 * a + b << " (" << a << ", " << b << ")" << endl;
            }
        }
    }
}


int main() {
    part1();
    part2();
}