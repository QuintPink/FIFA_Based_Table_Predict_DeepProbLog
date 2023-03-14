import statistics
def test_accuracy(dataset,network):
    correct_baseline_count = 0 
    correct_count = 0 
    count = 0
    for example in dataset:
        inpt, result = example
        
        win_prediction = network.forward(*inpt).detach().numpy()[0]
        int_inpt = list(map(lambda x: int(x),inpt))
        baseline_prediction = statistics.mean(int_inpt[:11]) >= statistics.mean(int_inpt[11:])
        
        if baseline_prediction and result == "win":
            correct_baseline_count += 1
        elif (not baseline_prediction) and result == "loss":
            correct_baseline_count += 1
        
        if result == "win":
            if win_prediction >= 0.5:
                correct_count += 1
        elif result == "loss":
            if win_prediction < 0.5:
                correct_count += 1
        
        count += 1

    print("Accuracy:",correct_count/count)

def baseline_averages_accuracy(dataset):
    correct_baseline_count = 0 
    count = 0
    for example in dataset:
        inpt, result = example
        int_inpt = list(map(lambda x: int(x),inpt))
        baseline_prediction = statistics.mean(int_inpt[:11]) >= statistics.mean(int_inpt[11:])
        
        if baseline_prediction and result == "win":
            correct_baseline_count += 1
        elif (not baseline_prediction) and result == "loss":
            correct_baseline_count += 1        
        count += 1


    print("Baseline Averages:", correct_baseline_count/count)

def baseline_majorityClass_accuracy(dataset):
    count = 0
    count_w = 0
    count_l = 0
    for _ , result in dataset:
        if result == "win":
            count_w +=1
        if result == "loss":
            count_l +=1
        count += 1
    

    print(f'class "win" with accuracy {count_w/count}')
    print(f'class "loss" with accuracy {count_l/count}')