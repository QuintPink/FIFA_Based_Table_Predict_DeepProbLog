import torch.nn as nn
import torch
class FIFA_Net(nn.Module):
    def __init__(self) -> None:
        super(FIFA_Net, self).__init__()
        self.hidden1 = nn.Linear(22,10)
        self.act1 = nn.ReLU()
        self.output = nn.Linear(10,2)
        self.act_output = nn.Softmax(-1)
    
    def forward(self,*y):
        x = []
        for i in y:
            x.append(int(i))
        x = torch.tensor(x,dtype=torch.float32)
        x = self.act1(self.hidden1(x))
        x = self.act_output(self.output(x))
        return x 
