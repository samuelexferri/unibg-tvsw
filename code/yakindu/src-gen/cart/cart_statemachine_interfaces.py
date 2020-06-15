"""Interfaces defined in the state chart model.

The interfaces defined in the state chart model are represented
as separate classes.

"""

class SCI_Interface:

	"""Implementation of scope sci_interface.
	"""
	
	def __init__(self):
		self.reset = None
		self.exit = None
		self.order = None
		self.selectgeneric = None
		self.selectcommercial = None
		self.confirm = None
		self.back = None
		self.numofproductsincart = None
		self.totalproducts = None
		self.operationCallback = None
	
	
	
	def raise_reset(self):
		self.reset = True
		
	def raise_exit(self):
		self.exit = True
		
	def raise_order(self):
		self.order = True
		
	def raise_selectgeneric(self):
		self.selectgeneric = True
		
	def raise_selectcommercial(self):
		self.selectcommercial = True
		
	def raise_confirm(self):
		self.confirm = True
		
	def raise_back(self):
		self.back = True
		
	def clear_events(self):
		self.reset = False
		self.exit = False
		self.order = False
		self.selectgeneric = False
		self.selectcommercial = False
		self.confirm = False
		self.back = False
		

