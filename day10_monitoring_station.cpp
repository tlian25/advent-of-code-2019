// Day 10. Monitoring Station
// https://adventofcode.com/2019/day/10
#include<iostream>
#include<fstream>
#include<set>
#include<cmath>

using namespace std;

char EMPTY = '.';
char ASTEROID = '#';
double INF = (double) INT_MAX;

auto read_input() {
    string line;
    vector<vector<char>> grid;
    ifstream input("inputs/day10_input.txt");
    while (getline(input, line)) {
        vector<char> l(line.begin(), line.end());
        grid.push_back(l);
    }
    input.close();
    return grid;
}


// Map of all asteroids
// best location is the asteroid that can detect the largest number of other asteroids
// Build a relationship map. If A can see B, then B can see A
// Exact ray tracing out of each asteroid
// Create a map of slopes for each asteroid vs all other asteroids
// Get min distance on each slope

struct Coord {
    int x;
    int y;
};


void printCoord(Coord& c) {
    cout << "Coord: (" << c.x << ", " << c.y << ")" << endl;
}


double calcSlope(Coord& c1, Coord& c2) {
    if (c1.x - c2.x == 0) { return INF; }
    return (double) (c1.y - c2.y) / (double) (c1.x - c2.x);
}


int canSee(Coord& self, vector<Coord>& asteroids) {
    // count number of unique slopes, but one in each direction
    
    // keep track of slopes for asteroids above self and below self separately
    set<double> above;
    set<double> below;
    set<double> left;
    set<double> right;
    double slope;

    for (auto a : asteroids) {
        slope = calcSlope(self, a);
        if (a.y == self.y && a.x == self.x) {
            continue; // self
        } else if (a.y > self.y) {
            above.insert(slope);
        } else if (a.y < self.y) {
            below.insert(slope);
        } else if (a.x < self.x) {
            // same line y's equal
            right.insert(slope);
        } else {
            left.insert(slope);
        }
    }

    return above.size() + below.size() + left.size() + right.size();
}


void part1() {
    auto grid = read_input();
    vector<Coord> asteroids;

    for (int y=0; y<grid.size(); y++) {
        for (int x=0; x<grid[y].size(); x++) {
            if (grid[y][x] == ASTEROID) {
                Coord c{x, y};
                asteroids.push_back(c);
            }
        }
    }

    Coord mxcoord;
    int mxcount = 0;
    int count;
    for (auto self : asteroids) {
        count = canSee(self, asteroids);
        if (count > mxcount) {
            mxcount = count;
            mxcoord = self;
        }
        
    }

    cout << "Solution 1: " << mxcount << endl;
    cout << "Best Location: (" << mxcoord.x << ", " << mxcoord.y << ')' << endl;

}



int calcMult(Coord& c) {
    cout << "Calculate: " << c.x << ' ' << c.y << endl;
    return 100 * c.x + c.y;
}


int lazer(Coord station, vector<Coord>& asteroids) {
    // keep track of slopes for asteroids above self and below self separately
    unordered_map<double, vector<Coord>> above;
    unordered_map<double, vector<Coord>> below;
    unordered_map<double, vector<Coord>> right;
    unordered_map<double, vector<Coord>> left;
    double slope;

    for (auto a : asteroids) {
        slope = calcSlope(station, a);
        if (a.y == station.y && a.x == station.x) {
            continue; // station
        }
        
        if (a.x > station.x) {
            right[slope].push_back(a);
        } else if (a.x < station.x) {
            left[slope].push_back(a);
        } else if (a.y < station.y) {
            // same line y's equal
            above[slope].push_back(a);
        } else {
            below[slope].push_back(a);
        }
    }

    vector<double> rightslopes;
    vector<double> leftslopes;


    int x0 = station.x;
    int y0 = station.y;

    for (auto p : right) {
        rightslopes.push_back(p.first);
        // sort asteroids by distance from station
        sort(p.second.begin(), p.second.end(),
            [](const Coord& c1, const Coord& c2) {
                return (abs(c1.x - 11) + abs(c1.y - 13)) > (abs(c2.x-11) + abs(c2.y-13));
            });
    }
    sort(rightslopes.begin(), rightslopes.end(), greater<>());
        

    for (auto p: left) {
        leftslopes.push_back(p.first);
        sort(p.second.begin(), p.second.end(),
            [](const Coord& c1, const Coord& c2) {
                return (abs(c1.x - 11) + abs(c1.y - 13)) > (abs(c2.x-11) + abs(c2.y-13));
            });
    }
    sort(leftslopes.begin(), leftslopes.end(), greater<>());

    // Sort each direction and slope in order

    // Lazer
    int count = 0;
    Coord curr;

    // Rotate clockwise
    while (count < 200) {
        cout << "Count: " << count << endl;
        // 12 oclock
        if (above[INF].size() > 0) {
            printCoord(above[INF].back());
            if (++count == 200) {
                return calcMult(above[INF].back());
            }
            above[INF].pop_back();
        }

        for (auto s : rightslopes) {
            if (right[s].size() > 0) {
                printCoord(right[s].back());
                if (++count == 200) {
                    return calcMult(right[s].back());
                }
                right[s].pop_back();
            }
        }

        // 6 oclock
        if (below[INF].size() > 0) {
            printCoord(below[INF].back());
            if (++count == 200) {
                return calcMult(below[INF].back());
            }
            below[INF].pop_back();
        }

        for (auto s : leftslopes) {
            if (left[s].size() > 0) {
                printCoord(left[s].back());
                if (++count == 200) {
                    return calcMult(left[s].back());
                }
                left[s].pop_back();
            }
        }
    }

    return -1;
}




void part2() {
    auto grid = read_input();
    vector<Coord> asteroids;

    for (int y=0; y<grid.size(); y++) {
        for (int x=0; x<grid[y].size(); x++) {
            if (grid[y][x] == ASTEROID) {
                Coord c{x, y};
                asteroids.push_back(c);
            }
        }
    }

    // from Part 1
    Coord station{11, 13};

    // Laser starts at 12 o'clock and moves clockwise
    //
    int res = lazer(station, asteroids);
    cout << "Solution 2: " << res << endl;

}


int main() {
    part1();
    part2();
}