import sys
import pandas as pd
from ID3 import build_decison_tree
from ID3 import prune_tree
from ID3 import calc_accuracy


def print_tree(root, s):
    if root is not None:
        if root.isLeaf():
            sys.stdout.write(":" + str(root.classLabel))
            print()
        else:
            print()
            sys.stdout.write(s + root.attribute + "= 0")
            print_tree(root.left, s + " |")
            sys.stdout.write(s + root.attribute + "= 1")
            print_tree(root.right, s + " |")


def print_output(root, training, validation, test):
    accuracy = calc_accuracy(root, training)
    print("Training set accuracy is", str(accuracy) + "%")
    val_accuracy = calc_accuracy(root, validation)
    print("Validation set accuracy is", str(val_accuracy) + "%")
    test_accuracy =calc_accuracy(root, test)
    print("Pre-pruned test data accuracy is", str(test_accuracy) + "%")

l = int(sys.argv[1])
k = int(sys.argv[2])
training_data = pd.read_csv(sys.argv[3])
validation_data = pd.read_csv(sys.argv[4])
test_data = pd.read_csv(sys.argv[5])
to_print = sys.argv[6]
dfAttr = training_data.iloc[:, :-1]
attr_list = list(dfAttr)
treeRoot = build_decison_tree(attr_list, training_data, 0)
print("pre-pruning tree with information gain heuristic")
if to_print == "yes":
   print_tree(treeRoot, "")
print_output(treeRoot, training_data, validation_data, test_data)
val_accuracy = calc_accuracy(treeRoot, validation_data)
prunedRoot = prune_tree(l, k, treeRoot, validation_data, val_accuracy)
test_accuracy = calc_accuracy(prunedRoot, test_data )
print("Post pruned test data accuracy with information gain heuristic", str(test_accuracy) + "%")
treeRoot1 = build_decison_tree(attr_list, training_data, 1)
print("--------------------------------------------------")
print("pre-pruning tree with variance impurity heuristic")
if to_print == "yes":
   print_tree(treeRoot1, "")
print_output(treeRoot1, training_data, validation_data, test_data)
val_accuracy = calc_accuracy(treeRoot1, validation_data)
prunedRoot1 = prune_tree(l, k, treeRoot1, validation_data, val_accuracy)
test_accuracy1 = calc_accuracy(prunedRoot1, test_data )
print("Post pruned test data accuracy with variance impurity heuristic", str(test_accuracy1) + "%")
