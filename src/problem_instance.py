from typing import List

from graph import Tree, Graph, BranchDecomposition

class ProblemInstance:
	def __init__(self, trees: List[Tree], dg: Graph, bd: BranchDecomposition):
		self._trees = trees
		self._dg = dg
		self._bd = bd

	def getTrees(self):
		return self._trees

	def getDisplaGraph(self):
		return self._dg

	def getBranchDecomposition(self):
		return self._bd
