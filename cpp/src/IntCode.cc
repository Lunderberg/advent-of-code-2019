#include "IntCode.hh"

#include <iostream>
#include <sstream>
#include <stdexcept>
#include <utility>

IntCode::IntCode(std::vector<long> initial_memory)
  : memory(std::move(initial_memory)),
    ip(0), relative_base(0),
    done(false), paused(false)
{ }

void IntCode::send_input(long i) {
  inputs.push(i);
  paused = false;
}

long IntCode::get_output() {
  if(outputs.size() == 0) {
    throw std::runtime_error("No output to get");
  }
  long output = outputs.front();
  outputs.pop();
  return output;
}

void IntCode::iterate() {
  long opcode = at(ip) % 100;

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
      op_adjust_relative_base();
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

  done = (opcode == 99);
}

void IntCode::iterate_until_done() {
  while(!done && !paused) {
    iterate();
  }
}

long IntCode::get_mode(long param) {
  long mode = at(ip)/100;
  for(long i=1; i<param; i++) {
    mode /= 10;
  }
  mode %= 10;
  return mode;
}

long IntCode::get_param(long param) {
  long mode = get_mode(param);

  long value = at(ip+param);
  if(mode==0) {
    value = at(value);
  } else if (mode==1) {
    value = value;
  } else if (mode==2) {
    value = at(value + relative_base);
  } else {
    std::stringstream ss;
    ss << "Unknown mode " << mode
       << " at ip=" << ip
       << ", value=" << at(ip);
    throw std::runtime_error(ss.str());
  }
  return value;
}

void IntCode::set_param(long param, long val) {
  long mode = get_mode(param);

  long addr = at(ip + param);
  if(mode==0) {
    set_memory(addr, val);
  } else if (mode==1) {
    throw std::runtime_error("Cannot use mode==1 (immediate mode) for output params");
  } else if (mode==2) {
    set_memory(addr + relative_base, val);
  } else {
    std::stringstream ss;
    ss << "Unknown mode " << mode
       << " at ip=" << ip
       << ", value=" << at(ip);
    throw std::runtime_error(ss.str());
  }
}

long IntCode::at(long i) {
  if((unsigned long)i < memory.size()) {
    return memory.at(i);
  } else {
    return 0;
  }
}

void IntCode::set_memory(long i, long val) {
  if((unsigned long)i >= memory.size()) {
    memory.resize(i+1, 0);
  }

  memory.at(i) = val;
}

long IntCode::value_at(long i) const {
  return memory.at(i);
}

void IntCode::op_add() {
  long a = get_param(1);
  long b = get_param(2);
  long x = a + b;

  set_param(3, x);

  ip += 4;
}

void IntCode::op_mul() {
  long a = get_param(1);
  long b = get_param(2);
  long x = a * b;

  set_param(3, x);

  ip += 4;
}

void IntCode::op_input() {
  if(inputs.size()) {
    long x = inputs.front();
    inputs.pop();
    set_param(1, x);
    ip += 2;
  } else {
    paused = true;
  }
}

void IntCode::op_output() {
  long x = get_param(1);
  outputs.push(x);
  ip += 2;
}

void IntCode::op_jump_if_true() {
  long a = get_param(1);
  long b = get_param(2);

  if(a) {
    ip = b;
  } else {
    ip += 3;
  }
}

void IntCode::op_jump_if_false() {
  long a = get_param(1);
  long b = get_param(2);

  if(!a) {
    ip = b;
  } else {
    ip += 3;
  }
}

void IntCode::op_lt() {
  long a = get_param(1);
  long b = get_param(2);
  long x = a < b;

  set_param(3, x);

  ip += 4;
}

void IntCode::op_eq() {
  long a = get_param(1);
  long b = get_param(2);
  long x = a == b;

  set_param(3, x);

  ip += 4;
}

void IntCode::op_adjust_relative_base() {
  long a = get_param(1);
  relative_base += a;
  ip += 2;
}
