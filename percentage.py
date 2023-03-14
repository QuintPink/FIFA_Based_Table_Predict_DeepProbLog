import copy
NR_OF_TEAMS = 4

ranking = (0,)*4
def get_outcomes(i):
    if i == NR_OF_TEAMS:
        result = ()
        for x in range(NR_OF_TEAMS):
            result += ((0,x),)
        return [result]
    
    outcomes = get_outcomes(i+1)
    for j in range(NR_OF_TEAMS):
        if j == i:
            continue

        part1 = add_win(outcomes,j)
        part2 = add_win(outcomes,i)
        # part3 = add_draw(outcomes,i,j)
        outcomes = part1 + part2 
    return outcomes

def add_draw(outcomes,j,i):
    outcomes = copy.deepcopy(outcomes)
    for z in range(len(outcomes)):
        outcome = outcomes[z]
        lst = list(outcome)
        i_prev , _ = lst[i]
        lst[i] = (i_prev +1,i)
        j_prev , _ = lst[j]
        lst[j] = (j_prev +1,j)
        outcomes[z] = tuple(lst)
    return outcomes
def add_win(outcomes:list[tuple[int,int]],i):
    outcomes = copy.deepcopy(outcomes)
    for j in range(len(outcomes)):
        outcome = outcomes[j]
        lst = list(outcome)
        i_prev , _ = lst[i]
        lst[i] = (i_prev +3,i)
        outcomes[j] = tuple(lst)
    return outcomes

rankings = get_outcomes(0)
print(len(rankings))

count = 0
other_count = 0
for ranking in rankings:
    if sorted(ranking) == list(ranking):
        count += 1
        x = sorted(ranking)
        if x[0][0] == x[1][0]:
            other_count += 1
print(count)    
print(other_count)  

