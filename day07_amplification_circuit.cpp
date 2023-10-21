// Day 7. Amplification Circuit
// https://adventofcode.com/2019/day/7
#include<iostream>
#include<fstream>
#include<algorithm>
#include<set>
#include<cmath>
#include "util/IntcodeComputer.h"

using namespace std;

auto read_input() {
    string line;
    deque<int> lines;
    ifstream input("inputs/day07_input.txt");
    while (getline(input, line, ',')) {
        lines.push_back(stoi(line));
    }
    input.close();
    return lines;
}

// each amplifier runs a copy of the program
// phase setting - 0-4, each setting used once
// input signal -> output signal
// find largest output signal that can be send to the thrusters
// first input is 0



int run_phase_settings(vector<int>& phase_settings) {
    deque<int> program;
    IntcodeComputer computer;
    vector<string> amps = {"A", "B", "C", "D", "E"};
    int input = 0;
    for (int i=0; i<phase_settings.size(); i++) {
        cout << "Amp: " << amps[i] << " Phase: " << phase_settings[i] << " Input: " << input << endl;
        program = read_input();
        input = computer.amplify(program, phase_settings[i], input);
    }

    cout << input << endl;
    return input;
}


void part1() {

    vector<int> phase_settings = {0, 1, 2, 3, 4};
    int mx = INT_MIN;
    int m;

    // Find max among all possible permutations of phase settings
    do {
        m = run_phase_settings(phase_settings);
        mx = max(mx, m);
    } while (next_permutation(phase_settings.begin(), phase_settings.end()));

    cout << "Solution 1: " << mx << endl;
}



int run_phase_settings_loop(vector<int>& phase_settings) {
    deque<int> program;
    unordered_map<string, IntcodeComputer> computers;

    vector<string> amps = {"A", "B", "C", "D", "E"};

    for (string a : amps) {
        computers[a] = IntcodeComputer();
    }

    IntcodeComputer computer;
    string amp;
    int input = 0;
    int i = 0;
    while (true) {
        amp = amps[i];
        computer = computers[amp];
        cout << "Amp: " << amp << " Phase: " << phase_settings[i] << " Input: " << input << endl;
        program = read_input();
        input = computer.amplifyloop(program, phase_settings[i], input);
        i = (i+1) % 5;
    }

    cout << input << endl;
    return input;
}

void part2() {
    vector<int> phase_settings = {5, 6, 7, 8, 9};
    int mx = INT_MIN;
    int m;

    do {
        m = run_phase_settings(phase_settings);
        mx = max(mx, m);
    } while (next_permutation(phase_settings.begin(), phase_settings.end()));

    cout << "Solution 2: " << mx << endl;

}


int main() {
    part1();
    part2();
}