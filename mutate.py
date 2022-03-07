
import sys
import ast
import astor
import random
random.seed(10)

print(sys.argv[1])
print(sys.argv[2])

filename = sys.argv[1]
iterations = int(sys.argv[2])

# negate any single comparison operator
class NegateComparison(ast.NodeTransformer):
        # constructor requires probability value
	def __init__(self, probability):
		self.probability_ = probability

        # handles node input
	def visit_Name(self, node):
        # check if valid node
		newOp = self.negateComp(node)
		if (newOp != False):
			# check probability
			if (random.uniform(0,1) <= self.probability_):
				newNode = node
				node.op = newOp
				# transform node
				return ast.copy_location(newNode, node)

        # validates node and negates comparison
	def negateComp(self, node):
		if (isinstance(node, ast.Eq)):
			return ast.NotEq()
		elif (isinstance(node, ast.NotEq)):
			return ast.Eq()
		elif (isinstance(node, ast.Lt)):
			return ast.GtE()
		elif (isinstance(node, ast.LtE)):
			return ast.Gt()
		elif (isinstance(node, ast.Gt)):
			return ast.LtE()
		elif (isinstance(node, ast.GtE)):
			return ast.NotEq()
		else:
			# else not a valid node
			return False

# swap binary operators + and -, as well as * and /
class SwapBinaryOps(ast.NodeTransformer):
	# constructor requires probability value
	def __init__(self, probability):
			self.probability_ = probability

	# handles node input
	def visit_Name(self, node):
		# call swap
		newOp = self.swap(node)
		if (newOp != False):
			# check probability
			if (random.uniform(0,1) <= self.probability_):
				newNode = node
				node.op = newOp
				# tranform node
				return ast.copy_location(newNode, node)

	# check if node is valid for swap
	def swap(self, node):
		if (isinstance(node, ast.Add)):
			return ast.Sub()
		elif (isinstance(node, ast.Sub)):
			return ast.Add()
		elif (isinstance(node, ast.Mult)):
			return ast.Div()
		elif (isinstance(node, ast.Div)):
			return ast.Mult()
		else:
			return False

# delete assignment functions, jusst ast.Assign
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

# instantiate objects for transformation
negator = NegateComparison(1)
swapper = SwapBinaryOps(1)
deleter = DeleteAssign(0)

i = 0
lastFile = filename

while (i < iterations):

	# opens the file
	with open(lastFile, "r") as source:
		tree = ast.parse(source.read())
		source.close()
	
	# iterate through and transform nodes
	for node in ast.walk(tree):
		negator.visit(node)
		swapper.visit(node)
		deleter.visit(node)

	# write output
	lastFile = str(i) + ".py"
	with open(lastFile, "w") as newfile:
		s = astor.to_source(tree, indent_with=' ' * 4, add_line_information=False, source_generator_class=astor.SourceGenerator)
		newfile.write(s)
		newfile.close()
	
	i += 1
