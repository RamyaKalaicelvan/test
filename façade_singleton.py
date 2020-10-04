from abc import ABCMeta, abstractstaticmethod

class Sensor():
	def __init__(self):
		pass
	def sensorOn(self):
		print ("Sensor is on")
	def sensorOff(self):
		print ("Sensor is off")
class Smoke():
	def __init__(self):
		pass
	def smokeOn(self):
		print ("Smoke is on")
	def smokeOff(self):
		print ("Smoke is off")
class Lights():
	def __init__(self):
		pass
	def lightsOn(self):
		print ("Lights is on")
	def lightsOff(self):
		print ("Lights is off")
		
class Meta(type):		
	""" Singleton pattern"""
	_instance = {}
	def __call__(cls,*args,**kwargs):
		""" Creating Object """
		if cls not in cls._instance:
			cls._instance[cls] = super(Meta,cls).__call__(*args,**kwargs)
			return cls._instance[cls]
		
class Facade(metaclass=Meta):
	
	def __init__(self):
		self._sensor = Sensor()
		self._smoke = Smoke()
		self._lights = Lights()
		

	def Emergency(self):
		self._sensor.sensorOn()
		self._smoke.smokeOn()
		self._lights.lightsOn()
	def NoEmergency(self):
		self._sensor.sensorOff()
		self._smoke.smokeOff()
		self._lights.lightsOff()
		
if __name__ == '__main__':
	facade = Facade()
	print ('facade =====',facade)
	facade1 = Facade()
	print ('facade1 ===',facade1)
	sensor = 22
	if sensor > 60:
		facade.Emergency()
	else:
		facade.NoEmergency()
		
