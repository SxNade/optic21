#!/usr/bin/python3

RED = '\033[1;31;48m'
WHITE = "\33[0m"
GREEN = '\033[1;32;48m'

print(f'''\noptic21-{RED}v(1.1){WHITE}
Author: {RED}Bhairav{WHITE}
{WHITE}Copyright (c) 2023{WHITE}
{GREEN}[scan anonymous ftp login]{WHITE}\n''')


import ftplib
import time,optparse,sys,os,ipaddress

# ===== time place holder ====
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


# ================== Function to check existence of file ===============
def check_file_existence(file_path):
	if os.path.exists(file_path) == False:
		return False
	else:
		return True

#============== Write to file found servers =========== 

#============== parse subnets/IP ===============
#======== we will do parsing to save it in a tuple, tuple is more memory efficent===

def parse_subnets(subnet):
	ip_tuple = tuple(ipaddress.ip_network(subnet, False).hosts())
	return ip_tuple

# ================= Function to check ftp login ===============
def ftp_anonymous_login(server):
	try:
		ftp = ftplib.FTP(f'{server}', timeout=5) # note that this will connect to the host with default port of 21 with default timeout set to 2
		ftp.login("anonymous", "anonymous") # Check anonymous login credentials
	except ftplib.error_perm:
		print(f"[{RED}-{WHITE}] {server}")
	except TimeoutError:
		print(f"[{RED}-{WHITE}] {server} 5sec {RED}timeout{WHITE}")
	except ftplib.error_temp:
		print(f"[{RED}-{WHITE}] {server} {RED}requires TLS?{WHITE}")
	except ConnectionRefusedError:
		print(f"[{RED}-{WHITE}] {server} {RED}connection refused!{WHITE}")
	except OSError:
		print(f"[{RED}-{WHITE}] {server} {RED}error!{WHITE}")
	else:
		print(f"[{GREEN}+{WHITE}] {server}")
		f = open(f"{current_time}_.txt", "a")
		f.write(f"\n{server}")


# =================== Function to test from file list ========================= 
def ftp_file(file_path):
	with open(file_path, 'r') as file:
		for line in file.readlines(): # Nested For loop to loop through subnet and then each individual IP in it
			tuple = parse_subnets(line)
			for ip in tuple:
				ftp_anonymous_login(str(ip))

# =========================== Parsing options below ===========================

parser = optparse.OptionParser("\n./main.py [-h or --help] [-f or --file]=<file-path-with-IPs or Domains For FTP servers, one on each line> [-l or --ftp=domain or IP of ftp server]")
parser.add_option("-f", "--file", dest="server_file_path", type='string', help="specify the file containing server IP/domains or subnets")
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
			print(f"[*] successful login IP/domains will be saved to {current_time} in current directory..\n")
			ftp_file(file_path)

		else:
			print(f"[{RED}!{WHITE}] unable to process specified file")
			sys.exit(0)
	elif options.ftp_server_addr != None:
		tuple = parse_subnets(options.ftp_server_addr)
		for ip in tuple:
			ftp_anonymous_login(str(ip))
main()
