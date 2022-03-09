#include <torch/torch.h>

#include "net.h"

#define BATCH_SIZE 64
#define N_EPOCHS 10
#define LEARNING_RATE 0.01

int main(int argc, char **argv) {
  // Init model
  std::string out_path;
  std::shared_ptr<Net> net = std::make_shared<Net>();
  if (argc == 3) {              // if 3 args
    torch::load(net, argv[1]);  // load from arg 1
    out_path = argv[2];         // save to arg 2
  } else if (argc == 2) {
    out_path = argv[1];  // save to arg 1, no initial model
  } else {
    std::cerr << "Wrong number of arguments" << std::endl;
    exit(1);
  }

  // Get other params from environment vars
  size_t n_splits = std::stoi(std::getenv("N_SPLITS"));
  size_t split = std::stoi(std::getenv("SPLIT"));
  std::string data_dir = std::getenv("DATA_DIR");

  // Multi-threaded data loader for the MNIST dataset.
  auto data_loader =
      torch::data::make_data_loader(torch::data::datasets::MNIST(data_dir).map(
                                        torch::data::transforms::Stack<>()),
                                    BATCH_SIZE);

  // Init optimizer
  torch::optim::SGD optimizer(net->parameters(), LEARNING_RATE);

  // Train loop
  for (size_t epoch = 1; epoch <= N_EPOCHS; ++epoch) {  // epoch loop
    size_t batch_index = 0;
    for (auto &batch : *data_loader) {  // batch loop
      if (batch_index % n_splits == split) {
        optimizer.zero_grad();                                // reset gradients
        torch::Tensor prediction = net->forward(batch.data);  // forward pass
        torch::Tensor loss =
            torch::nll_loss(prediction, batch.target);  // compute loss
        loss.backward();                                // backprop
        optimizer.step();                               // update params
        // Print logs
        if (batch_index % (100 + split) == 0) {
          std::cerr << "Epoch: " << epoch << " | Batch: " << batch_index
                    << " | Loss: " << loss.item<float>() << std::endl;
        }
      }
      batch_index++;
    }
  }

  // Save
  torch::save(net, out_path);
}