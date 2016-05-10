# Still very much a work in progress

import zipfile, argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("noOfLetters", metavar = "<NOOFLETTERS>", type = int, help = "How many letters does the password contain?")
    args = parser.parse_args()
    if args.noOfLetters == None:
        print parser.usage()
        exit(0)
    else:
        noOfLetters = args.noOfLetters
        
    return noOfLetters
    
def main():
    noOfLetters = parse()
    startString = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    flag_found = True
    
    for i in range(noOfLetters):
        startString += "A"
    
    
