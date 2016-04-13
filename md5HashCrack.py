import hashlib, argparse, os

# hash = "3e25960a79dbc69b674cd4ec67a72c62"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help = "File to crack hashes from", required = True, metavar = "<filename>")
    parser.add_argument("-w", "--wordlist", help = "Wordlist containing possible passwords", required = True, metavar = "<wordlist>")
    parser.add_argument("-v", "--verbosity", help = "Run program in verbose mode (outputs words being tested against hash)", action = "store_true")
    args = parser.parse_args()
    if (args.filename == None) | (args.wordlist == None):
        print parser.usage
        exit(0)
    else:
        args.filename = filename
        args.wordlist = wordlist
        args.verbosity = verbosity
    
    try:
        with open(filename) as f:
            with open(wordlist) as w:
                for line in f:
                    for word in w:
                        m = hashlib.md5()
                        m.update(word)
                        if verbosity:
                            print "[*] Trying %s [%s]" % (word, m.hexdigest())
                        if m.hexdigest() == line:
                            print "\033[92m[+] Found password: %s\033[0m" % word
                            os._exit(1)
    except:
        pass
    
    print "\033[91m[-] Failed: could not find password in supplied wordlist [%s]\033[0m" % \
                                                        (wordlist.split("/")[-1] if os.name == "linux2" else wordlist.split("\\")[-1]

main()
