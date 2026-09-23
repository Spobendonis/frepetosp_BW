from input_parser import ProblemInstance

class Solver:
	def __init__(self, problemInstance):
		self._problemInstance = problemInstance

	def solve(self):
		raise NotImplementedError()
		return None