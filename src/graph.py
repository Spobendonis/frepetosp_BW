from __future__ import annotations
from typing import *

class Tree:
	def __init__(self):
		self._root = TreeNode()
		self._leaves: List[TreeNode] = []

	def setLeaves(self, leaves):
		self._leaves = leaves

	def getLeaves(self):
		return self._leaves

	def getRoot(self):
		return self._root

	def printTree(self):
		self.printSubtree(self._root)
		print()

	def printSubtree(self, root: TreeNode):
		if root.getLabel() != "":
			print(root.getLabel(), end="")
		else:
			print("(", end="")
			self.printSubtree(root.getLeft())
			print(",", end="")
			self.printSubtree(root.getRight())
			print(")", end="")

	def sPrintTree(self) -> str:
			return f"{self.sPrintSubtree(self._root)};"

	def sPrintSubtree(self, root: TreeNode) -> str:
			if root.getLabel() != "":
				return root.getLabel()
			else:
				return f"({self.sPrintSubtree(root.getLeft())},{self.sPrintSubtree(root.getRight())})"
					

class TreeNode:
	def __init__(self, left: TreeNode = None, right: TreeNode = None, parent: TreeNode = None, label: str = ""):
		self._left = left
		self._right = right
		self._parent = parent
		self._label = label

	def getLabel(self):
		return self._label

	def getLeft(self):
		return self._left

	def getRight(self):
		return self._right

	def getParent(self):
		return self._parent

	def setLabel(self, label):
		self._label = label

	def setLeft(self, child):
		self._left = child

	def setRight(self, child):
		self._right = child

	def setParent(self, parent):
		self._parent = parent

class Graph:
	def __init__(self):
		pass

def generateDisplayGraph(trees: List[Tree]) -> Graph: ...

class BranchDecomposition:
	def __init__(self):
		pass