import os
import sys
import winreg
import subprocess

class PyWIN32Service:
	service_name = ""
	executable = ""
	display_name = ""

	def __init__(self, service_name, executable, display_name):
		self.service_name = service_name
		self.executable = executable
		self.display_name = display_name

	# @params:	string	operation system command
	def call(self, command):
		process = subprocess.Popen(command,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True,universal_newlines=True)
		std_out,std_err = process.communicate()
		return process.returncode,std_out,std_err

	def findPythonPath(self):
		code,out,err = self.call("echo %PATH%")
		out = out.strip().split(";")
		env = [s for s in out if "Python" in s]
		if env:
			env_list = env[-1].split("\\")
			for i,j in enumerate(env_list):
				if "Python" in j:
					env_index = env_list.index(j)+1
			try:
				binPath = "\\".join(env_list[:env_index])
			except Exception:
				pass
			if binPath:
				return binPath
		return False

	def findSrvanyPath(self):
		code, out, err = self.call("echo %PATH%")
		out = out.strip().split(";")
		env = [s for s in out if "Windows Resource Kits" in s]
		if env:
			env_list = env[-1].split("\\")
			for i,j in enumerate(env_list):
				if "Windows Resource Kits" in j:
					env_index = env_list.index(j)+2
			try:
				binPath = "\\".join(env_list[:env_index])
			except Exception:
				pass
			if binPath:
				return binPath
		return False

	# @params:	string	path to python script
	def findAppDir(self, executable):
		app_dir = executable.split("\\")[:-1]
		app_dir = "\\".join(app_dir)
		return app_dir

	# @params:	string	service name (usually name of script)
	# @params:	string	registry key name (usually name of script)
	# @params:	string	registry key value (name that will be displayed in services list)
	def addRegistryKey(self, service_name, key, value):
		try:
			reg_key = f"SYSTEM\CurrentControlSet\Services\{self.service_name}\Parameters"
			hive = winreg.HKEY_LOCAL_MACHINE
			if not os.path.exists(reg_key):
				winreg.CreateKey(hive, reg_key)
			RegistryKey = winreg.OpenKey(hive, reg_key, 0, winreg.KEY_WRITE)
			winreg.SetValueEx(RegistryKey, key, 0, winreg.REG_SZ, value)
			winreg.CloseKey(RegistryKey)
		except Exception as e:
			raise SystemExit(f"Add '{key}' registry key error: {e}")

	def install(self):
		try:
			code, out, err = self.call(f"sc query {self.service_name}|findstr SERVICE_NAME")
			if out:
				sys.exit("Service already installed")
			srvany = self.findSrvanyPath()
			if(srvany):
				srvany_env = srvany+"\\srvany.exe"
			else:
				sys.exit("Windows Resource Kit not found.")
			code, out, err = self.call(f"sc create {self.service_name} binPath= \"{srvany_env}\" start= auto DisplayName= \"{self.display_name}\"")
			if err:
				sys.exit(f"Service install failed: {err}")
			python = self.findPythonPath()
			if python:
				python_env = python+"\\python.exe"
			else:
				sys.exit("Python interpreter not found.")
			app_dir = self.findAppDir(self.executable)
			self.addRegistryKey(self.service_name, "Application", python_env)
			self.addRegistryKey(self.service_name, "AppParameters", self.executable)
			self.addRegistryKey(self.service_name, "AppDirectory", app_dir)
			print("Service installed successfully")
		except Exception as e:
			raise SystemExit(f"Service install failed: {e}")

	def uninstall(self):
		code, out, err = self.call(f"sc query {self.service_name}|findstr {self.service_name}")
		if not out:
			sys.exit("Service not exist")
		code, out, err = self.call(f"sc delete {self.service_name}")
		print("Service uninstalled successfully")

	def usage(self):
		sys.exit(f"Usage: python {sys.argv[0]} (install|uninstall)")
