#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "ReadInputs.hh"

using Edge = std::pair<std::string, std::string>;


void part_a(const std::vector<Edge>& edges) {
  std::map<std::string, int> distance;
  distance["COM"] = 0;

  while(distance.size() != edges.size()+1) {
    for(auto edge : edges) {
      if(distance.count(edge.first) && !distance.count(edge.second)) {
        distance[edge.second] = distance[edge.first] + 1;
      }
    }
  }

  int sum = 0;
  for(auto pair : distance) {
    sum += pair.second;
  }
  std::cout << "Total direct+indirect orbits: " << sum << std::endl;
}


void part_b(const std::vector<Edge>& edges) {
  std::map<std::string, std::string> parent;
  for(const auto& edge : edges) {
    parent[edge.second] = edge.first;
  }

  auto path_to_com = [&](std::string start) {
    std::vector<std::string> path{start};
    while(start != "COM") {
      start = parent[start];
      path.push_back(start);
    }
    return path;
  };

  auto you_path = path_to_com("YOU");
  auto san_path = path_to_com("SAN");

  while(you_path.back() == san_path.back()) {
    you_path.pop_back();
    san_path.pop_back();
  }
  int num_transfers = you_path.size() + san_path.size() - 2;
  std::cout << "Number of transfers: " << num_transfers << std::endl;
}


int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);
  auto lines = read_lines(puzzle_input_file);



  std::vector<Edge> edges;
  for(auto line : lines) {
    std::string parent = line.substr(0,3);
    std::string child = line.substr(4,7);
    edges.push_back({parent, child});
  }
  part_a(edges);
  part_b(edges);
}
