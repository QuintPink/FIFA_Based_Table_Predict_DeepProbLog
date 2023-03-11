from network import FIFA_Net
import torch
from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model
from data import FIFADataset
from deepproblog.evaluate import get_confusion_matrix

network = FIFA_Net()
net = Network(network,"game_result",batching = False)
net.optimizer = torch.optim.Adam(network.parameters(), lr=1e-3)

model = Model("table_predict.pl" , [net])
model.set_engine(ExactEngine(model))


dataset = FIFADataset("training")
test = FIFADataset("test")

# Train the model
loader = DataLoader(dataset,1,True)
train_model(model,loader,1,loss_function_name = "mse",log_iter = 1)
model.save_state("snapshot/trained_model.pth")

# Query
query = dataset.to_query(0)
result = model.solve([query])[0]
print(result)

