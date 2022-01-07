import requests
from os.path import exists as file_exists
import json
import time

## HTTP Request Parameters
PROVISION_ENDPOINT =  'provision/activate'
STACK_ALIAS_ENDPOINT = 'onep:v1/stack/alias'
ACCEPT_HEADER = 'application/x-www-form-urlencoded; charset=utf-8'
CONTENT_TYPE_HEADER = 'application/x-www-form-urlencoded; charset=utf-8'

## Constants
CFG_FILE = "exosite.cfg"
TOKEN_FILE = "token.txt"
NUM_ITER = 1 # Number of times the ExositeSimulator.run() method loops
POLLING_RATE = 60 # In Seconds

DEVICE_ID = "AWESOME TEST"
HOST_URL = "https://a4b2b21bbpf200000.m2.exosite.io/"

class UserDefinitions(object):
	''' Class to manage User input '''
	def __init__(self):
	
		self.device_id = False
		self.host_url = False

		if file_exists(CFG_FILE):
			self.load_cfg()
			
			## Have user enter new parameters 
			if not self.device_id or not self.host_url:
				self.new_cfg()   
		else:
			self.new_cfg()

	def load_cfg(self):
		""" If cfg file exists, check if user wants to re-use Exosite parameters """
		cfg_file = open(CFG_FILE,'r')
		cfg = cfg_file.readline()
		
		## If user enters anything besides y, reset parameters
		use_previous = input("Use Previous Device ID and Connector Endpoint? (y/n): ")
		if use_previous.lower() == "y":

			## Load parameters from existing cfg file
			cfg = json.loads(cfg)
			self.device_id = cfg["device_id"]
			self.host_url = cfg["host_url"]
			print("Device ID: {}".format(self.device_id))
			print("IoT Connector Endpoint: {}".format(self.host_url))

	def new_cfg(self):
		""" Method for getting new Exosite parameters from the User """
		self.device_id = DEVICE_ID   #input("Enter Device ID: ")
		self.host_url = HOST_URL   #input("Enter IoT Connector Endpoint: ")
		cfg_dict = {"device_id":self.device_id,"host_url":self.host_url}
        	
		## Save parameters to local cfg file
		new_cfg_file = open(CFG_FILE,"w")
		new_cfg_file.write(json.dumps(cfg_dict))
		new_cfg_file.close()


class ExositeSimulator(object):

	def __init__(self,device_id,host_url):
		self.device_id = device_id
		self.host_url = host_url
		self.token = ""

		## Check for token, provision if necessary
		self.token_utils()
		print(self.token)
		print(self.device_id)
		print(self.host_url)
		## If token does not exist, exit program
		#if self.token == "":
                #        print("No token available, Stopping Simulator")
                #        return

		## Cheeck for and acknowledge config_io
		#self.config_io_utils()
	
		## Main loop data collection and reporting
		#self.run()

	def load_token(self):
		""" Method to get token from file """
		if file_exists(TOKEN_FILE):
			load_token_file_handler = open(TOKEN_FILE,"r")
			token = load_token_file_handler.read()
			return token
		else:
			## Return empty string if no token exists
			return ""	

	def dump_token(self):
		""" Method to save token to file """
		dump_token_file_handler = open(TOKEN_FILE,"w")
		dump_token_file_handler.write(self.token)
		dump_token_file_handler.close()

	def http_provision(self):
		""" Method to provision a device """
		url = '{0}{1}'.format(self.host_url,PROVISION_ENDPOINT)
		body = 'id={}'.format(self.device_id)
		headers = {
			'Content-Type' : CONTENT_TYPE_HEADER,
			'Content-Length': str(len(body))
		}
		return requests.post(url, headers=headers, data=body)

	def http_read(self,resource):
		""" Method to read from config_io resource """
		url = '{0}{1}?{2}'.format(self.host_url,STACK_ALIAS_ENDPOINT,resource)
		headers = {
                	'Accept' : ACCEPT_HEADER,
                	'X-Exosite-CIK' : self.token
        	}
		return requests.get(url, headers=headers)

	def http_write(self,body):
		""" Method to write to a device dataport. """
		url = '{0}{1}'.format(self.host_url,STACK_ALIAS_ENDPOINT)
		headers = {
			'Content-Type' : CONTENT_TYPE_HEADER,
			'Content-Length' : str(len(body)),
			'X-Exosite-CIK' : self.token
		}
		return requests.post(url, headers=headers, data=body)

	def token_utils(self):
		""" Method to manage token """
		self.token = self.load_token()

		## If there is no token, attempt to provision with Exosite
		if self.token == "":
			resp = self.http_provision()
			if resp.status_code == 200 or resp.status_code == 204:
				self.token = str(resp.text)

				## Save token to file
				self.dump_token()
				print("Successfully provisioned {0} with Exosite with token: {1}".format(self.device_id,self.token))
			else:
				print("failed to provision device with Murano: {0} with code {1}".format(resp.text,resp.status_code))
		else:
			print("Device {0} already provisioned. Using token: {1}".format(self.device_id,self.token))


	def config_io_utils(self):
		""" Method to manage config_io """
		resp = self.http_read('config_io')
		if resp.status_code == 200 or resp.status_code == 204:
			config_io = resp.text
                        
			print("config_io successfully read from Murano")
			if config_io != "" and config_io != "config_io=":

                        	## If config_io exists, write it back to Exosite
                        	resp = self.http_write(config_io)
                        	if resp.status_code == 200 or resp.status_code == 204:
                                	print("config_io successfully written to Murano with code {}".format(resp.status_code))
			else:
				print("config_io not yet defined")
		else:
        		print("Failed to read config_io from Murano: {0} with code {1}".format(resp.text,resp.status_code))

	def run(self):
		""" Main data collection/reporting loop method """
		loop = 1
		while NUM_ITER >= loop:

			## Change code below to customize your own data handling!!
			for i in range(1,11):
				payload = "data_in={}".format(json.dumps({"000": i}))
				resp = self.http_write(payload)
				if resp.status_code == 200 or resp.status_code == 204:
					print("{1} successfully written to Murano with code {0}".format(resp.status_code,payload))
				else:
					print("Failed to write {2} to Murano: {0} with code {1}".format(resp.text,resp.status_code,payload))
				time.sleep(5)	
			loop += 1
			## Change code above to customize your own data handling!!

### MAIN

## Get User Input
user = UserDefinitions()

## Initiate Simulator
ExositeSimulator(user.device_id,user.host_url)

print("Simulator process is complete. Exiting...")

