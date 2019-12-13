#include <iostream>

#include "ReadInputs.hh"
#include "IntCode.hh"

int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);
  auto memory = read_integers(puzzle_input_file);

  for(auto val : {1,2}) {
    IntCode interp(memory);
    interp.send_input(val);
    interp.iterate_until_done();
    std::cout << interp.get_output() << std::endl;
  }
}
