from network import FIFA_Net
import torch
from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine,ApproximateEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.optimizer import SGD
from deepproblog.train import train_model
from data import FIFADataset,MatchDataset
from deepproblog.evaluate import get_confusion_matrix
from problog.logic import Term
import copy
import statistics

network = FIFA_Net()
net = Network(network,"game_result",batching = False)
net.optimizer = torch.optim.Adam(network.parameters(), lr=1e-3)

model = Model("optim_table_predict.pl" , [net])
model.set_engine(ExactEngine(model))
model.optimizer = SGD(model, 5e-2)

model.load_state("snapshot/trained_modelv3.pth")

implicit_network = model.networks["game_result"].network_module
dataset = MatchDataset().dataset


correct_baseline_count = 0 
correct_count = 0 
count = 0

for example in dataset:
    inpt, result = example
    
    win_prediction = implicit_network.forward(*inpt).detach().numpy()[0]
    int_inpt = list(map(lambda x: int(x),inpt))
    baseline_prediction = statistics.mean(int_inpt[:11]) >= statistics.mean(int_inpt[11:])
    
    if baseline_prediction and result == "win":
        correct_baseline_count += 1
    elif (not baseline_prediction) and result == "loss":
        correct_baseline_count += 1
    
    if result == "win":
        if win_prediction >= 0.5:
            correct_count += 1
    elif result == "loss":
        if win_prediction < 0.5:
            correct_count += 1
    
    count += 1

print("Amount of examples", count)
print("Accuracy:",correct_count/count)
print("Baseline:", correct_baseline_count/count)

