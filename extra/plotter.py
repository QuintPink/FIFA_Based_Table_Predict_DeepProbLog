from matplotlib import pyplot

iterations = [0,400,800,1200,1600,1920]

test_acc = [0.020833,0.09375,0.09375,0.114583,0.104166,0.09375]
train_acc = [0.052356,0.115183,0.109947, 0.115183,0.1256544,0.11518324607329843]
averages_baseline = [0.212543554]*6
random_guessing_baseline = [0.0416666]*6

pyplot.plot(iterations,test_acc, label="test accuracy")
pyplot.plot(iterations,train_acc,linestyle="dashed", label="train accuracy")
pyplot.plot(iterations,averages_baseline, label="averages method")
pyplot.plot(iterations,random_guessing_baseline, label="random guessing")

pyplot.xlabel("Amount of iterations (10 Epochs of 192 iterations)")
pyplot.ylabel("Accuracy")
pyplot.legend(loc="upper right")
pyplot.savefig("accuracy_evolution.pdf")
pyplot.show()