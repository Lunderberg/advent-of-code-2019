#ifndef _READINPUTS_H_
#define _READINPUTS_H_

#include <string>
#include <vector>

std::string read_file(std::string filename);
std::vector<std::string> read_lines(std::string filename);

std::vector<int> read_integers(std::string filename);

#endif /* _READINPUTS_H_ */
