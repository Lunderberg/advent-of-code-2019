#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <map>
#include <vector>

#include "ReadInputs.hh"

using point = std::pair<int,int>;

int gcd(int a, int b) {
  if(a<0 || b<0) {
    return gcd(std::abs(a), std::abs(b));
  } else if (a==0) {
    return b;
  } else if (b==0) {
    return a;
  } else if(a==b) {
    return a;
  } else if(a > b) {
    return gcd(a-b, b);
  } else {
    return gcd(a, b-a);
  }
}

std::map<point, std::vector<point> >
group_by_direction(const std::vector<point>& asteroids, point pos) {
  std::map<point, std::vector<point> > output;

  for(const auto& asteroid : asteroids) {
    point direction{pos.first - asteroid.first, pos.second - asteroid.second};
    if(direction.first || direction.second) {
      int scale = gcd(direction.first, direction.second);
      direction.first /= scale;
      direction.second /= scale;

      output[direction].push_back(asteroid);
    }
  }

  return output;
}

int get_num_visible(const std::vector<point>& asteroids, point pos) {
  return group_by_direction(asteroids, pos).size();
}

std::vector<point> get_order_destroyed(const std::vector<point>& asteroids, point pos) {

  std::map<double, std::vector<point> > grouped;
  for(auto& group : group_by_direction(asteroids, pos)) {
    auto& direction = group.first;
    double angle = std::atan2(-direction.first, direction.second);
    std::sort(group.second.begin(), group.second.end(),
              [&](point& a, point& b) {
                int dist_a = std::abs(a.first - pos.first) + std::abs(a.second - pos.second);
                int dist_b = std::abs(b.first - pos.first) + std::abs(b.second - pos.second);
                return dist_b < dist_a;
              });

    grouped[angle] = group.second;
  }


  std::vector<point> output;
  bool values_remain = true;
  while(values_remain) {
    values_remain = false;
    for(auto& group : grouped) {
      if(group.second.size()) {
        output.push_back(group.second.back());
        group.second.pop_back();
        values_remain = true;
      }
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
  auto lines = read_lines(puzzle_input_file);

  std::vector<point> asteroids;
  for(unsigned int i=0; i<lines.size(); i++) {
    const auto& line = lines.at(i);
    for(unsigned int j=0; j<line.size(); j++) {
      if(line[j]=='#') {
        asteroids.push_back({j,i});
      }
    }
  }

  int most_visible = 0;
  point best_pos{0,0};
  for(const auto& pos : asteroids) {
    int num_visible = get_num_visible(asteroids, pos);

    if(num_visible > most_visible) {
      most_visible = num_visible;
      best_pos = pos;
    }
  }

  std::cout << "(" << best_pos.first << ", " << best_pos.second << ")" << std::endl;
  std::cout << "Num visible: " << most_visible << std::endl;

  auto order_destroyed = get_order_destroyed(asteroids, best_pos);
  if(order_destroyed.size() >= 200) {
    std::cout << "200th destroyed: (" << order_destroyed[199].first << ", " << order_destroyed[199].second << ")" << std::endl;
  } else {
    std::cout << "Error somewhere, not enough asteroids destroyed" << std::endl;
  }
  // std::cout << "----------" << std::endl;
  // for(auto pos : order_destroyed) {
  //   std::cout << "(" << pos.first << ", " << pos.second << ")" << std::endl;
  // }
}
