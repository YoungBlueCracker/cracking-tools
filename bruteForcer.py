# still very much a work in progress

import zipfile, argparse, math, os, time, sys

startTime = time.clock()

# these variables will improve readability later on in the program
TEXT_COLOUR_GREEN = "\033[92m" 
TEXT_COLOUR_RED = "\033[91m" 
TEXT_COLOUR_RESET = "\033[0m" 

# I would except only RuntimeError here normally but if I do I get an "Invalid code lengths set" error pretty soon after it starts
# to run - if anyone knows what causes this, I'd love to know!
def tryCrack(password, zipFile):
	try:
		zipFile.extractall(pwd = password)
		print
		print (TEXT_COLOUR_GREEN + ("[+] Success! Found password for archive '%s' in %s seconds: '%s'" % (args.zipFile, round(time.clock() - startTime, 2), password)))
		print (("[+] Extracted archive '%s'." % args.zipFile) + TEXT_COLOUR_RESET)
		os._exit(1)
	except:
		return

# used later
def nCr(n, r):
	return (math.factorial(n)) / ((math.factorial(r) * math.factorial(n - r)))

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("noOfLetters", metavar = "<NOOFLETTERS>", type = int, help = "How many letters does the password contain?")
	parser.add_argument("zipFile", metavar = "<ZIPFILE>", help = "The zip file that we are attempting to crack.")
	parser.add_argument("characterSet", metavar = "CHARACTERSET=A[a[n[s]]]", help = "The character set to use. Choose A for uppercase letters, a for lowercase letters, n for numbers, and s for special characters.")
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
	
def main():
	global args
	
	args = parse()
	z = zipfile.ZipFile(args.zipFile)
	startString = []
	counter = 1
	maxCombinations = nCr(26, args.noOfLetters)
	
	flag_exhaustedAllCombinations = False
	flag_uppercaseAlphabet = False
	flag_lowercaseAlphabet = False
	flag_numbers = False
	flag_specialChars = False
	
	alphabet_upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	alphabet_lowerCase = "abcdefghijklmnopqrstuvwxyz"
	numbers = "123456789"
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
			
			if counter > maxCombinations:
				flag_exhaustedAllCombinations = True	
			counter += 1
			
			# checks if the last letter of the password (currently an array) is "Z" then loops through the list looking for other "Z"s
			# each iteration, sets posJ to the index at which j is currently at in the list
			# when it finds a "Z" and if the element isn't at index 0, tries to crack the zip file with that password, then advances 
			# the letter one element before by one ("A" -> "B", "B" -> "C", etc).
			# finally, sets the letter at the current index back to "A"
			# if the position of the current "Z" IS at index 0, the script will simply try to crack the zip file with this password and
			# then set the letter at the current index back to "A" so to avoid the rightmost letter (index -1) being messed with.
			
			if startString[-1] == "Z":
				for j in startString:
					posJ = startString.index(j)
					if (j == "Z"):
						if (posJ != 0):
							if args.verbosity:
								print "[*] Trying: %s" % ''.join(startString)
							tryCrack(''.join(startString), z)
							startString[posJ - 1] = chr(ord(startString[posJ - 1]) + 1)
							startString[posJ] = "A"
						else:
							if args.verbosity:
								print "[*] Trying: %s" % ''.join(startString)
							tryCrack(''.join(startString), z)
							startString[posJ] = "A"

	# this should only run if the while loop has been exited and so the password wasn't found
	print (TEXT_COLOUR_RED + "[-] The zip file's password was not found. Trying a different number of characters or a different character set might help.")
	print (("[-] Script ran in %s seconds." % round(time.clock() - startTime, 2)) + TEXT_COLOUR_RESET)
	exit(0)

if __name__ == "__main__":
	main()

# TODO: Actually implement different character sets. 
