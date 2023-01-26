#!/usr/bin/python3

RED = '\033[1;31;48m'
WHITE = "\33[0m"
GREEN = '\033[1;32;48m'

import ftplib
import time,optparse,sys,os

# ================== Function to check existence of file ===============
def check_file_existence(file_path):
	if os.path.exists(file_path) == False:
		return False
	else:
		return True

#============== Write to file found servers =========== 

# ================= Function to check ftp login ===============
def ftp_anonymous_login(server):
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	f = open(f"{current_time}_.txt", "a")
	ftp = ftplib.FTP(f'{server}') # note that this will connect to the host with default port of 21
	try:
		ftp.login("anonymous", "anonymous") # Check anonymous login credentials
	except ftplib.error_perm:
		print(f"[{RED}-{WHITE}] {server}")
	else:
		print(f"[{GREEN}+{WHITE}] {server}")
		f.write(f"\n{server}")


# =================== Function to test from file list ========================= 
def ftp_file(file_path):
	with open(file_path, 'r') as file:
		for line in file.readlines():
			ftp_anonymous_login(line.strip())

# =========================== Parsing options below ===========================

parser = optparse.OptionParser("\n./main.py [-h or --help] [-f or --file]=<file-path-with-IPs or Domains For FTP servers, one on each line> [-l or --ftp=domain or IP of ftp server]")
parser.add_option("-f", "--file", dest="server_file_path", type='string', help="specify the file containing server IP/domains")
parser.add_option("-t", "--ftp", dest="ftp_server_addr", type='string', help="specify a single ftp server")
(options, args) = parser.parse_args()

# ======================= Main Function Below ========================
def main():
	if options.server_file_path == None and options.ftp_server_addr == None:
		parser.error(f"\n[{RED}Error{WHITE}] Insufficent Arguments supplied {RED}-f/--file{WHITE} or {RED}-t/--ftp{WHITE} missing value\n")
		sys.exit(0)
	elif options.server_file_path != None:
		file_path = options.server_file_path
		if check_file_existence(file_path):
			print(f"[{GREEN}+{WHITE}] reading from file..")
			print(f"[*] successful login IP/domains will be saved to a a:b:c:_.txt in current directory..")
		else:
			print(f"[{RED}!{WHITE}] unable to process specified file")
			sys.exit(0)
	elif options.ftp_server_addr != None:
		ftp_anonymous_login(options.ftp_server_addr)

main()