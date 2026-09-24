from input_parser import ProblemInstance

class Solver:
	def __init__(self, problemInstance: ProblemInstance):
		self._problemInstance = problemInstance
		self._trees = problemInstance.getTrees()
		self._bd = problemInstance.getBranchDecomposition()

	def solve(self):
		# raise NotImplementedError()
		return None