from __future__ import annotations
from io import TextIOWrapper
from pathlib import Path
from typing import List
import re

from graph import BranchDecompositionNode, Tree, TreeNode, BranchDecomposition

class NewickParser:
	def __init__(self, path: str):
		self._path = Path(path)
		self._curId = 0

	def initCurId(self, id):
		self._curId = id

	def getCurId(self):
		id = self._curId
		self._curId += 1
		return id

	def parseInput(self) -> List[Tree]:
		trees: List[Tree] = []

		with open(self._path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line[0] != '#':
					trees.append(self.parseNewick(line))
				elif line[1] == 'p':
					try:
						treeCount, leafCount = list(map(int, line[2:].split()))	# We only care about leafCount
						self.initCurId(leafCount+1)								# Reserve the first leafCount ids for the leaves
					except:
						raise RuntimeError(f"Failed to map #p to int: {line}")
				else:
					print("# IGNORED: ", line)

		return trees

	def parseNewick(self, newick: str) -> Tree:
		tree = Tree()

		cur = tree.getRoot()

		label = ""

		for char in newick:
			match char:
				case '(':	# Creates a left child of Cur, and updates Cur to that child
					l = TreeNode(parent = cur)
					assert cur is not None
					cur.setLeft(l)
					cur = l
					tree.addNode(cur)
				case ')':	# Moves Cur up one level in the tree
					if label:	# See case _: for explanation
						assert cur is not None
						cur.setLabel(label)
						cur.setId(int(label))
						tree.addLeaf(cur)
						label = ""

					assert cur is not None
					cur = cur.getParent()
					assert cur is not None
					cur.setId(self.getCurId())
				case ',':	# Creates a right sibling to Cur, and updates Cur to that sibling
					if label:	# See case _: for explanation
						assert cur is not None
						cur.setLabel(label)
						cur.setId(int(label))
						tree.addLeaf(cur)
						label = ""

					cur = cur.getParent()
					r = TreeNode(parent = cur)
					assert cur is not None
					cur.setRight(r)
					cur = r
					tree.addNode(cur)
					pass
				case ';':	# Returns the built tree
					return tree
				case _:		# Assumes any other characters is a label of a leaf
					label += char	# Accumulates the label across multiple reads. Once "," or ")" is hit, the label is done, and written into the leaf before it is updated
		raise RuntimeError("Missing end character detected")

class BranchDecompositionParser():
	def __init__(self, path: Path):
		self._path = path
		self._lines = []
		self._curId = 1

	def getCurId(self):
		id = self._curId
		self._curId += 1
		return id

	def parseInput(self) -> BranchDecomposition:
		bw = -1 #TODO: Get that shit from the output
		bd = BranchDecomposition(bw)
		cur = bd.getRoot()
		with open(self._path, 'r') as f:
			self._lines = f.readlines()
		self.parseBDRec(cur, 0)

		return bd

	# Returns the up-to-date line number that has to be read
	def parseBDRec(self, cur: BranchDecompositionNode, lineNum: int) -> int:
		line = self._lines[lineNum]
		if ":" in line:
			# Internal node
			cur.setLeft(BranchDecompositionNode(self.getCurId()))
			l = cur.getLeft()
			assert l is not None
			currentLine = self.parseBDRec(l, lineNum+1)

			cur.setRight(BranchDecompositionNode(self.getCurId()))
			r = cur.getRight()
			assert r is not None
			return self.parseBDRec(r, currentLine)
		else:
			regex = r"{([\d].*), ([\d].*)}"
			res = re.search(regex, line)
			assert res is not None
			u, v = map(int,res.groups())
			verts: set[int] = set()
			verts.add(u+1) # The Branch decomposition decrements each vertex by 1. Increment to undo this transformation
			verts.add(v+1)
			cur.setVertexSet(verts)
			return lineNum+1