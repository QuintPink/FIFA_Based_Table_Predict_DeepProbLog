
from explicit.network import FIFA_Net
import random
from torch import optim
import torch
from explicit.test_outcome_net import test_accuracy, baseline_averages_accuracy, baseline_majorityClass_accuracy
from data import MatchDataset
from get_implicit_network import get_implicit_network

"""
Run by running python file run_explicit.py
"""
def run():
    dataset = MatchDataset()
    dataset.shuffle()
    dataset.balance()
    dataset = dataset.dataset

    third = len(dataset) // 3

    test_set = dataset[:third]
    train_set = dataset[third:]
    print("Train set size",len(train_set))
    print("Test set size",len(test_set))

    net = FIFA_Net()
    optimizer = optim.Adam(net.parameters(),lr= 1e-6)
    criterion : torch.nn.CrossEntropyLoss = torch.nn.CrossEntropyLoss()

    test_iter = 500
    count_iter = 1
    for epoch in range(1):
        
        print("Epoch",epoch+1)
        for example in test_set:
            print("Iteration:",count_iter)
            optimizer.zero_grad()
            if count_iter % test_iter== 0:
                net.eval()
                with torch.no_grad():
                    test_accuracy(test_set,net)
                    test_accuracy(train_set,net)
                net.train()
            inpt, result = example
            if result == "win":
                target = 1.0
            else:
                target = 0.0
            target = torch.tensor([target,abs(target-1.0)])
            output = net(*inpt)
            loss = criterion(output,target)
            # print("Loss: ",loss)
            loss.backward()
            optimizer.step()
            count_iter +=1

    torch.save(net.state_dict(),"snapshot/explicit_outcome_net.pth")

    print("Explicitly trained ",end="")
    test_accuracy(test_set,net)
    print("Implicitly trained ",end="")
    test_accuracy(test_set,get_implicit_network())
    baseline_averages_accuracy(test_set)
    baseline_majorityClass_accuracy(test_set)

if __name__ == "__main__":
    run()