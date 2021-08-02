def main1():
    import jittor as jt
    from jittor import Module
    from jittor import nn
    import numpy as np

    class Model(Module):
        def __init__(self):
            self.layer1 = nn.Linear(1, 10)
            self.relu = nn.Relu()
            self.layer2 = nn.Linear(10, 1)

        def execute(self, x):
            x = self.layer1(x)
            x = self.relu(x)
            x = self.layer2(x)
            return x

    model = Model()

    from jittorvis import server
    input = jt.float32(np.random.rand(10, 1))
    server.visualize(input, model, host='0.0.0.0', port=5008)
    # JittorVis start.
    # server.stop()
    # JittorVis stop.

def main2():
    from jittorvis import server
    server.run('test.pkl', host='0.0.0.0', port=5010)
    # JittorVis start.
    # server.stop()
    # JittorVis stop.

def test_pytorch():
    from jittorvis.__get_pytorch_info import graph
    import torch
    import torchvision
    dummy_input = torch.Tensor(1, 3, 224, 224)
    model = torchvision.models.alexnet()
    return graph(model, (dummy_input,))


def main3():
    data = test_pytorch()
    from jittorvis import server
    server.run_server(data, host='0.0.0.0', port=5009)


if __name__ == '__main__':
    main3()
