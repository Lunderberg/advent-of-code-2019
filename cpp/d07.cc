#include <algorithm>
#include <iostream>

#include "IntCode.hh"
#include "ReadInputs.hh"

int test_sequence(const std::vector<int>& memory,
                  const std::vector<int>& seq) {
  std::vector<IntCode> interpreters;

  for(auto val : seq) {
    interpreters.emplace_back(memory);
    auto& interp = interpreters.back();
    interp.send_input(val);
  }

  int signal = 0;
  int i_interp = 0;

  while(true) {
    auto& interp = interpreters.at(i_interp % interpreters.size());
    i_interp++;

    interp.send_input(signal);
    interp.iterate_until_done();
    signal = interp.get_output();

    bool all_done = true;
    for(auto& interp : interpreters) {
      all_done = all_done && interp.is_done();
    }
    if(all_done) {
      break;
    }
  }
  return signal;
}

int main(int argc, char** argv) {
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  auto memory = read_integers(argv[1]);

  // Part a
  {
    std::vector<int> seq{0,1,2,3,4};
    int best_seq_val = 0;
    do{
      int this_seq_val = test_sequence(memory, seq);
      if(this_seq_val > best_seq_val) {
        best_seq_val = this_seq_val;
      }
    } while(std::next_permutation(seq.begin(), seq.end()));
    std::cout << best_seq_val << std::endl;
  }

  // Part b
  {
    std::vector<int> seq{5,6,7,8,9};
    int best_seq_val = 0;
    do{
      int this_seq_val = test_sequence(memory, seq);
      if(this_seq_val > best_seq_val) {
        best_seq_val = this_seq_val;
      }
    } while(std::next_permutation(seq.begin(), seq.end()));
    std::cout << best_seq_val << std::endl;
  }
}
