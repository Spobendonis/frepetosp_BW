from pathlib import Path
import sys

from solver import Solver
from graph import Graph, generateDisplayGraph
from problem_instance import ProblemInstance
from branch_decomposition_generator import BranchDecompositionGenerator


from input_parser import RootedInputParser

def main():
	args = sys.argv[1:]
	file = "input/tiny01.nw" if len(args) == 0 else "input/"+args[0]
	bdFile = "bd/tiny01.bw" if len(args) == 0 else "bd/"+args[0].split(".")[0]+".gr"	# Gets file name without extension

	# Get trees from newick files
	parser = RootedInputParser(file)
	trees = parser.parseInput()

	# Generate Display Graph
	dg = generateDisplayGraph(trees)
	
	# Generate Branch Decomposition
	bdGen = BranchDecompositionGenerator("lib/bw.jar", bdFile)
	bd = bdGen.generate(dg)

	instance = ProblemInstance(trees, dg, bd)

	solver = Solver(instance)
	solver.solve()

if __name__ == "__main__":
	main()