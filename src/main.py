from pathlib import Path
import argparse

from solver import Solver
from graph import Graph, generateDisplayGraph
from problem_instance import ProblemInstance
from branch_decomposition_generator import BranchDecompositionGenerator
from bd_to_graphviz import writeGraphviz


from input_parser import NewickParser

def main():
	argParser = argparse.ArgumentParser()
	argParser.add_argument("input", nargs="?", help="Newick file in input/, e.g. mini02.nw")
	argParser.add_argument("--graphviz", action="store_true", help="Write the branch decomposition as a Graphviz file to graphviz/<name>.dot")
	args = argParser.parse_args()

	file = "input/tiny01.nw" if args.input is None else "input/"+args.input
	bdFile = "bd/tiny01.bw" if args.input is None else "bd/"+args.input.split(".")[0]+".gr"	# Gets file name without extension

	# Get trees from newick files
	parser = NewickParser(file)
	trees = parser.parseInput()

	# Generate Display Graph
	dg = generateDisplayGraph(trees)
	dg.printGraph()
	
	# Generate Branch Decomposition
	bdGen = BranchDecompositionGenerator("lib/bw.jar", bdFile)
	bd = bdGen.generate(dg)

	if args.graphviz:
		writeGraphviz(bd, Path("graphviz") / (Path(bdFile).stem + ".dot"))

	instance = ProblemInstance(trees, dg, bd)

	solver = Solver(instance)
	solver.solve()

if __name__ == "__main__":
	main()