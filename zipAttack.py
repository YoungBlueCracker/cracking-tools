###############################################################################################################################
#                                                        ZIPATTACK.PY                                                         #
#                           A TOOL TO CRACK PASSWORD-PROTECTED ZIP FILES USING A DICTIONARY ATTACK                            #
#                                                                                                                             #
#                                    USAGE: zipAttack.py -f <FILENAME> -w <WORDLIST> [-v]                                     #
#                                                     FILENAME: a zip file                                                    #
#                      WORDLIST: a Python-readable document containing a list of newline-separated words                      #
#                                       -v: verbose mode (outputs word being attempted)                                       #
#                                       RUN WITH -h TO VIEW THIS HELP MESSAGE AND EXIT                                        #
#                                                                                                                             #
#                                    KNOWN ISSUES: It doesn't play nice with big word lists                                   #
#                                                                                                                             #
#                                                      have fun skiddies                                                      #
#                                                            -YBC                                                             #
###############################################################################################################################

import zipfile, optparse, os

def main():
	# I wanted to do optparse in a separate function but I also didn't want to use any global variables so here we are
	# I'll also probably replace optparse with argparse next program since optparse is deprecated now anyway
	parser = optparse.OptionParser("Usage: python zipAttack.py -f <zipfile> -w <wordlist>")
	parser.add_option("-f", dest="zname", type="string", help="specify zip file (required)")
	parser.add_option("-w", dest="wname", type="string", help="specify word list (required)")
	parser.add_option("-v", dest="verbosity", action="store_true", help="increase verbosity (not required, default false)")
	(options, args) = parser.parse_args()
	if (options.zname == None) | (options.wname == None):
		print parser.usage
		exit(0)
	else:
		zname = options.zname
		wname = options.wname
		verbosity = options.verbosity
	
	z = zipfile.ZipFile(zname)
	
	# we'll first just try to extract without any password, just in case the zip file doesn't actually have a password
	try:
		z.extractall()
		print
		print "\033[92m[+] Success! This archive didn't have a password.\033[0m"
		os._exit(1)
	except:
		pass
	
	# now for the juicy bit - first we open the file specified by the user on the command line
	with open(wname) as f:
		for line in f:
			# we use line.strip() here to ensure that only the word is tried, not the word with a trailing newline
			password = line.strip()
			try:
				if verbosity:
					print "[*] Trying password '%s'..." % password
				z.extractall(pwd=password)
				# this part will only print if there was no exception raised and therefore the password was correct
				# the escape sequence \033[92m colours the terminal text green so it stands out
				# \033[0m at the end of the line changes the colour back to the original one
				print
				print "\033[92m[+] Success! Found password for archive %s: '%s'\033[0m" % (zname, password)
				os._exit(1)
			# normally trying to use z.extractall() with an incorrect password (i.e. every iteration of the loop)
			# would raise a bad password exception but the pass statement stops this
			# exception being raised
			except:
				pass
	
	# only runs if the word list is exhausted
	# \033[91m changes the terminal text colour to red whilst \033[0m changes the terminal text colour back to
	# its original colour
	print
	print "\033[91m[-] Failed: Could not find password in supplied wordlist [%s]\033[0m" % (wname.split('\\')[-1] if sys.platform == "win32" else wname.split('/')[-1])

main()
