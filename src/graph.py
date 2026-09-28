from __future__ import annotations
from typing import Dict, List
from functools import cache

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

		children: List[TreeNode] = []

		right = node.getRight()
		if right is not None:
			children.append(right)

		left = node.getLeft()
		if left is not None:
			children.append(left)

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

	def sPrintSubtree(self, root: TreeNode | None) -> str:
			if root is None:
				return ""
			if root.getLabel() != "":
				return root.getLabel()
			else:
				return f"({self.sPrintSubtree(root.getLeft())},{self.sPrintSubtree(root.getRight())})"


class TreeNode:
	def __init__(self, id: int = -1, left: TreeNode | None = None, right: TreeNode | None = None, parent: TreeNode | None = None, label: str = ""):
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

	def getLeft(self) -> TreeNode | None:
		return self._left

	def getRight(self) -> TreeNode | None:
		return self._right

	def getParent(self) -> TreeNode | None:
		return self._parent

	# Setters
	def setId(self, id):
		if self._id == -1:
			self._id = id
		else:
			raise RuntimeError(f"Tried to update the Id of a vertex which already had an Id: prevId = {self._id}, newId = {id}")

	def setLabel(self, label):
		self._label = label

	def setLeft(self, child: TreeNode | None):
		self._left = child

	def setRight(self, child: TreeNode | None):
		self._right = child

	def setParent(self, parent: TreeNode | None):
		self._parent = parent

class Graph:
	def __init__(self, vertexCount):
		self._vertexCount = vertexCount
		self._edgeCount = 0
		self._vertexMap: Dict[int, List[TreeNode]] = {i: [] for i in range(1, vertexCount+1)}	# Every vertex in the DG maps to the TreeNode it came from in the corresponding tree(s for the leaves)
		self._edges: Dict[int, set[int]] = {i: set() for i in range(1, vertexCount+1)}

	# Getters
	def getVertexMap(self):
		return self._vertexMap

	def getEdges(self):
		return self._edges

	def getEdgesOfVertex(self, v):
		return self._edges[v]

	def getVertexInTrees(self, id: int):
		return self._vertexMap[id]

	# Adders
	def addVertexMapping(self, key: int, value: TreeNode):
		self._vertexMap[key].append(value)

	def addEdge(self, u: int, v: int):
		if v not in self._edges[u]:
			self._edges[u].add(v)
			self._edgeCount += 1

		if u not in self._edges[v]:
			self._edges[v].add(u)
			self._edgeCount += 1

	def removeEdge(self, u: int, v: int):
		if v in self._edges[u]:
			self._edges[u].remove(v)
			self._edgeCount -= 1

		if u in self._edges[v]:
			self._edges[v].remove(u)
			self._edgeCount -= 1

	# Debug
	def printAdjacencyMatrix(self):
		for r in self._edges:
			print(r)

	def printGraph(self):
		print(self.sPrintGraph())

	def sPrintGraph(self):
		witnessed = set()

		res = (f"p tw {self._vertexCount} {self._edgeCount//2}\n")	# tw gaslights the bw implementation that this is a tree width problem
		for u in range(1, self._vertexCount+1):
			for v in self.getEdgesOfVertex(u):
				uId = (u, v) if u < v else (v, u)
				if uId not in witnessed:
					res += f"{u} {v}\n"
					witnessed.add(uId)
		return res

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
				parent = n.getParent()
				if parent is not None:
					dg.addEdge(n.getId(), parent.getId())
			except AttributeError: pass # Expected error, since n.getParent() can be None
			try:
				left = n.getLeft()
				if left is not None:
					dg.addEdge(n.getId(), left.getId())
			except AttributeError: pass # Expected error, since n.getLeft() can be None
			try:
				right = n.getRight()
				if right is not None:
					dg.addEdge(n.getId(), right.getId())
			except AttributeError: pass # Expected error, since n.getRight() can be None

	return dg

class BranchDecomposition:
	def __init__(self, bw: int):
		self.root: BranchDecompositionNode = BranchDecompositionNode(0)
		self.branchwidth = bw

	def getBranchwidth(self):
		return self.branchwidth

	def getRoot(self):
		return self.root

class DPState():
	def __init__(self, x: set, P: set, R: set):
		self._x = x
		self._P = P
		self._R = R

	def __repr__(self):
		return f"DPState(x={self._x}, P={self._P}, R={self._R})"

class BranchDecompositionNode():
	def __init__(self, node_id: int, left: BranchDecompositionNode | None = None, right: BranchDecompositionNode | None = None, vertex_set: set[int] | None = None):
		self.left = left
		self.id = node_id
		self.right = right
		self.parent: BranchDecompositionNode | None = None
		self.states: Dict[DPState, int] = {}
		self._vertexSet: set[int] = vertex_set if vertex_set is not None else set()

	@cache
	def mid(self, other: BranchDecompositionNode) -> set[int]:
		return self.getVertexSet(set([other.id])) & other.getVertexSet(set([self.id]))

	def getVertexSet(self, explored: set[int]) -> set[int]:
		if self._vertexSet:
			return self._vertexSet
		returnedSet = set()
		if self.left is not None and self.left.id not in explored:
			returnedSet.update(self.left.getVertexSet(explored | {self.id}))
		if self.right is not None and self.right.id not in explored:
			returnedSet.update(self.right.getVertexSet(explored | {self.id}))
		if self.parent is not None and self.parent.id not in explored:
			returnedSet.update(self.parent.getVertexSet(explored | {self.id}))
		return returnedSet

