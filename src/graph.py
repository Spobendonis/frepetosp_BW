from __future__ import annotations
from typing import *

class Tree:
	def __init__(self):
		self._root = Node()

	def getRoot(self):
		return self._root

	def printTree(self):
		self.printSubtree(self._root)
		print()

	def printSubtree(self, root: Node):
		if root.getLabel() != "":
			print(root.getLabel(), end="")
		else:
			print("(", end="")
			self.printSubtree(root.getLeft())
			print(",", end="")
			self.printSubtree(root.getRight())
			print(")", end="")

class Node:
	def __init__(self, left: Node = None, right: Node = None, parent: Node = None, label: str = ""):
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

class BranchDecomposition:
	def __init__(self):
		pass