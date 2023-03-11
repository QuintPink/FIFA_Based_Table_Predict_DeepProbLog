from domain.team import Team
from deepproblog.query import Query
from problog.logic import Term, Constant, list2term
import random
import copy
class League:
    def __init__(self,name,year) -> None:
        self.teamRanking : list[Team] = []
        self.name = name
        self.year = year
        self.OK = True

    """
    Assumption that you add the teams from highest ranking team to lowest ranking team
    """
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

    def to_query(self) -> Query:
        ranked_teamTerms = []
        for team in self.teamRanking:
            ranked_teamTerms.append(team.toTerm())
        teamTerms = copy.deepcopy(ranked_teamTerms)
        random.shuffle(teamTerms)
        return Query(Term("predict_table",list2term(teamTerms),list2term(ranked_teamTerms)))
