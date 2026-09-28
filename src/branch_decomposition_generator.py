# Uses the Branch Decomposition finder: https://github.com/twalgor/bw/tree/main

import tempfile

from graph import Graph, BranchDecomposition
from input_parser import BranchDecompositionParser

import subprocess
from pathlib import Path

class BranchDecompositionGenerator():
	def __init__(self, bwPath: str, ioFile: str):
		self._jarPath = Path(bwPath)
		self._ioFile = Path(ioFile)

	# Uses a Branchdecomposition found at bd/file if it exists, otherwise saves the created bd as that file
	def generate(self, displayGraph: Graph) -> BranchDecomposition:
		file = Path(self._ioFile)

		if not file.exists():
			input = displayGraph.sPrintGraph()
			_ = self.run_algorithm2(input, file)

		bdParser = BranchDecompositionParser(file)

		return bdParser.parseInput()

	def run_algorithm(self, algorithm_name: str, graph_input: str, output_file: Path=None):
		with tempfile.NamedTemporaryFile(
			mode="w",
			suffix=".txt",
			delete=True,
		) as temp_file:
			temp_file.write(graph_input)
			temp_file.flush()

			command = [
				"java",
				"-cp",
				str(self._jarPath),
				f"bw.{algorithm_name}",
				temp_file.name,
			]

			if output_file is not None:
				command.append(str(output_file))

			return subprocess.run(
				command,
				check=True,
			)

	def run_algorithm1(self, graph_input: str, output_file: Path=None):
		self.run_algorithm("Algorithm1", graph_input, output_file)

	def run_algorithm2(self, graph_input: str, output_file: Path=None):
		self.run_algorithm("Algorithm2", graph_input, output_file)
