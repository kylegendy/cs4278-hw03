
import sys
import ast

seed = 0

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
			# update seed and return new node
			print("the old:")
			print(node)
			print("and the new:")
			print(newNode)
			return ast.copy_location(newNode, node)

        # validates node and negates comparison
	def negateComp(self, node):
		if isinstance(node, ast.Compare):
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

		return False

with open(filename, "r") as source:
	tree = ast.parse(source.read())

negator = NegateComparison(0.1)

for node in ast.walk(tree):
	negator.visit(node)


class FuncLister(ast.NodeVisitor):
	def visit_FunctionDef(self, node):
		print(node.name)
		self.generic_visit(node)
