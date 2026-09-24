import sys

from solver import Solver
from graph import Graph, generateDisplayGraph
from problem_instance import ProblemInstance


from input_parser import RootedInputParser

def main():
	args = sys.argv[1:]
	file = "tiny/tiny01.nw" if len(args) == 0 else args[0]

	parser = RootedInputParser(file)
	trees = parser.parseInput()

	dg = generateDisplayGraph(trees)
	bd = 0	# TODO

	instance = ProblemInstance(trees, dg, bd)

	solver = Solver()
	solver.solve()

if __name__ == "__main__":
	main()