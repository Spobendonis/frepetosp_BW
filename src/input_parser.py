from __future__ import annotations
from typing import *

from graph import Tree, TreeNode

class RootedInputParser:
	def __init__(self, fileName: str):
		self._fileName = fileName
		self._curId = 0

	def initCurId(self, id):
		self._curId = id-1

	def getCurId(self):
		id = self._curId
		self._curId += 1
		return id

	def parseInput(self) -> List[Tree]:
		trees: List[Tree] = []

		with open(self._fileName, 'r') as f:
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

		for t in trees:
			t.printTree()
		
		return trees

	def parseNewick(self, newick: str) -> Tree:
		tree = Tree()

		cur = tree.getRoot()

		label = ""

		for char in newick:
			match char:
				case '(':	# Creates a left child of Cur, and updates Cur to that child
					l = TreeNode(parent = cur)
					cur.setLeft(l)
					cur = l
					tree.addNode(cur)
				case ')':	# Moves Cur up one level in the tree
					if label:	# See case _: for explanation
						cur.setLabel(label)
						cur.setId(int(label)-1)
						label = ""
						
					cur = cur.getParent()
					cur.setId(self.getCurId())
				case ',':	# Creates a right sibling to Cur, and updates Cur to that sibling
					if label:	# See case _: for explanation
						cur.setLabel(label)
						cur.setId(int(label)-1)
						label = ""

					cur = cur.getParent()
					r = TreeNode(parent = cur)
					cur.setRight(r)
					cur = r
					tree.addNode(cur)
					pass
				case ';':	# Returns the built tree
					return tree
				case _:		# Assumes any other characters is a label of a leaf
					label += char	# Accumulates the label across multiple reads. Once "," or ")" is hit, the label is done, and written into the leaf before it is updated
					tree.addLeaf(cur)
		raise RuntimeError("Missing end character detected")