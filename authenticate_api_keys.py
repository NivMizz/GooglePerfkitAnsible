import subprocess
import yaml
import argparse
import datetime
import re
import os
import sys

class api_key_reader():

	def __init__(self):
		self.config = self.import_yaml()

	def import_yaml(self):
		my_path = os.path.abspath(os.path.dirname(__file__))
		path = os.path.join(my_path, 'passwords/keys.yml')
		print(path)
		with open(path, 'r') as stream:
			try:
				return yaml.load(stream)
			except yaml.YAMLError as exc:
				print(exc)

	def runAuthCommands(self):
		#Digital Ocean configure
		try:
			if self.config['digital_ocean_key'] is None: # The variable
				print('The digital ocean key is empty skipping')
			else:
				command = 'doctl auth init -t ' + self.config['digital_ocean_key']
				result = subprocess.call(command, shell=True)
		except NameError:
			print ("There was an error in getting the keys for digital ocean..")

		#AWS configure
		try:
			if self.config['aws_keys']['aws_access_key_id'] is None: # The variable
				print('The aws key is empty skipping')
			else:
				command_one = 'aws configure set aws_access_key_id ' + self.config['aws_keys']['aws_access_key_id']
				command_two = 'aws configure set aws_secret_access_key ' + self.config['aws_keys']['aws_secret_access_key']
				command_three = 'aws configure set default.region ' + self.config['aws_keys']['default_region']
				subprocess.call(command_one, shell=True)
				subprocess.call(command_two, shell=True)
				subprocess.call(command_three, shell=True)
		except NameError:
			print ("There was an error in getting the keys for aws.")

		#Azure configure
		try:
			if self.config['azure_keys']['username'] is None: # The variable
				print('The azure key is empty skipping')
			else:
				command = 'azure login -u ' + self.config['azure_keys']['username'] + ' -p ' + self.config['azure_keys']['password']
				subprocess.call(command, shell=True)
				subprocess.call('azure config mode arm', shell=True)
				subprocess.call('azure provider register Microsoft.Compute', shell=True)
				subprocess.call('azure provider register Microsoft.Network', shell=True)
		except NameError:
			print ("There was an error in getting the keys for azure.")

		#Openstack configure
		try:
			if self.config['openstack'] is None: # The variable
				print('The openstack key is empty skipping')
			else:
				command = 'source ' + self.config['openstack']
		except NameError:
			print ("There was an error in getting the keys for openstack")

	def runBenchmarks(self):
		

def main():
	perfkitRun = api_key_reader()
	perfkitRun.runAuthCommands()

main()
