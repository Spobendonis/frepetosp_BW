from __future__ import annotations
from typing import *

from graph import Tree, Node, LeafNode, BranchDecomposition

class RootedInputParser:
	def __init__(self, fileName: str):
		self.fileName = fileName

	def Parse(self) -> ProblemInstance:
		parser = InputParser()
		trees = []
		bw = None

		with open(self.fileName, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line[0] != '#':								# Does not start with #
					trees.append(parser.ParseNewick(line))
				else:											# Starts with #
					match line[1]:
						case 'x':
							bw = parser.parseBD(line)
						case _:
							print("IGNORED: ", line)

		if(bw == None):
			raise RuntimeError("No branch decomposition found")

		return ProblemInstance(trees, bw)


class InputParser:
	def ParseNewick(self, newick: str) -> Tree:
		raise NotImplementedError()
		print(newick)
		return Tree()

	def parseBD(self, bd: str) -> BranchDecomposition:
		raise NotImplementedError()
		print(bd)
		return BranchDecomposition()


class ProblemInstance:
	def __init__(self, trees: List[Tree], bd: BranchDecomposition):
		self._trees = trees
		self._bd = bd
