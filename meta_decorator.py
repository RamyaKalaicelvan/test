# 1. Using Decorators
# 2. create meta class
#

try:
	import datetime
	import os
	import sys
	import logging
except Exception as e:
	print ("Some modules are missing")
	
class Meta(type):
	""" Meta class """
	
	def __call__(self, *args, **kwargs):
		instance = super(Meta,self).__call__(*args,**kwargs)
		return instance
		
	def __init__(self, name, base, attr):
		super(Meta, self).__init__(name,base,attr)
	
class log():
	def __init__(self,func):
		self.func = func
		
	def __call__(self, *args, **kwargs):
		""" Wrapper Function """
		
		start = datetime.datetime.now()
		Tem = self.func(self, *args, **kwargs)
		FunName = self.func.__name__
		end = datetime.datetime.now()
		message = """
			Fuction : {}
			Exe Time: {}
			Address : {}
			Memory  : {} Bytes
			Date : {}
		 """.format(FunName,end-start,self.func.__name__,sys.getsizeof(self.func),start)
		 
		cwd = os.getcwd()
		folder = 'Logs'
		newPath = os.path.join(cwd, folder)
		try:
			os.mkdir(newPath)
		except:
			""" Directory already Exists """
			logging.basicConfig(filename='{}/detaillog.log'.format(newPath),level=logging.DEBUG)
			logging.debug(message)
		return Tem
		
class Test(): # metaclass=Meta
	
	def __init__(self, *args, **kwargs):
		pass
		
	@log
	def methodA(self):
		print ('Hello')
		return '11111'
		
if __name__ == "__main__":
	obj = Test()
	obj.methodA()
		
		
		
