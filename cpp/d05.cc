#include <iostream>

#include "ReadInputs.hh"
#include "IntCode.hh"

int apply_func(int a, int b, std::vector<int> memory) {
  memory[1] = a;
  memory[2] = b;

  IntCode interp(std::move(memory));
  interp.iterate_until_done();
  return interp.value_at(0);
}

int main(int argc, char** argv) {
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  auto memory = read_integers(argv[1]);

  std::cout << "Part 1" << std::endl;
  {
    IntCode interp(memory);
    interp.send_input(1);
    interp.iterate_until_done();
    int output = 0;
    while(output == 0) {
      output = interp.get_output();
      std::cout << output << std::endl;
    }
  }

  std::cout << "Part 2" << std::endl;
  {
    IntCode interp(memory);
    interp.send_input(5);
    interp.iterate_until_done();
    std::cout << interp.get_output() << std::endl;
  }
}
