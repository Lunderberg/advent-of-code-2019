#include <iostream>

#include "ReadInputs.hh"

int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);
  // auto text = read_file(puzzle_input_file);
  // auto lines = read_lines(puzzle_input_file);
  // auto memory = read_integers(puzzle_input_file);
}
