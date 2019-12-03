#include "IntCode.hh"

#include <iostream>
#include <utility>

IntCode::IntCode(std::vector<int> initial_memory)
  : memory(std::move(initial_memory)), ip(0) { }

bool IntCode::iterate() {
  int opcode = at(ip);
  if (opcode == 1) {
    op_add();
  } else if (opcode == 2) {
    op_mul();
  }

  return (opcode == 99);
}

void IntCode::iterate_until_done() {
  bool done = false;
  while(!done) {
    done = iterate();
  }
}

int& IntCode::at(int i) {
  return memory.at(i);
}

int IntCode::value_at(int i) const {
  return memory.at(i);
}

void IntCode::op_add() {
  int a = at(at(ip+1));
  int b = at(at(ip+2));
  int x = a + b;

  at(at(ip+3)) = x;

  ip += 4;
}

void IntCode::op_mul() {
  int a = at(at(ip+1));
  int b = at(at(ip+2));
  int x = a * b;

  at(at(ip+3)) = x;

  ip += 4;
}
