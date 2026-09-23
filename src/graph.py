from __future__ import annotations
from typing import *

class Tree:
	def __init__(self):
		self._root = Node()


class Node:
	def __init__(self, left: Node = None, right: Node = None, parent: Node = None):
		self._left = left
		self._right = right
		self._parent = parent

	def getLabel(self):
		return None

	def setLeft(self, child):
		self._left = child

	def setRight(self, child):
		self._right = child


class LeafNode(Node):
	def __init__(self, left: Node = None, right: Node = None, parent: Node = None, label: str = ""):
		super(left, right, parent)
		self._label = label

	def getLabel(self):
		return self._label


class BranchDecomposition:
	def __init__(self):
		pass