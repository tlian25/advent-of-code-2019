// Day 6. Universal Orbit Map
// https://adventofcode.com/2019/day/6
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

struct Node {
    string name;
    string orbits;
};


auto read_input() {
    string line;
    string DELIMITER = ")";
    vector<string> lines;
    ifstream input("inputs/day06_input.txt");
    unordered_map<string, Node> dag;
    string a;
    string b;
    while (getline(input, line)) {
        int idx = line.find(DELIMITER);
        a = line.substr(0, idx);
        b = line.substr(idx+1);
        // cout << a << " -> " << b << endl;
        if (!dag.count(a)) {
            Node na;
            na.name = a;
            dag[a] = na; 
        }

        if (!dag.count(b)) {
            Node nb;
            nb.name = b;
            dag[b] = nb;
        }
        dag[b].orbits = a;
    }
    input.close();
    return dag;
}


// Orbit Count Checksums
// Direct orbits
// indirect orbits
// Construct DAG
string COM = "COM";
string YOU = "YOU";
string SAN = "SAN";

int traverse(string node, unordered_map<string, Node>& dag) {
    int count = 0;
    string curr = node;
    while (curr != COM) {
        curr = dag[curr].orbits;
        count++;
    }
    return count;
}


void part1() {
    auto dag = read_input();
    int counts = 0;

    for (auto node : dag) {
        counts += traverse(node.first, dag);
    }
    cout << "Solution 1: " << counts << endl;
}


int you2santa(unordered_map<string, Node>& dag) {


    vector<string> path = {};
    set<string> seen = {};

    // Traverse YOU -> COM
    string curr = YOU;
    while (curr != COM) {
        curr = dag[curr].orbits;
        seen.insert(curr);
        path.push_back(curr);
    }

    path.push_back(COM);
    seen.insert(COM);

    // Traverse SAN -> COM until path intersects with a seen
    // Count hops in total

    curr = SAN;
    int count = 0;
    while (!seen.count(curr)) {
        curr = dag[curr].orbits;
        count++;
    }

    for (int i=0; i<path.size(); i++) {
        if (path[i] == curr) {
            return count + i - 1;
        }
    }
    return -1;
}

void part2() {
    auto dag = read_input();
    int count = you2santa(dag);
    cout << "Solution 2: " << count << endl;
}


int main() {
    part1();
    part2();
}