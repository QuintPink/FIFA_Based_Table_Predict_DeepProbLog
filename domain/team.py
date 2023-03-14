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
        return self.name+self.year
    
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        try:
            if __o.year == self.year and __o.name == self.name:
                return True
            else:
                return False
        except:
            return False


    def toTerm(self) -> Term:
        playerOVRs = []
        for i in range(11):
            playerOVRs.append(Constant(self.players[i].OVR))
        term = Term("team",Constant('"'+self.name+'"'),*playerOVRs)
        return term

    """
    Get team average of 11 best players
    """
    def getTeamAverage(self):
        accumulator = 0.0
        for player in self.players[:11]:
            accumulator += float(player.OVR)
        
        return accumulator / 11
    
    def getTeamOVRs(self) -> list[int]:
        return list(map(lambda player: player.OVR,self.players))
        

if __name__ == "__main__":
    Team()