import hashlib, argparse

hash = "3e25960a79dbc69b674cd4ec67a72c62"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help = "File to crack hashes from", required = True, metavar = "<filename>")
    parser.add_argument("-w", "--wordlist", help = "Wordlist containing possible passwords", required = True, metavar = "<wordlist>")
    parser.parse_args()
    
    try:
        with open(filename) as f:
            with open(wordlist) as w:
                for line in f:
                    for line in w:
                        m = hashlib.md5()
                        m.update(line)
                        if m.hexdigest() == hash:
                            print "Found password: %s" % word
    except:
        pass

main()
