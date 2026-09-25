import sys

from solver import Solver
from graph import Graph, generateDisplayGraph
from problem_instance import ProblemInstance


from input_parser import RootedInputParser

def main():
	args = sys.argv[1:]
	file = "input/tiny01.nw" if len(args) == 0 else args[0]

	# Get trees from newick files
	parser = RootedInputParser(file)
	trees = parser.parseInput()

	# Generate Display Graph
	dg = generateDisplayGraph(trees)
	dg.printAdjacencyMatrix()
	
	# Generate Branch Decomposition
	bd = 0	# TODO

	instance = ProblemInstance(trees, dg, bd)

	solver = Solver(instance)
	solver.solve()

if __name__ == "__main__":
	main()