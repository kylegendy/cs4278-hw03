
import sys
import ast
import random
random.seed(10)

filename = "fuzzywuzzy.py"

# negate any single comparison operator
class NegateComparison(ast.NodeTransformer):
        # constructor requires probability value
	def __init__(self, probability):
		self.probability_ = probability

        # handles node input
	def visit_Comp(self, node):
        # check if valid node
		newNode = self.negateComp(node)
		if (newNode != False):
			# check probability
			if (random.uniform(0,1) <= self.probability_):
				# update seed and return new node
				return ast.copy_location(newNode, node)

        # validates node and negates comparison
	def negateComp(self, node):
		if (isinstance(node, ast.Eq)):
			return ast.NotEq
		elif (isinstance(node, ast.NotEq)):
			return ast.Eq
		elif (isinstance(node, ast.Lt)):
			return ast.GtE
		elif (isinstance(node, ast.LtE)):
			return ast.Gt
		elif (isinstance(node, ast.Gt)):
			return ast.LtE
		elif (isinstance(node, ast.GtE)):
			return ast.NotEq
		# else not a valid node
		return False

# swap binary operators + and -, as well as * and /
# class SwapBinaryOps(ast.NodeTransformer):
# 	# constructor requires probability value
# 	def __init__(self, probability):
# 			self.probability_ = probability

# 	# handles node input
# 	def visit_Swap(self, node):
# 			if (self.isSwappable(node)):


# 	# check if node is valid for swap
# 	def swap(self, node):
# 		if (isinstance(node, ast.Add))

with open(filename, "r") as source:
	tree = ast.parse(source.read())

negator = NegateComparison(0.1)

for node in ast.walk(tree):
	if (node.op == ast.Sub or node.op == ast.Add):
		print(ast.dump(node))


class FuncLister(ast.NodeVisitor):
	def visit_FunctionDef(self, node):
		print(node.name)
		self.generic_visit(node)
