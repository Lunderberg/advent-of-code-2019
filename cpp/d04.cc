#include <algorithm>
#include <iostream>
#include<map>

#include "ReadInputs.hh"

std::vector<int> digits(int x) {
  std::vector<int> output;

  while(x != 0) {
    output.push_back(x%10);
    x /= 10;
  }

  std::reverse(output.begin(), output.end());
  return output;
}

bool is_increasing(int x) {
  int prev_digit = 0;
  for(auto digit : digits(x)) {
    if(digit < prev_digit) {
      return false;
    }
    prev_digit = digit;
  }
  return true;
}

bool has_double(int x) {
  int prev_digit = 0;
  for(auto digit : digits(x)) {
    if(digit == prev_digit) {
      return true;
    }
    prev_digit = digit;
  }
  return false;
}

bool has_double_no_triple(int x) {
  std::map<int,int> counts;
  for(auto digit : digits(x)) {
    counts[digit] += 1;
  }

  for(auto pair : counts) {
    if(pair.second == 2) {
      return true;
    }
  }

  return false;
}

bool is_password_part1(int x) {
  return is_increasing(x) && has_double(x);
}

bool is_password_part2(int x) {
  return is_increasing(x) && has_double_no_triple(x);
}

int main() {
  int min_val = 402328;
  int max_val = 864247;

  int part1 = 0;
  for(int i=min_val; i<=max_val; i++) {
    part1 += is_password_part1(i);
  }
  std::cout << part1 << std::endl;

  int part2 = 0;
  for(int i=min_val; i<=max_val; i++) {
    part2 += is_password_part2(i);
  }
  std::cout << part2 << std::endl;

}
