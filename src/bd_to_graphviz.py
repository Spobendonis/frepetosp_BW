# Converts a Branch Decomposition into a Graphviz (DOT) representation
# Usage: python src/bd_to_graphviz.py bd/mini02.gr [-o out.dot]


# --- VIBE CODED USING CLAUDE OPUS 5.5 ---
import argparse
from collections import Counter
from pathlib import Path
import sys
from typing import Dict, List

from graph import BranchDecomposition, BranchDecompositionNode
from input_parser import BranchDecompositionParser

def formatSet(vertices: set[int]) -> str:
	return "{" + ", ".join(map(str, sorted(vertices))) + "}"

def branchDecompositionToDot(bd: BranchDecomposition, name: str = "BranchDecomposition") -> str:
	root = bd.getRoot()

	# Collect nodes in preorder
	nodes: List[BranchDecompositionNode] = []
	stack = [root]
	while stack:
		node = stack.pop()
		nodes.append(node)
		for child in (node.getRight(), node.getLeft()):
			if child is not None:
				stack.append(child)

	# Vertices of the display graph covered by the leaves below each node
	subtreeVertices: Dict[int, Counter[int]] = {}
	for node in reversed(nodes):
		vertices: Counter[int] = Counter(node.getVertexSet())
		for child in (node.getLeft(), node.getRight()):
			if child is not None:
				vertices += subtreeVertices[child.getId()]
		subtreeVertices[node.getId()] = vertices
	total = subtreeVertices[root.getId()]

	lines = [f'graph "{name}" {{', "\tnode [fontname=\"Helvetica\"];", "\tedge [fontname=\"Helvetica\", fontsize=10];"]

	for node in nodes:
		vs = node.getVertexSet()
		if vs:
			lines.append(f'\tn{node.getId()} [shape=box, label="{formatSet(vs)}"];')
		else:
			lines.append(f'\tn{node.getId()} [shape=circle, label="{node.getId()}"];')

	for node in nodes:
		for child in (node.getLeft(), node.getRight()):
			if child is None:
				continue
			# Middle set: vertices appearing both below and outside the child's subtree
			inside = subtreeVertices[child.getId()]
			mid = {v for v, count in inside.items() if count < total[v]}
			lines.append(f'\tn{node.getId()} -- n{child.getId()} [label="{formatSet(mid)}"];')

	lines.append("}")
	return "\n".join(lines) + "\n"

def writeGraphviz(bd: BranchDecomposition, output: Path):
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_text(branchDecompositionToDot(bd, output.stem))

def main():
	argParser = argparse.ArgumentParser(description="Convert a branch decomposition file to Graphviz DOT")
	argParser.add_argument("input", help="Branch decomposition file, e.g. bd/mini02.gr")
	argParser.add_argument("-o", "--output", help="Output .dot file (default: stdout)")
	args = argParser.parse_args()

	bd = BranchDecompositionParser(Path(args.input)).parseInput()

	if args.output is None:
		sys.stdout.write(branchDecompositionToDot(bd, Path(args.input).stem))
	else:
		writeGraphviz(bd, Path(args.output))

if __name__ == "__main__":
	main()
