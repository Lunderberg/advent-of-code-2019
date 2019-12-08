#ifndef _INTCODE_H_
#define _INTCODE_H_

#include <queue>
#include <vector>

class IntCode {
public:
  IntCode(std::vector<int> initial_memory);

  /// Returns whether the computation is done.
  bool iterate();

  /// Iterate until computation is done
  void iterate_until_done();

  int value_at(int i) const;

  void send_input(int i);
  int get_output();

private:
  int get_param(int i);
  int& at(int i);

  void op_add();
  void op_mul();
  void op_input();
  void op_output();
  void op_jump_if_true();
  void op_jump_if_false();
  void op_lt();
  void op_eq();

  std::vector<int> memory;
  std::queue<int> inputs;
  std::queue<int> outputs;
  int ip;
};

#endif /* _INTCODE_H_ */
