###############################################################################################################################
#                                                       MD5HASHCRACK.PY                                                       #
#                                      A TOOL TO CRACK MD5 HASHES WRITTEN IN A TEXT FILE                                      #
#                                                                                                                             #
#                                   USAGE: md5HashCrack.py <FILENAME> <WORDLIST> [-h] [-v]                                    #
#                                   FILENAME: file containing newline-separated MD5 hashes                                    #
#                               WORDLIST: file containing possible newline-separated cleartext                                #
#                      -v, --verbose: execute program in verbose mode (outputs cleartext being compared)                      #
#                                       RUN WITH -h TO VIEW THIS HELP MESSAGE AND EXIT                                        #
#                                                                                                                             #
#                                                      have fun skiddies                                                      #
#                                                            -YBC                                                             #
###############################################################################################################################

import hashlib, argparse

# here I map three text colour-altering ANSI strings to global variables to increase readability later in the program
global TEXT_COLOUR_GREEN
global TEXT_COLOUR_RED
global TEXT_COLOUR_RESET

TEXT_COLOUR_GREEN = "\033[92m"
TEXT_COLOUR_RED = "\033[91m"
TEXT_COLOUR_RESET = "\033[0m"

def main():
	# I actually used argparse this time. It's a lot more user-friendly and not deprecated
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help = "File to crack MD5 hashes from (each hash must be on its own newline-separated line)", metavar = "<FILENAME>")
	parser.add_argument("wordlist", help = "Wordlist containing possible plaintext for the hashes (each word must be on its own newline-separated line)", metavar = "<WORDLIST>")
	parser.add_argument("-v", "--verbosity", help = "Run program in verbose mode (outputs words being tested against hash. Not required, default False)", action = "store_true")
	args = parser.parse_args()
	if (args.filename == None) | (args.wordlist == None):
		print parser.usage
		exit(0)
	else:
		filename = args.filename
		wordlist = args.wordlist
		verbosity = args.verbosity

	# will be used later
	crackedHashes = []
	uncrackedHashes = []
	flag_found = False
	
	# opening two files in read mode with just one statement is a pretty nice addition to Python 2.7.x
	with open(filename) as f, open(wordlist) as w:
		for line in f:
			flag_found = False
			for word in w:
				# the following statements instantiate a hashlib object and encrypt the cleartext read from the wordlist file
				# m.hexdigest() refers to the encrypted text
				# again, I used word.strip() so the word will be encrypted without a trailing newline (which would completely
				# change the hex digest)
				m = hashlib.md5()
				m.update(word.strip())
				if verbosity:
					print "[*] Trying '%s' [%s]" % (word.strip(), m.hexdigest())
				if m.hexdigest() == line.strip():
					flag_found = True
					cracked = word.strip()
				
			# what did I say about those variables being used later
			if flag_found:
				crackedHashes.append(cracked)
			else:
				uncrackedHashes.append(line.strip())
			w.seek(0)
				
	print
	
	# I know that formatting a string conditionally inside an if statement is probably bad practice but fuck it, it looks good
	if len(crackedHashes) > 0:
		print (TEXT_COLOUR_GREEN + "[+] Cracked %i %s (%i total)") % (len(crackedHashes), ("hashes" if len(crackedHashes) != 1 else "hash"), (len(crackedHashes) + len(uncrackedHashes)))
		for i in crackedHashes:
			m = hashlib.md5()
			m.update(i)
			print "[+] %s [%s]" % (i, m.hexdigest())
		print TEXT_COLOUR_RESET	
	
	if len(uncrackedHashes) > 0:
		print (TEXT_COLOUR_RED + "[-] Failed to crack %i %s (%i total)") % (len(uncrackedHashes), ("hashes" if len(uncrackedHashes) != 1 else "hash"), (len(crackedHashes) + len(uncrackedHashes)))
		for i in uncrackedHashes:
			print "[-] %s" % i
		print TEXT_COLOUR_RESET

if __name__ == "__main__":
	main()
