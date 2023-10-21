// Day 8. Space Image Format
// https://adventofcode.com/2019/day/8
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

int COL = 25;
int ROW = 6;

auto read_input() {
    string line;
    vector<vector<int>> layers;
    ifstream input("inputs/day08_input.txt");
    getline(input, line);

    vector<int> layer = {};
    int i = 0;
    for (char s: line) {
        layer.push_back(s - '0');
        i++;
        if (i == COL * ROW) {
            layers.push_back(layer);
            layer = {};
            i = 0;
        }
    }
    return layers;
}


// digits that each represent the color of a single pixel
// digits fill each row of the image left->right-> down to next row


int count_nums(vector<int>& layer, int target) {
    int count = 0;
    for (int n: layer) {
        if (n == target) count++;
    }
    return count;
}


void part1() {
    vector<vector<int>> layers = read_input();
    int minzeros = INT_MAX;
    int res;

    for (auto layer : layers) {
        int zerocount = count_nums(layer, 0);
        if (zerocount < minzeros) {
            int onecount = count_nums(layer, 1);
            int twocount = count_nums(layer, 2);
            res = onecount * twocount;
            minzeros = min(minzeros, zerocount);
        }
        
    }
    cout << "Solution 1: " << res << endl;
}


// 0 - black
// 1 - white
// 2 - transparent
//

void printimage(vector<int>& image) {
    for (int i=0; i<image.size(); i++) {
        if (i % COL == 0) {
            cout << endl;
        }

        if (image[i] == 1) {
            cout << "\u2588";
        } else {
            cout << ' ';
        }
    }
    cout << endl;
}


void stacklayers(vector<int>& image, vector<int>& layer) {
    for (int i=0; i<image.size(); i++) {
        // transparent, pass down
        if (image[i] == 2) {
            image[i] = layer[i];
        }
        // else do nothing
    }
}

void part2() {
    vector<vector<int>> layers = read_input();
    vector<int> image = layers[0];

    for (auto layer : layers) {
        stacklayers(image, layer);
    }
    printimage(image);

}


int main() {
    part1();
    part2();
}