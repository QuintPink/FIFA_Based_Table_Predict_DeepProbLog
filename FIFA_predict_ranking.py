from network import FIFA_Net
import torch
from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine,ApproximateEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.optimizer import SGD
from deepproblog.train import train_model
from data import FIFADataset
from deepproblog.evaluate import get_confusion_matrix

network = FIFA_Net()
net = Network(network,"game_result",batching = False)
net.optimizer = torch.optim.Adam(network.parameters(), lr=1e-3)

# model = Model("table_predict.pl" , [net])
model = Model("optim_table_predict.pl" , [net])
model.set_engine(ExactEngine(model))
model.optimizer = SGD(model, 5e-2)
dataset = FIFADataset("training")
testset = FIFADataset("test")

# Train the model
loader = DataLoader(dataset,1,True)
train = train_model(model,loader,10,log_iter = 10)
    # test=lambda x: [
    #     ("Accuracy Train Set", get_confusion_matrix(model, dataset).accuracy()),
    #     ("Accuracy Test Set", get_confusion_matrix(model, testset).accuracy())
    # ])

model.save_state("snapshot/trained_modelv3.pth") #V1 = 22-20-2, V2 = 22-10-10-2, #V3 = 22-10-2

print("Accuracy Test Set", get_confusion_matrix(model, testset).accuracy())
print("Accuracy Train Set", get_confusion_matrix(model, dataset).accuracy())
# Query
query = dataset.to_query(0)
result = model.solve([query])[0]
print(result)
print("---")
# query = query.variable_output()
# result = model.solve([query])[0]
# print(result)

