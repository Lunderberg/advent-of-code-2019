#include <algorithm>
#include <iostream>
#include <string>

#include "ReadInputs.hh"

int fuel(int weight, bool tyranny=false) {
  int output = std::max(weight/3 - 2, 0);

  if(output && tyranny) {
    return output + fuel(output, true);
  } else {
    return output;
  }
}

int main(int argc, char** argv) {
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);

  auto inputs = read_integers(puzzle_input_file);

  int total_fuel = 0;
  for(auto weight : inputs) {
    total_fuel += fuel(weight);
  }
  std::cout << "Without tyranny: " << total_fuel << std::endl;

  total_fuel = 0;
  for(auto weight : inputs) {
    total_fuel += fuel(weight, true);
  }
  std::cout << "With tyranny: " << total_fuel << std::endl;
}
