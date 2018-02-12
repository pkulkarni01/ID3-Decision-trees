class TreeNode(object):

    def __init__(self):
        self.left = None
        self.right = None
        self.classLabel = -1
        self.attribute = ""
        self.majorityClass = -1

    def add_left(self, obj):
        self.left = obj

    def add_node_attributes(self, n):
        self.attribute = n.attribute
        self.classLabel = n.classLabel
        self.majorityClass = n.majorityClass

    def add_right(self, obj):
        self.right = obj

    def add_attribute(self, attr):
        self.attribute = attr

    def add_class(self, classLabel):
        self.classLabel = classLabel

    def add_majority_class(self, majclass):
        self.majorityClass = majclass

    def isLeaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

