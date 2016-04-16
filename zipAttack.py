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

import zipfile, optparse, os, sys

# this class maps the text colour-altering ANSI strings to class variables so as to improve the code readability later on
class Text_Colours:
	RED = "\033[91m"
	GREEN = "\033[92m"
	RESET = "\033[0m"

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
	# the reason I use the evil os._exit(1) is because, fun fact, the regular exit(0) raises a SystemExit exception
	# so control would be directed to the except block, which would then execute pass and wouldn't exit the program at all
	try:
		z.extractall()
		print
		print Text_Colours.GREEN + "[+] Success! This archive didn't have a password." + Text_Colours.RESET
		os._exit(1)
	except:
		pass
	
	with open(wname) as f:
		for line in f:
			# we use line.strip() here to ensure that only the word is tried, not the word with a trailing newline
			password = line.strip()
			try:
				if verbosity:
					print "[*] Trying password '%s'..." % password
				z.extractall(pwd=password)
				# this part will only print if there was no exception raised, control wasn't directed to the except block and
				# therefore the password was correct
				print
				print (Text_Colours.GREEN + "[+] Success! Found password for archive %s: '%s'" + Text_Colours.RESET) % (zname, password)
				print (Text_Colours.GREEN + "[+] Extracted archive '%s'" + Text_Colours.RESET) % (zname.split('\\')[-1] if sys.platform == "win32" else zname.split('/')[-1])
				os._exit(1)
			# normally trying to use z.extractall() with an incorrect password (i.e. every iteration of the loop)
			# would raise a bad password exception and let us know about it but the pass statement stops this exception message
        		# from being printed
			except:
				pass
	
	# only runs if the word list is exhausted
	print
	print (Text_Colours.RED + "[-] Failed: Could not find password in supplied wordlist [%s]" + Text_Colours.RESET) % (wname.split('\\')[-1] if sys.platform == "win32" else wname.split('/')[-1])

main()
