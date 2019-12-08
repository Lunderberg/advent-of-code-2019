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

  auto inputs = read_integers(argv[1]);
  std::cout << "1202 -> " << apply_func(12, 2, inputs) << std::endl;

  for(int a=0; a<100; a++) {
    for(int b=0; b<100; b++) {
      if(apply_func(a,b,inputs) == 19690720) {
        std::cout << a << ", " << b << " --> " << 19690720 << std::endl;
      }
    }
  }
}
