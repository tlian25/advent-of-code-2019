// Day 1. The Tyranny of the Rocket Equation
// https://adventofcode.com/2019/day/1
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

auto read_input() {
    string line;
    vector<int> lines;
    ifstream input("inputs/day01_input.txt");
    while (getline(input, line)) {
        lines.push_back(stoi(line));
    }
    input.close();
    return lines;
}

/*
To launch a given module based on mass
fuel = mass / 3 - 2
*/

int calc_fuel(int mass) {
    int fuel = mass / 3 - 2;
    if (fuel <= 0) {
        return 0;
    }
    return fuel;
}

void solution1() {
    vector<int> modules = read_input();
    int sum = 0;
    for (int m : modules) {
        sum += calc_fuel(m);
    }

    cout << "Solution 1: " << sum << endl;
}



void solution2() {
    vector<int> modules = read_input();
    vector<int> nxt_modules = {};
    int sum = 0;
    int s = 0;

    while (modules.size() > 0) {
        nxt_modules = {};
        for (int m : modules) {
            s = calc_fuel(m);
            if (s > 0) {
                sum += s;
                nxt_modules.push_back(s);
            }
        }
        modules = nxt_modules;
    }
    cout << "Solution 2: " << sum << endl;
}


int main() {
    solution1();
    solution2();
}