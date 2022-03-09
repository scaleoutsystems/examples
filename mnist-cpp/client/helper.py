import collections

import fire
import torch
from fedn.utils.pytorchhelper import PytorchHelper
from torch import nn
from torch.nn import functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x.reshape(x.size(0), 784)))
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.fc2(x))
        x = F.log_softmax(self.fc3(x), dim=1)
        return x


def np2pt(np_path, pt_path):
    # Load weights
    helper = PytorchHelper()
    weights_np = helper.load_model(np_path)
    weights = collections.OrderedDict()
    for w in weights_np:
        weights[w] = torch.tensor(weights_np[w])

    # Save model
    model = Net()
    model.load_state_dict(weights)
    model.eval()
    torch.jit.script(model).save(pt_path)


def pt2np(pt_path, np_path):
    # Load weights
    weights = torch.jit.load(pt_path).state_dict()
    weights_np = collections.OrderedDict()
    for w in weights:
        weights_np[w] = weights[w].cpu().detach().numpy()

    # Save
    helper = PytorchHelper()
    helper.save_model(weights_np, np_path)


if __name__ == '__main__':
    fire.Fire()
