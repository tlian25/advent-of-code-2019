// Day 3. Crossed Wires
// https://adventofcode.com/2019/day/3
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

// for string delimiter
std::vector<std::string> split(string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<std::string> res;

    while ((pos_end = s.find(delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}

auto read_input() {
    string line;
    vector<string> wire1;
    vector<string> wire2;
    ifstream input("inputs/day03_input.txt");
    // Wire 1
    getline(input, line);
    wire1 = split(line, ",");
    // cout << "Wire 1 size: " << wire1.size() << endl;
    
    getline(input, line);
    wire2 = split(line, ",");
    // cout << "Wire 2 size: " << wire2.size() << endl;
    input.close();
    return pair<vector<string>, vector<string>>{wire1, wire2};
}

string hashkey(int row, int col) {
    return to_string(row) + ":" + to_string(col);
}

pair<int, int> hashkeytocoord(string key) {
    int idx = key.find(':');
    int r = stoi(key.substr(0, idx));
    int c = stoi(key.substr(idx+1));
    return pair<int, int>{r, c};
}



void mark_grid(unordered_map<string, int>& grid, string dir, vector<int>& state) {
    // Get direction and count from dir
    int dr = 0, dc = 0;
    switch (dir[0]) {
        case 'U':
            dr = -1;
            break;
        case 'D':
            dr = 1;
            break;
        case 'R':
            dc = 1;
            break;
        case 'L':
            dc = -1;
            break;
        default:
            cerr << "Unknown direction: " << dir << endl;
    }

    int s = stoi(dir.substr(1)); // steps
    string key;
    while (s > 0) {
        state[0] += dr;
        state[1] += dc;
        state[2]++;
        key = hashkey(state[0], state[1]);
        if (!grid.count(key)) {
            grid[key] = state[2];
        }
        s--;
    }
}


int manhattan_dist(pair<int, int> cell) {
    return abs(cell.first) + abs(cell.second);
}


void part1_and_2() {
    auto p = read_input();
    vector<string> w1 = p.first;
    vector<string> w2 = p.second;

    unordered_map<string, int> grid1 = {};
    unordered_map<string, int> grid2 = {};

    // state = row, col, steps
    vector<int> state = {0, 0, 0};
    for (string d : w1) {
        mark_grid(grid1, d, state);
    }

    // reset state for grid2
    state = {0, 0, 0};
    for (string d : w2) {
        mark_grid(grid2, d, state);
    }


    int mindist = INT_MAX;
    int minsteps = INT_MAX;
    for (auto cell : grid1) {
        if (grid2.count(cell.first)) {
            mindist = min(mindist, manhattan_dist(hashkeytocoord(cell.first)));
            minsteps = min(minsteps, grid1[cell.first] + grid2[cell.first]);
        }
    }

    cout << "Solution 1: " << mindist << endl;
    cout << "Solution 2: " << minsteps << endl;
}



int main() {
    part1_and_2();
}