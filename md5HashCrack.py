import hashlib, argparse, os.path

def argParser():
	global args
	parser = argparse.ArgumentParser(description = "Dictionary attack on a text document containing hashes of passwords.")
	parser.add_argument("passwordfile", help = "File containing encrypted passwords.", type = str)
	parser.add_argument("wordlist", help = "Word list used to attack passwords.", type = str)
	#parser.add_argument("-e", "--encryption", help = "Encryption standard used. Can be either SHA1, SHA224, SHA256, SHA384, SHA512 or MD5 (default MD5).", choices = ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"])
	args = parser.parse_args()
	return args
	
def main():
	argParser()
	
	if os.path.isfile(args.passwordfile) and os.path.isfile(args.wordlist):
		with open(args.passwordfile) as f:
			for user in f:
				found = False
				username = user.split(":")[0].strip()
				password = user.split(":")[1].strip()
				print "[+] Attempting to crack password for user '%s'" % username
				with open(args.wordlist) as g:
					for word in g:
						m = hashlib.md5()
						m.update(word.strip())
						ciphertext = m.hexdigest()
						if ciphertext.strip() == password.strip():
							print "[+] Found password: %s" % word
							found = True
				if not found:
					print "[-] Password for user '%s' not found in %s\n" % (username, args.wordlist) 
	else:
		if not os.path.isfile(args.passwordfile) and not os.path.isfile(args.wordlist):
			print "Neither %s nor %s exist." % (args.passwordfile, args.wordlist)
		elif not os.path.isfile(args.passwordfile):
			print "File %s does not exist." % args.passwordfile
		elif not os.path.isfile(args.wordlist):
			print "File %s does not exist." % args.wordlist
		exit(0)
main()