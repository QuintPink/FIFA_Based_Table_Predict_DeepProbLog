from player import Player


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

if __name__ == "__main__":
    pass