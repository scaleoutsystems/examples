#include <torch/torch.h>

#define DROPOUT 0.5
#define BATCH_SIZE 64
#define N_EPOCHS 10

// Define neural network
struct Net : torch::nn::Module {
  torch::nn::Linear fc1{nullptr}, fc2{nullptr}, fc3{nullptr};

  Net() {
    fc1 = register_module("fc1", torch::nn::Linear(784, 64));
    fc2 = register_module("fc2", torch::nn::Linear(64, 32));
    fc3 = register_module("fc3", torch::nn::Linear(32, 10));
  }

  torch::Tensor forward(torch::Tensor x) {
    x = torch::relu(fc1->forward(x.reshape({x.size(0), 784})));
    x = torch::dropout(x, /*p=*/DROPOUT, /*train=*/is_training());
    x = torch::relu(fc2->forward(x));
    x = torch::log_softmax(fc3->forward(x), /*dim=*/1);
    return x;
  }
};

int main(int argc, char** argv) {
  // Init model
  std::shared_ptr<Net> net = std::make_shared<Net>();
  if (argc == 3) {
    torch::load(net, argv[1]);
  } else if (argc > 3 || argc < 2) {
    std::cerr << "Wrong number of arguments" << std::endl;
  }

  // Multi-threaded data loader for the MNIST dataset.
  auto data_loader = torch::data::make_data_loader(
      torch::data::datasets::MNIST("./data").map(
        torch::data::transforms::Stack<>()),
        BATCH_SIZE);

  // Init optimizer
  torch::optim::SGD optimizer(net->parameters(), /*lr=*/0.01);

  // Train loop
  for (size_t epoch = 1; epoch <= N_EPOCHS; ++epoch) { // epoch loop
    size_t batch_index = 0;
    for (auto& batch : *data_loader) { // batch loop
      optimizer.zero_grad(); // reset gradients
      torch::Tensor prediction = net->forward(batch.data); // forward pass
      torch::Tensor loss = torch::nll_loss(prediction, batch.target); // compute loss
      loss.backward(); // backprop
      optimizer.step(); // update params
      if (++batch_index % 100 == 0) { // every 100 baches
        // Print logs
        std::cout << "Epoch: " << epoch << " | Batch: " << batch_index
                  << " | Loss: " << loss.item<float>() << std::endl;
        // Checkpoint model
        torch::save(net, argv[2]);
      }
    }
  }
}