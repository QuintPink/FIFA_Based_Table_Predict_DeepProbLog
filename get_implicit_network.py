from network import FIFA_Net
import torch
from deepproblog.engines import ExactEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.optimizer import SGD

def get_implicit_network():
    network = FIFA_Net()
    net = Network(network,"game_result",batching = False)
    net.optimizer = torch.optim.Adam(network.parameters(), lr=1e-3)

    model = Model("optim_table_predict.pl" , [net])
    model.set_engine(ExactEngine(model))
    model.optimizer = SGD(model, 5e-2)

    model.load_state("snapshot/trained_modelv3.pth")

    implicit_network = model.networks["game_result"].network_module
    return implicit_network

