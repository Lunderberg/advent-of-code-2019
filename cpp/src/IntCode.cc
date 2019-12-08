#include "IntCode.hh"

#include <iostream>
#include <sstream>
#include <stdexcept>
#include <utility>

IntCode::IntCode(std::vector<int> initial_memory)
  : memory(std::move(initial_memory)), ip(0) { }

void IntCode::send_input(int i) {
  inputs.push(i);
}

int IntCode::get_output() {
  int output = outputs.front();
  outputs.pop();
  return output;
}

bool IntCode::iterate() {
  int opcode = at(ip) % 100;

  switch(opcode) {
    case 1:
      op_add();
      break;
    case 2:
      op_mul();
      break;
    case 3:
      op_input();
      break;
    case 4:
      op_output();
      break;
    case 5:
      op_jump_if_true();
      break;
    case 6:
      op_jump_if_false();
      break;
    case 7:
      op_lt();
      break;
    case 8:
      op_eq();
      break;
    case 9:
      break;
    case 99:
      break;
    default:
    {
      std::stringstream ss;
      ss << "Unknown opcode: " << opcode << " at ip " << ip;
      throw std::runtime_error(ss.str());
    }
      break;
  }

  return (opcode == 99);
}

void IntCode::iterate_until_done() {
  bool done = false;
  while(!done) {
    done = iterate();
  }
}

int IntCode::get_param(int param) {
  int mode = memory.at(ip)/100;
  for(int i=1; i<param; i++) {
    mode /= 10;
  }
  mode %= 10;

  int value = memory.at(ip+param);
  if(!mode) {
    value = memory.at(value);
  }
  return value;
}

int& IntCode::at(int i) {
  return memory.at(i);
}

int IntCode::value_at(int i) const {
  return memory.at(i);
}

void IntCode::op_add() {
  int a = get_param(1);
  int b = get_param(2);
  int x = a + b;

  at(at(ip+3)) = x;

  ip += 4;
}

void IntCode::op_mul() {
  int a = get_param(1);
  int b = get_param(2);
  int x = a * b;

  at(at(ip+3)) = x;

  ip += 4;
}

void IntCode::op_input() {
  int x = inputs.front();
  inputs.pop();
  at(at(ip+1)) = x;
  ip += 2;
}

void IntCode::op_output() {
  int x = get_param(1);
  outputs.push(x);
  ip += 2;
}

void IntCode::op_jump_if_true() {
  int a = get_param(1);
  int b = get_param(2);

  if(a) {
    ip = b;
  } else {
    ip += 3;
  }
}

void IntCode::op_jump_if_false() {
  int a = get_param(1);
  int b = get_param(2);

  if(!a) {
    ip = b;
  } else {
    ip += 3;
  }
}

void IntCode::op_lt() {
  int a = get_param(1);
  int b = get_param(2);
  int x = a < b;

  at(at(ip+3)) = x;

  ip += 4;
}

void IntCode::op_eq() {
  int a = get_param(1);
  int b = get_param(2);
  int x = a == b;

  at(at(ip+3)) = x;

  ip += 4;
}
