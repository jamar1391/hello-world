import numpy as np

class People:
	def __init__(self,iq,talent,money,success):
		self.iq      = iq
		self.talent  = talent
		self.money   = money
		self.success = success
	
	def money_check(self):
		self.money -= 50

	def talent_check(self):
		x = np.random.randint(1,100)
		if self.iq > 139:
			if x > 20:
				self.money_check()
				self.talent += 1

		elif self.iq > 126:
			if x > 30:
				self.money_check()
				self.talent += 1

		elif self.iq > 113:
			if x > 40:
				self.money_check()
				self.talent += 1

		elif self.iq > 100:
			if x > 50: 
				self.money_check()
				self.talent += 1

		elif self.iq > 87:
			if x > 60:
				self.money_check()
				self.talent += 1


	def luck_test(self):
		luck = np.random.randint(1,100)
		self.money_check()
		
		if luck < 50:
			if self.money < 100:
				self.success -= 1
		
		else:
			self.success += 1
