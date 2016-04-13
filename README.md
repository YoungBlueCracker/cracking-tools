# cracking-tools
A collection of cracking tools (mainly written in Python).

#### zipAttack.py
USAGE: `zipAttack.py -f <FILENAME> -w <WORDLIST> [-h] [-v]` <br />
FILENAME: a zip file <br />
WORDLIST: the word list used to attack the zip file with <br />
-v: verbose mode (reports which password it's attempting to crack the zip file with)

<hr />

#### md5HashCrack.py
USAGE : `md5HashCrack.py <FILENAME> <WORDLIST>` [-h] [-v] <br />
FILENAME: the file containing newline-separated MD5 hashes <br />
WORDLIST: the word list containing newline-separated cleartext <br />
-v, --verbose: run in verbose mode (output the cleartext being encrypted and compared with the current hash)
