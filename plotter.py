from matplotlib import pyplot

iterations = [0,400,800,1200,1600,x]

test_acc = [0.020833,0.09375,0.09375,0.114583,0.104166]
train_acc = [0.052356,0.115183,0.109947, 0.115183,0.1256544]

pyplot.plot(iterations,test_acc, label="test accuracy")

pyplot.plot(iterations,train_acc,linestyle="dashed", label="train accuracy")
pyplot.legend(loc="upper left")
pyplot.savefig("accuracy_evolution.pdf")
pyplot.show()