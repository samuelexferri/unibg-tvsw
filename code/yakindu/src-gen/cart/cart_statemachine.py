# Implementation of statechart cart_statemachine.

import warnings
# implemented interfaces:
from .cart_statemachine_interfaces import SCI_Interface
# to store states:
from enum import Enum

class Cart:

	""" State Enum
	"""
	State = Enum('State', '\
	main_region_addorexit,\
	main_region_choosegencom,\
	main_region_selectedgeneric,\
	main_region_selectedcommercial,\
	main_region_closed,\
	null_state')

	"""
	
	Implementation of the state machine 'Cart'.
	
	"""
	
	def __init__(self):
		""" Declares all necessary variables including list of states, histories etc. 
		"""
		self.sci_interface = SCI_Interface()
		self.initialized = False
		self.state_vector = [None] * 1		
		self.next_state_index = None
		# enumeration of all states:
		self.State =  Cart.State
	
	def init(self):
		"""	Initializes the state machine by checking the timer, 
		initializing states and clearing events.
		"""
		self.initialized = True
		for state_index in range(1):
			self.state_vector[state_index] = self.State.null_state
		self._clear_events()
		self.sci_interface.numofproductsincart = 0
		self.sci_interface.totalproducts = 0
	
	def enter(self):
		if self.initialized is not True:
			raise ValueError(
					'The state machine needs to be initialized first by calling the init() function.')
		self.enter_sequence_main_region_default()
	
	def exit(self):
		"""	Exit the the state machine.
		"""
		self.exit_sequence_main_region()
	
	def is_active(self):
		""" @see IStatemachine#is_active()
		"""
		return (self.state_vector[0] is not self.State.null_state)
	
	def is_final(self):
		"""Always returns 'false' since this state machine can never become final.
		@see IStatemachine#is_final()
		"""
		return False
			
	def _clear_events(self):
		""" Resets incoming events (time events included).
		"""
		self.sci_interface.clear_events()
	
	def is_state_active(self, state):
		""" Returns True if the given state is currently active otherwise false.
		"""
		s = state.name
		if s == 'main_region_addorexit':
			return self.state_vector[0] == self.State.main_region_addorexit
		elif s == 'main_region_choosegencom':
			return self.state_vector[0] == self.State.main_region_choosegencom
		elif s == 'main_region_selectedgeneric':
			return self.state_vector[0] == self.State.main_region_selectedgeneric
		elif s == 'main_region_selectedcommercial':
			return self.state_vector[0] == self.State.main_region_selectedcommercial
		elif s == 'main_region_closed':
			return self.state_vector[0] == self.State.main_region_closed
		else:
			return False
	
	def check_main_region__choice_0_tr0_tr0(self):
		return self.sci_interface.numofproductsincart < 2
		
	def effect_main_region__choice_0_tr0(self):
		self.sci_interface.numofproductsincart = self.sci_interface.numofproductsincart+1
		self.enter_sequence_main_region_choosegencom_default()
		
	def effect_main_region__choice_0_tr1(self):
		self.enter_sequence_main_region_closed_default()
		
	def enter_sequence_main_region_addorexit_default(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.main_region_addorexit
		self.state_vector_changed = True
		
	def enter_sequence_main_region_choosegencom_default(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.main_region_choosegencom
		self.state_vector_changed = True
		
	def enter_sequence_main_region_selectedgeneric_default(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.main_region_selectedgeneric
		self.state_vector_changed = True
		
	def enter_sequence_main_region_selectedcommercial_default(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.main_region_selectedcommercial
		self.state_vector_changed = True
		
	def enter_sequence_main_region_closed_default(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.main_region_closed
		self.state_vector_changed = True
		
	def enter_sequence_main_region_default(self):
		self.react_main_region__entry_default()
		
	def exit_sequence_main_region_addorexit(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.null_state
		
	def exit_sequence_main_region_choosegencom(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.null_state
		
	def exit_sequence_main_region_selectedgeneric(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.null_state
		
	def exit_sequence_main_region_selectedcommercial(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.null_state
		
	def exit_sequence_main_region_closed(self):
		self.next_state_index = 0
		self.state_vector[0] = self.State.null_state
		
	def exit_sequence_main_region(self):
		state = self.state_vector[0].name
		if state == 'main_region_addorexit':
			self.exit_sequence_main_region_addorexit()		
		elif state == 'main_region_choosegencom':
			self.exit_sequence_main_region_choosegencom()
		elif state == 'main_region_selectedgeneric':
			self.exit_sequence_main_region_selectedgeneric()
		elif state == 'main_region_selectedcommercial':
			self.exit_sequence_main_region_selectedcommercial()
		elif state == 'main_region_closed':
			self.exit_sequence_main_region_closed()
		
	def react_main_region__choice_0(self):
		if self.check_main_region__choice_0_tr0_tr0():
			self.effect_main_region__choice_0_tr0()
		else:
			self.effect_main_region__choice_0_tr1()
		
	def react_main_region__entry_default(self):
		self.enter_sequence_main_region_addorexit_default()
		
	def react(self):
		return False
	
	
	def main_region_addorexit_react(self,  try_transition):
		did_transition = try_transition
		
		if try_transition:
			if self.sci_interface.exit:
				self.exit_sequence_main_region_addorexit()
				self.enter_sequence_main_region_closed_default()
				self.react()
			elif self.sci_interface.order:
				self.exit_sequence_main_region_addorexit()
				self.react_main_region__choice_0()
			elif self.sci_interface.reset:
				self.exit_sequence_main_region_addorexit()
				self.sci_interface.numofproductsincart = 0
				self.sci_interface.totalproducts = 0
				self.enter_sequence_main_region_addorexit_default()
				self.react()
			else:
				did_transition = False
		
		if did_transition == False:
			did_transition = self.react()
		
		return did_transition
	
	
	def main_region_choosegencom_react(self,  try_transition):
		did_transition = try_transition
		
		if try_transition:
			if self.sci_interface.selectgeneric:
				self.exit_sequence_main_region_choosegencom()
				self.enter_sequence_main_region_selectedgeneric_default()
				self.react()
			elif self.sci_interface.selectcommercial:
				self.exit_sequence_main_region_choosegencom()
				self.enter_sequence_main_region_selectedcommercial_default()
				self.react()
			elif self.sci_interface.back:
				self.exit_sequence_main_region_choosegencom()
				self.sci_interface.numofproductsincart = self.sci_interface.numofproductsincart-1
				self.enter_sequence_main_region_addorexit_default()
				self.react()
			else:
				did_transition = False
		
		if did_transition == False:
			did_transition = self.react()
		
		return did_transition
	
	
	def main_region_selectedgeneric_react(self,  try_transition):
		did_transition = try_transition
		
		if try_transition:
			if self.sci_interface.confirm:
				self.exit_sequence_main_region_selectedgeneric()
				self.sci_interface.totalproducts = self.sci_interface.totalproducts + self.sci_interface.operationCallback.selectGen()
				self.enter_sequence_main_region_addorexit_default()
				self.react()
			elif self.sci_interface.back:
				self.exit_sequence_main_region_selectedgeneric()
				self.enter_sequence_main_region_choosegencom_default()
				self.react()
			else:
				did_transition = False
		
		if did_transition == False:
			did_transition = self.react()
		
		return did_transition
	
	
	def main_region_selectedcommercial_react(self,  try_transition):
		did_transition = try_transition
		
		if try_transition:
			if self.sci_interface.confirm:
				self.exit_sequence_main_region_selectedcommercial()
				self.sci_interface.totalproducts = self.sci_interface.totalproducts + self.sci_interface.operationCallback.selectCom()
				self.enter_sequence_main_region_addorexit_default()
				self.react()
			elif self.sci_interface.back:
				self.exit_sequence_main_region_selectedcommercial()
				self.enter_sequence_main_region_choosegencom_default()
				self.react()
			else:
				did_transition = False
		
		if did_transition == False:
			did_transition = self.react()
		
		return did_transition
	
	
	def main_region_closed_react(self,  try_transition):
		did_transition = try_transition
		
		if try_transition:
			did_transition = False
		
		if did_transition == False:
			did_transition = self.react()
		
		return did_transition
	
	
	def run_cycle(self):
		""" Starts a cycle in the state machine. 
		"""
		if self.initialized is not True:
			raise ValueError(
					'The state machine needs to be initialized first by calling the init() function.')
		self.next_state_index = 0
		while self.next_state_index < len(self.state_vector):
			if self.state_vector[self.next_state_index].name == 'main_region_addorexit' :
				self.main_region_addorexit_react(True)
			elif self.state_vector[self.next_state_index].name == 'main_region_choosegencom' :
				self.main_region_choosegencom_react(True)
			elif self.state_vector[self.next_state_index].name == 'main_region_selectedgeneric' :
				self.main_region_selectedgeneric_react(True)
			elif self.state_vector[self.next_state_index].name == 'main_region_selectedcommercial' :
				self.main_region_selectedcommercial_react(True)
			elif self.state_vector[self.next_state_index].name == 'main_region_closed' :
				self.main_region_closed_react(True)
			self.next_state_index += 1
		self._clear_events()
