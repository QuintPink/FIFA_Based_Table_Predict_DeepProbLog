from domain.team import Team
class League:
    def __init__(self,name,year) -> None:
        self.teamRanking : list[Team] = []
        self.name = name
        self.year = year
        self.OK = True

    def addTeam(self,team):
        self.teamRanking.append(team)
    
    def getTeamRank(self,team):
        return self.teamRanking.index(team) + 1

    def getSize(self):
        return len(self.teamRanking)
    
    def getTeamRankingStr(self):
        strr = ""
        rank = 1
        for team in self.teamRanking:
            strr += str(rank)  + ": " + team.name + " // " + str(len(team.players)) + "\n"
            rank += 1
        strr += "_________________________________________"
        return strr

    def __str__(self) -> str:
        return self.name + "|" + self.year + ":\n" + self.getTeamRankingStr()
    
    def __repr__(self) -> str:
        return self.__str__()