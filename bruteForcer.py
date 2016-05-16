# still very much a work in progress

import zipfile, argparse, math

# these variables will improve readability later on in the program
TEXT_COLOUR_GREEN = "\033[92m" 
TEXT_COLOUR_RED = "\033[91m" 
TEXT_COLOUR_RESET = "\033[0m" 

def tryCrack(password, zipFile):
    try:
        zipFile.extractall(pwd = password)
        print (TEXT_COLOUR_GREEN + "Found password: %s" % password)
        print (("Extracted %s" % zipfile) + TEXT_COLOUR_RESET)
        os._exit(0)
    except RuntimeError:
        return

# used later
def nCr(n, r):
	return (math.factorial(n)) / ((math.factorial(r) * math.factorial(n - r)))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("noOfLetters", metavar = "<NOOFLETTERS>", type = int, help = "How many letters does the password contain?")
    parser.add_argument("zipFile", metavar = "<ZIPFILE>", help = "The zip file that we are attempting to crack.")
    args = parser.parse_args()
    if (args.noOfLetters == None) or (args.zipFile == None):
        print parser.usage()
        exit(0)
    else:
        noOfLetters = args.noOfLetters
        zipFile = args.zipFile
        
    return args
    
def main():
    args = parse()
    z = zipfile.ZipFile(args.zipFile)
    startString = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # in case the zip file doesn't actually have a password
    try:
        z.extractall()
        print (TEXT_COLOUR_GREEN + "Success! This archive didn't have a password.")
        print (("Extracted %s" % z) + TEXT_COLOUR_RESET)
    except RuntimeError:
        pass
    
    # creates an array of size noOfLetters and sets each element in the array to "A" (strings are immutable; arrays aren't)
    for i in range(args.noOfLetters):
        startString.append("A")
    
    
    # the range is 26 choose noOfLetters, which is the maximum number of combinations that the password can possibly be
    for i in range(nCr(26, args.noOfLetters)):
        for letter in alphabet:
            tryCrack(str(startString), z)
            startString[-1] = letter
            if startString[-1] == "Z":
                for j in reversed(startString):
                    if (j == "Z") and (j != len(startString)):
                        # got an error here, still figuring out how to fix it
                        startString[j - 1] = chr(ord(startString[j] + 1))
                        startString[j] = "A"

    print (TEXT_COLOUR_RED + "Sorry, the zip file's password was not found!" + TEXT_COLOUR_RESET)
    exit(0)

main()
