from __future__ import annotations
from typing import *

from graph import Tree, TreeNode

class RootedInputParser:
	def __init__(self, fileName: str):
		self.fileName = fileName

	def parseInput(self) -> List[Tree]:
		trees: List[Tree] = []

		with open(self.fileName, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line[0] != '#':
					trees.append(self.parseNewick(line))
				else:
					print("# IGNORED: ", line)

		print()
		for tree in trees:
			tree.printTree()
		
		return trees

	def parseNewick(newick: str) -> Tree:
		tree = Tree()
		leaves: List[TreeNode] = []

		cur = tree.getRoot()

		for char in newick:
			match char:
				case '(':	# Creates a left child of Cur, and updates Cur to that child
					l = TreeNode(parent = cur)
					cur.setLeft(l)
					cur = l
				case ')':	# Moves Cur up one level in the tree
					cur = cur.getParent()
				case ',':	# Creates a right sibling to Cur, and updates Cur to that sibling
					cur = cur.getParent()
					r = TreeNode(parent = cur)
					cur.setRight(r)
					cur = r
					pass
				case ';':	# Returns the built tree
					tree.setLeaves(leaves)
					return tree
				case _:		# Assumes any other characters is a label of a leaf
					cur.setLabel(char)
					leaves.append(cur)
		raise RuntimeError("Missing end character detected")