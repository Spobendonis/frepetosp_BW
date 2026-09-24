from __future__ import annotations
from typing import *

from graph import Tree, Node, BranchDecomposition

class RootedInputParser:
	def __init__(self, fileName: str):
		self.fileName = fileName

	def parseInput(self) -> ProblemInstance:
		parser = InputParser()
		trees: List[Tree] = []
		bw = None

		with open(self.fileName, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line[0] != '#':								# Does not start with #
					trees.append(parser.parseNewick(line))
				else:											# Starts with #
					match line[1]:
						case 'x':
							bw = parser.parseBD(line)
						case _:
							print("# IGNORED: ", line)

		if(bw == None):
			raise RuntimeError("No branch decomposition found")

		print()
		for tree in trees:
			tree.printTree()
		return ProblemInstance(trees, bw)


class InputParser:
	def readChar(self, str: str):
		pass

	def parseNewick(self, newick: str) -> Tree:
		tree = Tree()
		cur = tree.getRoot()

		for char in newick:
			match char:
				case '(':	# Creates a left child of Cur, and updates Cur to that child
					l = Node(parent = cur)
					cur.setLeft(l)
					cur = l
				case ')':	# Moves Cur up one level in the tree
					cur = cur.getParent()
				case ',':	# Creates a right sibling to Cur, and updates Cur to that sibling
					cur = cur.getParent()
					r = Node(parent = cur)
					cur.setRight(r)
					cur = r
					pass
				case ';':	# Returns the built tree
					return tree
				case _:		# Assumes any other characters is a label of a leaf
					cur.setLabel(char)
		raise RuntimeError("Missing end character detected")

	def parseBD(self, bd: str) -> BranchDecomposition:
		# raise NotImplementedError()
		print(bd)
		return BranchDecomposition()


class ProblemInstance:
	def __init__(self, trees: List[Tree], bd: BranchDecomposition):
		self._trees = trees
		self._bd = bd

	def getTrees(self):
		return self._trees

	def getBranchDecomposition(self):
		return self._bd
