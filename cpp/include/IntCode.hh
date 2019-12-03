#ifndef _INTCODE_H_
#define _INTCODE_H_

#include <vector>

class IntCode {
public:
  IntCode(std::vector<int> initial_memory);

  /// Returns whether the computation is done.
  bool iterate();

  /// Iterate until computation is done
  void iterate_until_done();

  int value_at(int i) const;

private:
  int& at(int i);

  void op_add();
  void op_mul();

  std::vector<int> memory;
  int ip;
};

#endif /* _INTCODE_H_ */
