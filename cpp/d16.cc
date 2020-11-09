#include <algorithm>
#include <iostream>
#include <vector>

#include "ReadInputs.hh"

std::vector<char> fft_iter(const std::vector<char>& input) {
  std::vector<char> output;
  output.reserve(input.size());

  for(unsigned int i=0; i<input.size(); i++) {
    int cumsum = 0;
    for(unsigned int j=0; j<input.size(); j++) {
      unsigned int d = (j+1)/(i+1);
      d = (d&1) * (1 - (d&2));
      cumsum += d*input[j];
    }
    output.push_back(std::abs(cumsum%10));
  }

  return output;
}

void part_a(std::vector<char> vals) {
  for(int i=0; i<100; i++) {
    vals = fft_iter(vals);
  }

  for(int i=0; i<8; i++) {
    std::cout << int(vals[i]);
  }
  std::cout << std::endl;
}

void part_b(std::vector<char> vals) {
  int index = (1000000*vals[0] +
                100000*vals[1] +
                 10000*vals[2] +
                  1000*vals[3] +
                   100*vals[4] +
                    10*vals[5] +
                     1*vals[0]);

  std::vector<char> repeated;
  repeated.reserve(10000*vals.size());
  for(int i=0; i<10000; i++) {
    for(auto val : vals) {
      repeated.push_back(val);
    }
  }

  for(int i=0; i<100; i++) {
    std::cout << "Iteration: " << i << std::endl;
    repeated = fft_iter(repeated);
  }

  for(int i=index; i<index+8; i++) {
    std::cout << int(repeated[i]);
  }
  std::cout << std::endl;
}

int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);
  auto text = read_file(puzzle_input_file);
  //text = "03036732577212944063491565474664";

  std::vector<char> vals;
  for(auto c : text) {
    if(c >= '0' && c <= '9') {
      vals.push_back(c - '0');
    }
  }

  part_a(vals);
  //part_b(vals);
}
