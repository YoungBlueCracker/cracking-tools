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

def parse():
	parser = optparse.OptionParser("Usage: zipAttack.py -f <zipfile> -w <wordlist>")
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
	
	return options
	
def main():
	options = parse()
	
	# these variables will improve code readability later on
	TEXT_COLOUR_GREEN = "\033[92m"
	TEXT_COLOUR_RED = "\033[91m"
	TEXT_COLOUR_RESET = "\033[0m"
	
	z = zipfile.ZipFile(options.zname)
	
	# we'll first just try to extract without any password, just in case the zip file doesn't actually have a password
	try:
		z.extractall()
		print
		print TEXT_COLOUR_GREEN + "[+] Success! This archive didn't have a password." + TEXT_COLOUR_RESET
		exit(0)
	except RuntimeError:
		pass
	
	with open(options.wname) as f:
		for line in f:
			# we use line.strip() here to ensure that only the word is tried, not the word with a trailing newline
			password = line.strip()
			try:
				if options.verbosity:
					print "[*] Trying password '%s'..." % password
				z.extractall(pwd=password)
				# this part will only print if there was no exception raised, control wasn't directed to the except block and
				# therefore the password was correct
				print
				print (TEXT_COLOUR_GREEN + "[+] Success! Found password for archive '%s': '%s'") % (options.zname, password)
				print ("[+] Extracted archive '%s'" + TEXT_COLOUR_RESET) % (os.path.split(options.zname)[1])
				os._exit(1)
			# normally trying to use z.extractall() with an incorrect password (i.e. every iteration of the loop)
			# would raise a bad password exception and let us know about it but the pass statement stops this exception message
			# from being printed
			# unfortunately I can't catch only a RuntimeError here because I get a new error about an invalid code length
			# if the password isn't found in the word list - any insight about this error would be great!
			except:
				pass
	
	# only runs if the word list is exhausted
	print
	print (TEXT_COLOUR_RED + "[-] Failed: Could not find password in supplied wordlist [%s]" + TEXT_COLOUR_RESET) % (os.path.split(options.wname)[1])

if __name__ == "__main__":
	main()
