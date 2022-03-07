
import sys
import ast
import astor
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
				# transform node
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
		else:
			# else not a valid node
			return False

# swap binary operators + and -, as well as * and /
class SwapBinaryOps(ast.NodeTransformer):
	# constructor requires probability value
	def __init__(self, probability):
			self.probability_ = probability

	# handles node input
	def visit_Swap(self, node):
		# call swap
		newNode = self.swap(node)
		if (newNode != False):
			# check probability
			if (random.uniform(0,1) <= self.probability_):
				# tranform node
				return ast.copy_location(newNode, node)

	# check if node is valid for swap
	def swap(self, node):
		if (isinstance(node, ast.Add)):
			return ast.Sub
		elif (isinstance(node, ast.Sub)):
			return ast.Add
		elif (isinstance(node, ast.Mult)):
			return ast.Div
		elif (isinstance(node, ast.Div)):
			return ast.Mult
		else:
			return False

class DeleteAssign(ast.NodeTransformer):
	# constructor requires probability value
	def __init__(self, probability):
		self.probability_ = probability

	# handles node input
	def visit_Delete(self, node):
		# call swap
		newNode = self.deleteAssign(node)
		if (newNode != False):
			# check probability
			if (random.uniform(0,1) <= self.probability_):
				# tranform node
				return ast.copy_location(newNode, node)

	def deleteAssign(self, node):
		if (isinstance(node, ast.Assign)):
			return None 
		else:
			return False

with open(filename, "r") as source:
	tree = ast.parse(source.read())
	source.close()

negator = NegateComparison(1)
swapper = SwapBinaryOps(1)
deleter = DeleteAssign(0)

for node in ast.walk(tree):
	negator.visit_Comp(node)
	swapper.visit_Swap(node)
	deleter.visit_Delete(node)

with open("0.py", "w") as newfile:
	s = astor.to_source(tree, indent_with='\t', add_line_information=False, source_generator_class=astor.SourceGenerator)
	newfile.write(s)
	newfile.close()
