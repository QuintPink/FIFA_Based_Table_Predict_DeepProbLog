from domain.player import Player
from problog.logic import Term, Constant

class Team: 

    def __init__(self, name:str, year:str) -> None:
        self.year : str = year
        self.name : str = name
        self.players : list[Player] = []

    def add_player(self, player : Player):
        self.player = player
        self.players.append(player)
    
    def sort_players(self):
        self.players.sort(reverse=True,key=(lambda p: p.OVR))

    def __str__(self) -> str:
        self.sort_players()
        return str(self.players)
    
    def __repr__(self) -> str:
        return self.__str__()

    def toTerm(self) -> Term:
        playerOVRs = []
        for i in range(11):
            playerOVRs.append(Constant(self.players[i].OVR))
        term = Term("team",Constant('"'+self.name+'"'),*playerOVRs)
        return term

if __name__ == "__main__":
    Team()