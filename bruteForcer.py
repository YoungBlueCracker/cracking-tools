# Still very much a work in progress

import zipfile, argparse

def tryCrack(password, zipFile):
    try:
        zipFile.extractall(pwd = string)
    except:

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
    flag_found = False
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for i in range(noOfLetters):
        startString.append("A")
    
    while not flag_found:
        for letter in alphabet:
            startString[-1] = letter
            tryCrack(str(startString), z)
            if startString[-1] = "Z":
                for i in reversed(startString):
                    if (i == "Z") and (i != len(startString)):
                        startString[i] = chr(ord(startString[i] + 1))
