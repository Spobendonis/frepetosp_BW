from __future__ import annotations
from typing import *

class Tree:
	def __init__(self):
		self._root = TreeNode()
		self._leaves: List[TreeNode] = []
		self._nodes: List[TreeNode] = [self._root]

	# Getters
	def getRoot(self):
		return self._root
	
	def getLeaves(self):
		return self._leaves

	def getNodes(self):
		return self._nodes

	def getNumLeaves(self):
		return len(self._leaves)

	def getNumNodes(self):
		return len(self._nodes)

	# Adders
	def addLeaf(self, leaf: TreeNode):
		self._leaves.append(leaf)

	def addNode(self, node: TreeNode):
		self._nodes.append(node)

	# Setters
	def setLeaves(self, leaves: List[TreeNode]):
		self._leaves = leaves

	# Debug
	def printTree(self):
		self.printSubtree(self._root, "", True, True)

	def printSubtree(self, node: TreeNode, prefix: str, is_last: bool, is_root: bool):
		node_id = node.getId()
		label = node.getLabel()

		# Print the node
		if is_root:
			connector = ""
		else:
			connector = "└── " if is_last else "├── "

		if label != "":
			print(f'{prefix}{connector}{node_id} : "{label}"')
		else:
			print(f'{prefix}{connector}{node_id}')

		children = []

		if node.getRight() is not None:
			children.append(node.getRight())

		if node.getLeft() is not None:
			children.append(node.getLeft())

		# Print children recursively
		for i, child in enumerate(children):
			child_is_last = (i == len(children) - 1)

			if is_root:
				child_prefix = ""
			else:
				child_prefix = prefix + ("    " if is_last else "│   ")

			self.printSubtree(
				child,
				child_prefix,
				child_is_last,
				False
			)

	def sPrintTree(self) -> str:
			return f"{self.sPrintSubtree(self._root)};"

	def sPrintSubtree(self, root: TreeNode) -> str:
			if root.getLabel() != "":
				return root.getLabel()
			else:
				return f"({self.sPrintSubtree(root.getLeft())},{self.sPrintSubtree(root.getRight())})"
					

class TreeNode:
	def __init__(self, id: int = -1, left: TreeNode = None, right: TreeNode = None, parent: TreeNode = None, label: str = ""):
		self._id = id
		self._left = left
		self._right = right
		self._parent = parent
		self._label = label

	# Getters
	def getId(self):
		return self._id

	def getLabel(self):
		return self._label

	def getLeft(self):
		return self._left

	def getRight(self):
		return self._right

	def getParent(self):
		return self._parent

	# Setters
	def setId(self, id):
		if self._id == -1:
			self._id = id
		else:
			raise RuntimeError(f"Tried to update the Id of a vertex which already had an Id: prevId = {self._id}, newId = {id}")

	def setLabel(self, label):
		self._label = label

	def setLeft(self, child):
		self._left = child

	def setRight(self, child):
		self._right = child

	def setParent(self, parent):
		self._parent = parent

class Graph:
	def __init__(self, vertexCount):
		self._vertexMap: Dict[int, List[TreeNode]] = {}	# Every vertex in the DG maps to the TreeNode it came from in the corresponding tree(s for the leaves)
		self._edges = [[0 for _ in range(vertexCount)] for _ in range(vertexCount)]

	# Getters
	def getVertexMap(self):
		return self._vertexMap

	def getEdges(self):
		return self._edges

	def getVertexInTrees(self, id: int):
		return self._vertexMap[id]

	# Adders
	def addVertexMapping(self, key: int, value: TreeNode):
		if key in self._vertexMap:
			self._vertexMap[key].append(value)
		else:
			self._vertexMap[key] = [value]
 
	def addEdge(self, u: int, v: int):
		self._edges[u][v] = 1
		self._edges[v][u] = 1

	def removeEdge(self, u: int, v: int):
		self._edges[u][v] = 0
		self._edges[v][u] = 0

	# Debug
	def printAdjacencyMatrix(self):
		for r in self._edges:
			print(r)

def generateDisplayGraph(trees: List[Tree]) -> Graph:
	# Can technically be changed to: trees[0].getNumNodes + ((len(trees)-1) * (trees[0].getNumNodes - trees[0].getNumLeaves)) // but that is less descriptive imo
	numNodes = trees[0].getNumLeaves()	# Only count the number of leaves once, since they are shared in the DG for all trees
	for t in trees:
		numNodes += (t.getNumNodes() - t.getNumLeaves())

	dg = Graph(numNodes)

	for t in trees:
		# Adds all the edges in the trees to the display graph
		for n in t.getNodes():	# TODO: This is ugly, and (unnecassarily) adds each edge twice (since the add/remove edge already adds it twice). Probably make good
			dg.addVertexMapping(n.getId(), n)
			try:
				dg.addEdge(n.getId(), n.getParent().getId())
			except AttributeError: pass # Expected error, since n.getParent() can be None
			try:
				dg.addEdge(n.getId(), n.getLeft().getId())
			except AttributeError: pass # Expected error, since n.getLeft() can be None
			try:
				dg.addEdge(n.getId(), n.getRight().getId())
			except AttributeError: pass # Expected error, since n.getRight() can be None

	return dg

class BranchDecomposition:
	def __init__(self):
		pass