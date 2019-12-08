#include "ReadInputs.hh"



// #include <fstream>


// std::vector<int> read_inputs(std::string filename) {
//   std::cout << filename << std::endl;
//   std::ifstream ifile(filename);

//   std::vector<int> output;
//   int value;
//   std::cout << "hi " << output.size() << std::endl;
//   while ( ifile >> value) {
//     std::cout << "hi " << value << std::endl;
//     output.push_back(value);
//   }

//   return output;
// }


#include <cstdlib>
#include <regex>
#include <string>
#include <fstream>
#include <streambuf>
#include <string>

std::vector<int> read_integers(std::string filename) {
  auto contents = read_file(filename);

  std::regex re_integer("-?[0-9]+");
  std::sregex_iterator begin(contents.begin(), contents.end(), re_integer);
  std::sregex_iterator end;

  std::vector<int> output;

  for(auto i = begin; i!=end; i++) {
    std::smatch match = *i;
    int value = atoi(match.str().c_str());
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
