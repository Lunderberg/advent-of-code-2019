#include <iostream>
#include <map>

#include "ReadInputs.hh"

std::map<int,int> count_vals(const std::vector<char>& layer) {
  std::map<int,int> output;
  for(auto val : layer) {
    output[val]++;
  }
  return output;
}

int main(int argc, char** argv){
  if(argc < 2) {
    std::cerr << "Missing argument: puzzle input" << std::endl;
    return 1;
  }

  std::string puzzle_input_file(argv[1]);
  auto text = read_file(puzzle_input_file);

  int width = 25;
  int height = 6;

  std::vector<std::vector<char> > layers;
  int num_layers = text.size() / (width*height);
  for(int i=0; i<num_layers; i++) {
    std::string layer_str = text.substr(i*width*height, width*height);
    std::vector<char> layer;
    for(auto c : layer_str) {
      layer.push_back(c - '0');
    }
    layers.push_back(std::move(layer));
  }


  std::map<int,int> checksum_count{{0,width*height}};
  for(const auto& layer : layers) {
    auto layer_count = count_vals(layer);
    if(layer_count[0] < checksum_count[0]) {
      checksum_count = layer_count;
    }
  }
  std::cout << "Checksum = " << checksum_count[1]*checksum_count[2] << std::endl;

  std::vector<char> running_image(width*height, 2);
  for(const auto& layer : layers) {
    for(int i=0; i<width*height; i++){
      if(running_image[i]==2) {
        running_image[i] = layer[i];
      }
    }
  }

  for(int i=0; i<width*height; i++) {
    std::string to_print = running_image[i] ? "#" : " ";
    std::cout << to_print;
    if((i+1)%width == 0) {
      std::cout << std::endl;
    }
  }
}
