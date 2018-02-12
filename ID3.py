from treeNode import TreeNode
import math
from random import randint


def entropyFn(df1):
    positiveclass = 0
    negativeclass = 0
    if len(df1.index) == 0:
        return -1
    for index, row in df1.iterrows():
        if row['Class'] == 1:
            positiveclass += 1
        else:
            negativeclass += 1
    positiveprob = positiveclass / len(df1.index)
    negativeprob = negativeclass / len(df1.index)
    entropy = calcEntropy(positiveprob) + calcEntropy(negativeprob)
    return entropy


def varianceimpurityFn(df1):
    positiveclass = 0
    negativeclass = 0
    if len(df1.index) == 0:
        return -1
    for index, row in df1.iterrows():
        if row['Class'] == 1:
            positiveclass += 1
        else:
            negativeclass += 1
    positiveprob = positiveclass / len(df1.index)
    negativeprob = negativeclass / len(df1.index)
    variance_impurity = positiveprob * negativeprob
    return variance_impurity


def calcEntropy(p):
    if p == 0:
        return 0
    else:
        term = -(p * (math.log(p) / math.log(2)))
        return term


def info_gain(entropy, vi, attr_list, df1, heuristic):
    highest_ig = 0
    highest_vi = 0
    for attr in attr_list:
        total_child_entropy = 0
        total_child_impurity = 0
        dfZero = df1[df1[attr] == 0]
        dfOne = df1[df1[attr] == 1]
        zeroEntropy = entropyFn(dfZero)
        oneEntropy = entropyFn(dfOne)
        zeroImpurity = varianceimpurityFn(dfZero)
        oneImpurity = varianceimpurityFn(dfOne)
        total_child_entropy = total_child_entropy + (((len(dfZero.index)) / (len(df1.index))) * zeroEntropy) + (
            ((len(dfOne.index)) / (len(df1.index))) * oneEntropy)
        total_child_impurity = total_child_impurity + (((len(dfZero.index)) / (len(df1.index))) * zeroImpurity) + (
            ((len(dfOne.index)) / (len(df1.index))) * oneImpurity)
        info_gain = entropy - total_child_entropy
        variance_impurity = vi - total_child_impurity
        if highest_ig < info_gain:
            highest_ig = info_gain
            chosen_attribute = attr
        if highest_vi < variance_impurity:
            highest_vi = variance_impurity
            chosen_attribute_vi = attr
    list = []
    if highest_ig == 0 and heuristic == 0:
        list.append(None)
        list.append(None)
        return list
    if highest_vi == 0 and heuristic == 1:
        list.append(None)
        list.append(None)
        return list
    list.append(chosen_attribute)
    list.append(chosen_attribute_vi)
    return list


def count(df1):
    positiveclass = 0
    negativeclass = 0
    for index, row in df1.iterrows():
        if (row['Class'] == 1):
            positiveclass += 1
        else:
            negativeclass += 1
    return [positiveclass, negativeclass]


def traverse_tree(data, root):
    node = root
    while node.isLeaf() is not True:
        chosen_attr = node.attribute
        value = data[chosen_attr]
        if value == 0:
            node = node.left
        else:
            node = node.right
    classLabel = node.classLabel
    return classLabel


def calc_accuracy(root, df1):
    correct_number = 0
    for index, row in df1.iterrows():
        classLabel = traverse_tree(row, root)
        if classLabel == row['Class']:
            correct_number = correct_number + 1
    final_accuracy = (correct_number / len(df1.index)) * 100
    return final_accuracy


node_list = []


def copy_tree(root):
    newRoot = TreeNode()
    newRoot.add_node_attributes(root)
    if root is None:
        return None
    if root.left is not None:
        newRoot.add_left(copy_tree(root.left))
    if root.right is not None:
        newRoot.add_right(copy_tree(root.right))
    node_list.append(newRoot)
    return newRoot


def get_non_leaf_nodes(list):
    non_leaf_List = []
    for node in list:
        if not node.isLeaf():
            non_leaf_List.append(node)
    return non_leaf_List


def build_decison_tree(attr_list, df1, heuristic):
    treeRoot = TreeNode()
    countsPN = count(df1)
    if countsPN[0] > countsPN[1]:
        treeRoot.add_majority_class(1)
    else:
        treeRoot.add_majority_class(0)
    if countsPN[0] == len(df1.index):
        treeRoot.classLabel = 1
    elif countsPN[1] == len(df1.index):
        treeRoot.classLabel = 0
    elif len(attr_list) == 0:
        if countsPN[0] > countsPN[1]:
            treeRoot.classLabel = 1
        else:
            treeRoot.classLabel = 0
    else:
        entropy = entropyFn(df1)
        variance_impurity = varianceimpurityFn(df1)
        chosen_attr_list = info_gain(entropy, variance_impurity, attr_list, df1, heuristic)
        chosen_attr = chosen_attr_list[heuristic]
        if chosen_attr is not None:
            treeRoot.add_attribute(chosen_attr)
            new_attr_list = []
            for attr in attr_list:
                if attr != chosen_attr:
                    new_attr_list.append(attr)
            attr_list = new_attr_list
            for i in range(2):
                df2 = df1[df1[chosen_attr] == i]
                if len(df2.index) != 0:
                    if i == 0:
                        treeRoot.add_left(build_decison_tree(attr_list, df2, heuristic))
                    else:
                        treeRoot.add_right(build_decison_tree(attr_list, df2, heuristic))
                else:
                    treeChild = TreeNode()
                    if countsPN[0] > countsPN[1]:
                        treeChild.classLabel = 1
                    else:
                        treeChild.classLabel = 0
                    if i == 0:
                        treeRoot.add_left(treeChild)
                    else:
                        treeRoot.add_right(treeChild)
        else:
            if countsPN[0] > countsPN[1]:
                treeRoot.classLabel = 1
            else:
                treeRoot.classLabel = 0
    return treeRoot


def prune_tree(l, k, treeRoot, validation_data, validation_accuracy):
    bestroot = treeRoot
    for i in range(l):
        copiedRoot = copy_tree(treeRoot)
        m = randint(1, k)
        for j in range(m):
            non_leaf_list = get_non_leaf_nodes(node_list)
            p = randint(0, len(non_leaf_list))
            prun_node = non_leaf_list[p]
            majority_class = prun_node.majorityClass
            prun_node.add_class(majority_class)
            prun_node.add_left(None)
            prun_node.add_right(None)
        new_accuracy = calc_accuracy(copiedRoot, validation_data)
        if new_accuracy > validation_accuracy:
            bestroot = copiedRoot
    return bestroot
