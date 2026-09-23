from solver import Solver
import sys


from input_parser import RootedInputParser

def main():
	args = sys.argv[1:]
	file = "tiny/tiny01.nw" if len(args) == 0 else args[0]

	parser = RootedInputParser(file)
	problemInstance = parser.Parse()
	solver = Solver(problemInstance)
	solver.solve()

if __name__ == "__main__":
	main()