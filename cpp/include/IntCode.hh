#ifndef _INTCODE_H_
#define _INTCODE_H_

#include <queue>
#include <vector>

class IntCode {
public:
  IntCode(std::vector<long> initial_memory);

  void iterate();

  /// Iterate until computation is done
  void iterate_until_done();

  long value_at(long i) const;

  void send_input(long i);
  long get_output();

  bool is_done() const { return done; }

private:
  long get_mode(long param);
  long get_param(long param);
  void set_param(long param, long val);
  void set_memory(long i, long val);
  long at(long i);

  void op_add();
  void op_mul();
  void op_input();
  void op_output();
  void op_jump_if_true();
  void op_jump_if_false();
  void op_lt();
  void op_eq();
  void op_adjust_relative_base();

  std::vector<long> memory;
  std::queue<long> inputs;
  std::queue<long> outputs;
  long ip;
  long relative_base;
  bool done;
  bool paused;
};

#endif /* _INTCODE_H_ */
