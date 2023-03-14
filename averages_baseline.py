from data import FIFADataset
from domain.league import League
from domain.team import Team
import copy



def compareTeamLists(list1 : list[Team],list2: list[Team]) -> bool:
    for i in range(len(list1)):
        team1 = list1[i]
        team2 = list2[i]
        if team1 == team2:
            continue
        else:
            return False
    return True
        

testset  = FIFADataset("all")

prediction_count = 0
correct_count_full = 0
correct_count_nr1 = 0

for i in range(len(testset)):
    league : League = testset.get(i)
    
    teamRanking = league.teamRanking[:4]
    prediction = copy.deepcopy(teamRanking)

    prediction.sort(key= lambda team: team.getTeamAverage(), reverse=True)

    if compareTeamLists(teamRanking,prediction):
        correct_count_full += 1
    if teamRanking[0] == prediction[0]:
        correct_count_nr1 += 1
    prediction_count += 1

accuracy_full = correct_count_full / prediction_count
accuracy_nr1 = correct_count_nr1 / prediction_count

print(f'Full Ranking Accuracy: {accuracy_full}')
print(f'Nr1 Ranking Accuracy: {accuracy_nr1}')
    


