# Still very much a work in progress

import zipfile, argparse, math

TEXT_COLOUR_GREEN = "\033[92m" 
TEXT_COLOUR_RED = "\033[91m" 
TEXT_COLOUR_RESET = "\033[0m" 


def tryCrack(password, zipFile):
    try:
        zipFile.extractall(pwd = password)
        print (TEXT_COLOUR_GREEN + "Found password: %s" % password)
        print (("Extracted %s" % zipfile) + TEXT_COLOUR_RESET)
        exit(0)
    except RuntimeError:
        return

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
        
    return noOfLetters
    
def main():
    noOfLetters = parse()
    z = zipfile.ZipFile()
    startString = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for i in range(noOfLetters):
        startString.append("A")
    
    while attempts != ((math.factorial(26)) / (math.factorial(noOfLetters) * math.factorial(26 - noOfLetters)):
        for letter in alphabet:
            tryCrack(str(startString), z)
            startString[-1] = letter
            if startString[-1] = "Z":
                for i in reversed(startString):
                    if (i == "Z") and (i != len(startString)):
                        startString[i] = chr(ord(startString[i] + 1))

print (TEXT_COLOUR_RED + "Sorry, the zip file's password was not found!" + TEXT_COLOUR_RESET)
exit(0)
