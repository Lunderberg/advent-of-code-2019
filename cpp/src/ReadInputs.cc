#include "ReadInputs.hh"



#include <cstdlib>
#include <regex>
#include <string>
#include <fstream>
#include <streambuf>
#include <string>

std::vector<long> read_integers(std::string filename) {
  auto contents = read_file(filename);

  std::regex re_integer("-?[0-9]+");
  std::sregex_iterator begin(contents.begin(), contents.end(), re_integer);
  std::sregex_iterator end;

  std::vector<long> output;

  for(auto i = begin; i!=end; i++) {
    std::smatch match = *i;
    long value = atol(match.str().c_str());
    output.push_back(value);
  }

  return output;
}

std::string read_file(std::string filename) {
  std::ifstream ifile(filename);
  auto contents = std::string(std::istreambuf_iterator<char>(ifile),
                              std::istreambuf_iterator<char>());
  return contents;
}

std::vector<std::string> read_lines(std::string filename) {
  std::vector<std::string> output;
  std::string line;

  std::ifstream ifile(filename);
  while(std::getline(ifile, line)) {
    output.push_back(std::move(line));
  }

  return output;
}
