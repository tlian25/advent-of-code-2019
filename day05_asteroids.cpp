// Day 5. Sunny with a Chance of Asteroids
// https://adventofcode.com/2019/day/5
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>
#include<deque>
#include "util/IntcodeComputer.h"

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


// IntcodeComputer defined in util folder

void part1() {
    cout << "Solution 1" << endl;
    deque<int> program = read_input();
    int start_value = 1;
    IntcodeComputer().calculate(program, start_value);
}


void part2() {
    cout << "Solution 2" << endl;
    deque<int> program = read_input();
    int start_value = 5;
    IntcodeComputer().calculate(program, start_value);
}


int main() {
    part1();
    part2();
}