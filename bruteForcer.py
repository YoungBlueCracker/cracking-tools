###############################################################################################################################
#                                                       BRUTEFORCER.PY                                                        #
#                           A TOOL TO CRACK PASSWORD-PROTECTED ZIP FILES USING A BRUTE FORCE METHOD                           #
#                                                                                                                             #
#                                  USAGE: bruteForcer.py <NOOFCHARACTERS> <CHARACTERSET> [-v]                                 #
#                                                                                                                             #
#   NOOFCHARACTERS: The number of characters in the password. If unknown, enter -1; this will test every combination of one   #
#  character, then every combination of two characters, then three, etc. Be careful, this can easily start an infinite loop   #
#                                               with an incorrect character set.                                              #
#    CHARACTERSET: The character set(s) to use. Use A to test upper case letters, a to test lower case letters, n to test     # 
#   numbers and s to test special characters. You can use any combination of A, a, n and s, e.g. A, s, sa, Aans, snaA, etc.   #
#                                       -v: verbose mode (outputs word being attempted)                                       #
#                                          RUN WITH -h TO VIEW HELP MESSAGE AND EXIT                                          #
#                                                                                                                             #
#   KNOWN ISSUES: In verbose mode, it sometimes outputs the word it's trying to crack the zip file with twice. This doesn't   #
#                                                affect how well it functions.                                                #
#                                                                                                                             #
#                                                      have fun skiddies                                                      #
#                                                            -YBC                                                             #
###############################################################################################################################

import zipfile, argparse, time, os, sys

# these variables will improve readability later on in the program
TEXT_COLOUR_GREEN = "\033[92m"
TEXT_COLOUR_RED = "\033[91m"
TEXT_COLOUR_RESET = "\033[0m"

def parse():
	parser = argparse.ArgumentParser(epilog = "Example: bruteForcer.py 3 Aans passwords.zip -v")
	parser.add_argument("noOfCharacters", metavar = "<NOOFCHARACTERS>", type = int, help = "How many characters does the password contain? Enter \"-1\" if you don't know (just be careful, this can start an infinite loop very easily and you might need to mash Ctrl+C a few times to exit the program if you use the wrong character set).")
	parser.add_argument("characterSet", metavar = "<CHARACTERSET>", help = "The character set(s) to use. Type A for uppercase letters, a for lowercase letters, n for numbers, and s for special characters. You can use any of the 24 combinations of A, a, n, and s.")
	parser.add_argument("zipFile", metavar = "<ZIPFILE>", help = "The zip file that we are attempting to crack.")
	parser.add_argument("-v", "--verbose", help = "Run program in verbose mode", action = "store_true", default = False)
	args = parser.parse_args()
	if (args.noOfCharacters == None) or (args.characterSet == None) or (args.zipFile == None):
		print parser.usage()
		exit(0)
	else:
		noOfCharacters = args.noOfCharacters
		characterSet = args.characterSet
		zipFile = args.zipFile
		verbosity = args.verbosity
		
	return args

def spin():
	while True:
		for cursor in "|||||||///////-------\\\\\\\\\\\\\\":
			yield cursor
			
def failed():
	print
	print TEXT_COLOUR_RED + "[-] The zip file's password was not found. Trying a different number of characters or a different character set might help."
	print ("[-] Script ran in %s seconds." % round(time.clock() - startTime, 2)) + TEXT_COLOUR_RESET
	exit(0)
	
# I would except only RuntimeError here normally but if I do I get an "Invalid code lengths set" error pretty soon after the program starts to run
# If anyone knows what causes this, I'd love to know!
def tryCrack(password, zipFile):
	try:
		zipFile.extractall(pwd = password)
		print
		print (TEXT_COLOUR_GREEN + ("[+] Success! Found password for archive '%s' in %s seconds: '%s'" % (args.zipFile, round(time.clock() - startTime, 2), password)))
		print (("[+] Extracted archive '%s'." % args.zipFile) + TEXT_COLOUR_RESET)
		os._exit(1)
	except:
		return
		
def main():
	# constants
	UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
	NUMBERS = "0123456789"
	SPECIAL_CHARACTERS = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
	
	# variables
	global args
	global startTime
	args = parse()
	spinner = spin()
	z = zipfile.ZipFile(args.zipFile)
	currentPassword = []
	reversedCurrentPassword = []
	chosenCharacterSets = []
	scan = 0
	cycleCounter = abs(args.noOfCharacters)
	flag_exhaustedAllCombinations = False
	dialogue = ""
	confirm = ""
	
	if "A" in args.characterSet:
		dialogue += UPPER_CASE
		chosenCharacterSets.append("A (upper case)")
	if "a" in args.characterSet:
		dialogue += LOWER_CASE
		chosenCharacterSets.append("a (lower case)")
	if "n" in args.characterSet:
		dialogue += NUMBERS
		chosenCharacterSets.append("n (numbers)")
	if "s" in args.characterSet:
		dialogue += SPECIAL_CHARACTERS
		chosenCharacterSets.append("s (special characters)")
		
	# I use an array instead of a string because in Python, arrays are mutable, whilst strings aren't.
	for i in range(abs(args.noOfCharacters)):
		currentPassword.append(dialogue[0])
		
	print
	print "[*] You have chosen to attempt to crack a password which has %s characters." % (args.noOfCharacters if args.noOfCharacters != -1 else "an indeterminate number of")
	print "[*] You have chosen to use the character sets %s." % (', '.join(chosenCharacterSets))
	print
	print "[*] Begin cracking? (Y / N)"
	while confirm not in ["Y", "y", "N", "n"]:
		confirm = raw_input()
		if (confirm == "N") or (confirm == "n"):
			print
			print TEXT_COLOUR_RED + "[-] Program terminating." + TEXT_COLOUR_RESET
			exit(0)
		elif (confirm == "Y") or (confirm == "y"):
			pass
			
	startTime = time.clock()
	
	# in case the zip file doesn't actually have a password / is 0 characters in length
	try:
		z.extractall()
		print
		print (TEXT_COLOUR_GREEN + ("[+] Success! This archive didn't have a password."))
		print (("[+] Extracted archive '%s'" % args.zipFile) + TEXT_COLOUR_RESET)
		exit(0)
	except RuntimeError:
		if args.noOfCharacters == 0:
			failed()
		else:
			pass
			
	while not flag_exhaustedAllCombinations:
		if not args.verbosity:
			timeMessage = "[%s] Taken %s seconds so far..." % (spinner.next(), round(time.clock() - startTime, 2))
			sys.stdout.write(timeMessage)
			for i in range(len(timeMessage)):
				sys.stdout.write("\b")
				
		for letter in dialogue:
			if args.verbosity:
				print "[*] Trying: %s" % ''.join(currentPassword)
			tryCrack(''.join(currentPassword), z)
			currentPassword[-1] = letter
			
			reversedCurrentPassword = list(reversed(currentPassword))
			
			# checks if the final character of currentPassword is equal to the final character of dialogue (the string containing all possible
			# characters, generated from the character sets chosen when calling the program). Prints the password being tested if program was
			# run in verbose mode. Tries to crack the password on the zip file using this password. Checks if password string consists
			# of the final character in the dialogue string repeated args.noOfCharacters times. If a definite number of characters for the
			# password was defined, all possible password permutations must have been tested, so the brute force attack failed. However, if
			# an indefinite number of characters for the password was defined (args.noOfCharacters == -1), appends another dialogue[0]
			# character to the currentPassword array, sets every character in the array to dialogue[0], and starts the loop over again.
			
			# the else branch after the statement cycleCounter += 1 loops the currentPassword array correctly, even when there is more than
			# one dialogue[-1] character in the array (e.g. "BZY" -> "BZZ" -> "CAA" -> "CAB" -> ...)
			
			if currentPassword[-1] == dialogue[-1]:
				if args.verbosity:
					print "[*] Trying: %s" % ''.join(currentPassword)
				tryCrack(''.join(currentPassword), z)
				if ''.join(currentPassword) == dialogue[-1] * cycleCounter:
					if args.noOfCharacters != -1:
						flag_exhaustedAllCombinations = True
					else:
						currentPassword.append(dialogue[0])
						for i in range(len(currentPassword)):
							currentPassword[i] = dialogue[0]
					cycleCounter += 1
				else:
					while reversedCurrentPassword[scan] == dialogue[-1]:
						scan += 1
						
					reversedCurrentPassword[scan] = dialogue[dialogue.index(reversedCurrentPassword[scan]) + 1]
					
					for i in range(scan):
						reversedCurrentPassword[i] = dialogue[0]
						
					scan = 0
					currentPassword = list(reversed(reversedCurrentPassword))
		
	# this should only run if the while loop has been exited and so the password wasn't found
	failed()
	
if __name__ == "__main__":
	main()
