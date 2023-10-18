// Day 5. Sunny with a Chance of Asteroids
// https://adventofcode.com/2019/day/5
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<deque>

using namespace std;

auto read_input() {
    string line;
    deque<int> lines;
    ifstream input("inputs/day05_input.txt");
    while (getline(input, line, ',')) {
        lines.push_back(stoi(line));
    }
    
    input.close();
    return lines;
}


void printvector(deque<int>& v) {
    cout << "[ ";
    for (int n : v) {
        cout << n << ' ';
    }
    cout << "]" << endl;
}


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

int interpretvalue(deque<int>& inputs, int mode, int value) {
    if (mode == 0) return inputs[value]; // position mode
    return value; // immediate mode
}

int operate(deque<int>& inputs, int i, int start) {
    int base = inputs[i];
    int op = base % 100;
    int mode1 = (base % 1000) / 100;
    int mode2 = (base % 10000) / 1000;
    // int mode3 = (base % 100000) / 10000;

    if (op == 1) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        // int v3 = interpretvalue(inputs, mode3, inputs[i+3]);
        int v3 = inputs[i+3];
        inputs[v3] = v1 + v2;
        // if (base != inputs[i]) return i;
        return i+4;

    } else if (op == 2) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        // int v3 = interpretvalue(inputs, mode3, inputs[i+3]);
        int v3 = inputs[i+3];
        inputs[v3] = v1 * v2;
        // if (base != inputs[i]) return i;
        return i+4;

    } else if (op == 3) {
        // Assuming mode will be position
        // Assume input of 1 to start
        int v1 = inputs[i+1];
        // cout << "User input: ";
        // cin >> start;
        inputs[v1] = start;
        return i+2;

    } else if (op == 4) {
        int v1 = inputs[i+1];
        cout << "Output: " << inputs[v1] << endl;
        return i+2;

    } else if (op == 5) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        if (v1 != 0) {
            inputs[i] = v2;
            return v2;
        }
        return i+3;

    } else if (op == 6) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        if (v1 == 0) {
            inputs[i] = v2;
            return v2;
        }
        return i+3;

    } else if (op == 7) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        // int v3 = interpretvalue(inputs, mode3, inputs[i+3]);
        int v3 = inputs[i+3];
        if (v1 < v2) inputs[v3] = 1;
        else inputs[v3] = 0;
        // if (base != inputs[i]) return i;
        return i+4;

    } else if (op == 8) {
        int v1 = interpretvalue(inputs, mode1, inputs[i+1]);
        int v2 = interpretvalue(inputs, mode2, inputs[i+2]);
        // int v3 = interpretvalue(inputs, mode3, inputs[i+3]);
        int v3 = inputs[i+3];
        if (v1 == v2) inputs[v3] = 1;
        else inputs[v3] = 0;
        // if (base != inputs[i]) return i;
        return i+4;

    } else {
        cerr << "Unknown operation: " << base << endl;
        return INT_MAX;
    }
}





void part1() {
    cout << "Solution 1" << endl;
    deque<int> inputs = read_input();
    int i = 0;
    while (i < inputs.size()) {
        // cout << i << ' ' << inputs[i] << endl;
        if (inputs[i] == 99) {
            break;
        }
        i = operate(inputs, i, 1);
    }
}


void part2() {
    cout << "Solution 2" << endl;
    deque<int> inputs = read_input();
    int i = 0;
    while (i < inputs.size()) {
        // cout << i << ' ' << inputs[i] << endl;
        // printvector(inputs);
        if (inputs[i] == 99) {
            break;
        }
        i = operate(inputs, i, 5);
    }
}


int main() {
    part1();
    part2();
}