import cellaserv.proxy

import mraa

from cellaserv.service import Service
from time import sleep

@Service.require("ax", "1")
class actuators(Service):

	def __init__(self, act):
		super().__init__(identification=str(act))
		self.robot = cellaserv.proxy.CellaservProxy()
		self.minimal_delay = 2
		for n in [1,2,3,4,5]:
			self.robot.ax[str(n)].mode_joint()
		self.relais = mraa.Gpio(13)
		self.relais.dir(mraa.DIR_OUT)
		print("Actuators : Init Done")

	@Service.action
	def open_door(self):
		self.robot.ax["1"].move(goal = 700)
		self.robot.ax["2"].move(goal = 200)

	@Service.action
	def close_door(self):
		self.robot.ax["1"].move(goal = 200)
		self.robot.ax["2"].move(goal = 700)

	@Service.action
	def half_close_door(self):
		self.robot.ax["1"].move(goal = 400)
		self.robot.ax["2"].move(goal = 500)

	@Service.action
	def open_umbrella(self):
		self.robot.ax["3"].move(goal = 1000)

	@Service.action
	def close_umbrella(self):
		self.robot.ax["3"].move(goal = 500)

	@Service.action
	def open_arm_left(self):
		self.robot.ax["4"].move(goal = 400)
		sleep(self.minimal_delay)
		self.robot.ax["5"].move(goal = 800)
		sleep(self.minimal_delay)
		self.robot.ax["4"].move(goal = 800)

	@Service.action
	def open_arm_right(self):
		self.robot.ax["4"].move(goal = 270)
		sleep(self.minimal_delay)
		self.robot.ax["5"].move(goal = 820)
		sleep(self.minimal_delay)
		self.robot.ax["5"].move(goal = 800)

	@Service.action
	def half_open_arm(self):
		self.robot.ax["5"].move(goal = 700)

	@Service.action
	def close_arm(self):
		self.robot.ax["4"].move(goal = 270)
		sleep(self.minimal_delay)
		self.robot.ax["5"].move(goal = 350)

	@Service.action
	def activate_ea(self):
		self.relais.write(1)

	@Service.action
	def disable_ea(self):
		self.relais.write(0)

def main():
	actuators_pal = actuators("pal")
	Service.loop()

if __name__ == "__main__":
	main()
