// Day 4. Secure Container
// https://adventofcode.com/2019/day/4
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

auto read_input() {
    string line;
    ifstream input("inputs/day04_input.txt");
    getline(input, line);
    int idx = line.find("-");
    return pair<int, int>{stoi(line.substr(0, idx)), stoi(line.substr(idx+1))};
}

// 6 digit number
// value within the range of input
// two adjacent digits are the same
// digits never decrease


int join_vector(vector<int>& v) {
    int s = 0;
    for (int n : v) {
        s = s*10 + n;
    }
    return s;
}


bool contains_duplicate(vector<int>& v) {
    set<int> seen;
    for (int n : v) {
        if (seen.count(n)) { return true; }
        seen.insert(n);
    }
    return false;
}

bool contains_duplicates2(vector<int>& v) {
    unordered_map<int, int> counts;
    for (int n : v) {
        counts[n]++;
    }

    // Need a group of exactly 2 
    for (auto k : counts) {
        if (k.second == 2) {
            return true;
        }
    }
    return false;
}


set<int> res1 = {};
set<int> res2 = {};

void dfs(vector<int>& v, int i){
    if (i == 5) {
        int n = join_vector(v);
        if (contains_duplicate(v)) {
            res1.insert(n);
        }

        if (contains_duplicates2(v)) {
            res2.insert(n);
        }
        return;
    }

    for (int j = v[i]; j <= 9; j++) {
        v[i+1] = j;
        dfs(v, i+1);
    }
} 


void part1_and_2() {
    pair<int, int> range = read_input();
    int low = range.first;
    int high = range.second;
    // cout << low << ' ' << high << endl;

    vector<int> v = {1, 1, 1, 1, 1, 1};

    for (int i=1; i <= 9; i++) {
        v[0] = i;
        dfs(v, 0);
    }

    int count = 0;
    for (int r : res1) {
        if (r >= low && r <= high) {
            // cout << r << endl;
            count++;
        }
    }
    cout << "Solution 1: " << count << endl;

    count = 0;
    for (int r : res2) {
        if (r >= low && r <= high) {
            // cout << r << endl;
            count++;
        }
    }
    cout << "Solution 2: " << count << endl;
}



int main() {
    part1_and_2();
}