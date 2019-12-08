#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>
#include <string>

#include "ReadInputs.hh"

using segment = std::pair<char,int>;
std::vector<std::vector<segment> > parse_wires(std::string filename) {
  auto contents = read_file(filename);

  std::vector<std::vector<segment> > all_wires;
  std::vector<segment> wire;

  char direction = 0;
  int distance = 0;
  for(auto c : contents) {
    if (c == 'R' || c=='L' || c=='U' || c=='D') {
      direction = c;
    } else if(c >= '0' && c <= '9') {
      int value = c-'0';
      distance = distance*10 + value;
    } else {
      wire.push_back({direction,distance});
      direction = 0;
      distance = 0;
    }

    if(c == '\n') {
      all_wires.push_back(std::move(wire));
      wire = std::vector<segment>();
    }
  }

  return all_wires;
}

// struct point {
//   point(int x, int y) : x(x), y(y) { }

//   int x;
//   int y;
// };
using point = std::pair<int,int>;

std::map<point,int> wire_locations(std::vector<segment> wire) {
  int x = 0;
  int y = 0;
  int distance = 0;

  std::map<point,int> output;

  for(auto seg : wire) {
    int dx = 0;
    int dy = 0;
    if(seg.first == 'L') {
      dx = -1;
      dy = 0;
    } else if (seg.first == 'R') {
      dx = 1;
      dy = 0;
    } else if (seg.first == 'U') {
      dx = 0;
      dy = 1;
    } else if (seg.first == 'D') {
      dx = 0;
      dy = -1;
    }

    for(int i=0; i<seg.second; i++) {
      x += dx;
      y += dy;
      distance += 1;

      if(!output.count({x,y})) {
        output[{x,y}] = distance;
      }
    }
  }

  return output;
}

std::vector<point> find_intersections(std::map<point,int> a,
                                      std::map<point,int> b) {
  std::vector<point> output;

  for(auto& pair : a) {
    if(b.count(pair.first)) {
      output.push_back(pair.first);
    }
  }

  return output;
}

int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);

  std::map<point,int> distances;

  auto wires = parse_wires(puzzle_input_file);
  auto path_a = wire_locations(wires[0]);
  auto path_b = wire_locations(wires[1]);
  auto intersections = find_intersections(path_a, path_b);

  auto manhattan = [&](point p) { return std::abs(p.first) + std::abs(p.second); };
  auto wire_distance = [&](point p) { return path_a[p] + path_b[p]; };

  auto closest_manhattan = *std::min_element(
    intersections.begin(),
    intersections.end(),
    [&](point a, point b) { return manhattan(a) < manhattan(b); } );
  std::cout << "Part a" << std::endl;
  std::cout << "(" << closest_manhattan.first
            << ", " << closest_manhattan.second
            << ") --> " << manhattan(closest_manhattan)
            << std::endl;

  auto closest_wire = *std::min_element(
    intersections.begin(),
    intersections.end(),
    [&](point a, point b) { return wire_distance(a) < wire_distance(b); } );
  std::cout << "Part b" << std::endl;
  std::cout << "(" << closest_wire.first
            << ", " << closest_wire.second
            << ") --> " << wire_distance(closest_wire)
            << std::endl;
}
