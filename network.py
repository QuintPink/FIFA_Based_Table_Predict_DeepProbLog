import torch.nn as nn
class FIFA_Net(nn.Module):
    def __init__(self) -> None:
        super(FIFA_Net, self).__init__()
        self.hidden1 = nn.Linear(22,10)
        self.act1 = nn.ReLU()
        self.hidden2 = nn.Linear(10,10)
        self.act2 = nn.ReLU()
        self.output = nn.Linear(10,3)
        self.act_output = nn.Softmax(1)
    
    def forward(self,x):
        x = self.act1(self.hidden1(x))
        x = self.act2(self.hidden2(x))
        x = self.act_output(self.output(x))
        return x
