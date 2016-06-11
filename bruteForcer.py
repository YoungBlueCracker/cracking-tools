# still very much a work in progress

import zipfile, argparse, os, time, sys

startTime = time.clock()

# these variables will improve readability later on in the program
TEXT_COLOUR_GREEN = "\033[92m" 
TEXT_COLOUR_RED = "\033[91m" 
TEXT_COLOUR_RESET = "\033[0m" 

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("noOfLetters", metavar = "<NOOFLETTERS>", type = int, help = "How many letters does the password contain?")
	parser.add_argument("zipFile", metavar = "<ZIPFILE>", help = "The zip file that we are attempting to crack.")
	parser.add_argument("characterSet", metavar = "<CHARACTERSET>", help = "The character set to use. Type A for uppercase letters, a for lowercase letters, n for numbers, and s for special characters. You can use any combination of A, a, n or s.")
	parser.add_argument("-v", "--verbosity", help = "Run program in verbose mode", action = "store_true", default = False)
	args = parser.parse_args()
	if (args.noOfLetters == None) or (args.zipFile == None) or (args.characterSet == None):
		print parser.usage()
		exit(0)
	else:
		noOfLetters = args.noOfLetters
		zipFile = args.zipFile
		characterSet = args.characterSet
		verbosity = args.verbosity
		
	return args

# I would except only RuntimeError here normally but if I do I get an "Invalid code lengths set" error pretty soon after it starts to run
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
	global args
	
	args = parse()
	z = zipfile.ZipFile(args.zipFile)
	
	startString = []
	
	scan = 0
	
	flag_exhaustedAllCombinations = False
	flag_uppercaseAlphabet = False
	flag_lowercaseAlphabet = False
	flag_numbers = False
	flag_specialChars = False
	
	alphabet_upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	alphabet_lowerCase = "abcdefghijklmnopqrstuvwxyz"
	numbers = "0123456789"
	specialCharacters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
	
	if "=" in args.characterSet:
		characterSetString = args.characterSet.split("=")[1]
	else:
		characterSetString = args.characterSet
		
	if "A" in characterSetString:
		flag_uppercaseAlphabet = True
	if "a" in characterSetString:
		flag_lowercaseAlphabet = True
	if "n" in characterSetString:
		flag_numbers = True
	if "s" in characterSetString:
		flag_specialChars = True
		
	# creates an array of size noOfLetters and sets each element in the array to "A" (arrays are mutable; strings aren't)
	for i in range(args.noOfLetters):
		startString.append("A")
	
	# in case the zip file doesn't actually have a password
	try:
		z.extractall()
		print (TEXT_COLOUR_GREEN + "[+] Success! This archive didn't have a password.")
		print (("[+] Extracted archive '%s'" % args.zipFile) + TEXT_COLOUR_RESET)
		exit(0)
	except RuntimeError:
		pass
	
	while not flag_exhaustedAllCombinations:
		if not args.verbosity:
			timeMessage = "[*] Taken %s seconds so far..." % (round(time.clock() - startTime, 2))
			sys.stdout.write(timeMessage)
			for i in range(len(timeMessage)):
				sys.stdout.write("\b")
				
		for letter in alphabet_upperCase:
			if args.verbosity:
				print "[*] Trying: %s" % ''.join(startString)
			tryCrack(''.join(startString), z)
			startString[-1] = letter
			
			reversedStartString = list(reversed(startString))
			
			# the while loop and subsequent code here essentially scans through reversedStartString until reversedStartString[scan] is not a 
			# "Z" character, advances this character by 1 ("A" -> "B", "B" -> "C", etc.) then sets every "Z" character in the string back to
			# "A". The purpose of this code is to ensure that at times where there is more than one "Z" in the password being tried, the 
			# string isn't set to "A[A" -> "A[B", etc (as the [ character is the character after Z in ascii), or "BAZ" -> "BBA" 
			# (which would skip the whole "BA<thirdCharacter>" branch).
			
			if reversedStartString[0] == "Z":
				if ''.join(reversedStartString) == "Z" * args.noOfLetters:
					flag_exhaustedAllCombinations = True
				else:
					if args.verbosity:
						print "[*] Trying: %s" % ''.join(startString)
					tryCrack(''.join(startString), z)
					while (reversedStartString[scan] == "Z") and (scan + 1 < args.noOfLetters):
						scan += 1
				
					reversedStartString[scan] = chr(ord(reversedStartString[scan]) + 1)
			
					for j in range(scan):
						reversedStartString[j] = "A"
				
					scan = 0
					startString = list(reversed(reversedStartString))

	# this should only run if the while loop has been exited and so the password wasn't found
	print (TEXT_COLOUR_RED + "[-] The zip file's password was not found. Trying a different number of characters or a different character set might help.")
	print (("[-] Script ran in %s seconds." % round(time.clock() - startTime, 2)) + TEXT_COLOUR_RESET)
	exit(0)

if __name__ == "__main__":
	main()

# TODO: Actually implement different character sets.
