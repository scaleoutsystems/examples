#include <torch/torch.h>

#include "net.h"

int main(int argc, char** argv) {
  // Init model
  std::string out_path;
  std::shared_ptr<Net> net = std::make_shared<Net>();
  if (argc == 3) {
    torch::load(net, argv[1]);  // load from arg 1
    out_path = argv[2];         // save json to arg 2
  } else {
    std::cerr << "Wrong number of arguments" << std::endl;
    exit(1);
  }

  // Parse env
  std::string data_dir = std::getenv("DATA_DIR");

  // Load data
  auto images = torch::data::datasets::MNIST(
                    data_dir, torch::data::datasets::MNIST::Mode::kTest)
                    .map(torch::data::transforms::Stack<>())
                    .dataset()
                    .images();
  auto targets = torch::data::datasets::MNIST(
                     data_dir, torch::data::datasets::MNIST::Mode::kTest)
                     .map(torch::data::transforms::Stack<>())
                     .dataset()
                     .targets();

  // Compute metrics
  auto prediction = net->forward(images);            // forward pass
  auto loss = torch::nll_loss(prediction, targets);  // compute loss
  auto acc = torch::mean((std::get<1>(prediction.max(1)) == targets)
                             .to(torch::kFloat));  // compute acc

  // Print to file
  std::ofstream out(out_path);
  out << "{"
      << "\"loss\": " << loss.item<float>()
      << ", \"acc\": " << acc.item<float>() << "}";
  out.close();
}