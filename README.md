# cracking-tools
A collection of cracking tools (mainly written in Python).

#### zipAttack.py
USAGE: `zipAttack.py -f <FILENAME> -w <WORDLIST> [-h] [-v]` <br />
FILENAME: a zip file <br />
WORDLIST: the word list used to attack the zip file with <br />
-v: verbose mode (reports which password it's attempting to crack the zip file with)

<hr>

#### md5HashCrack.py
USAGE : `md5HashCrack.py <FILENAME> <WORDLIST> [-h] [-v]` <br />
FILENAME: the file containing newline-separated MD5 hashes <br />
WORDLIST: the word list containing newline-separated cleartext <br />
-v, --verbose: run in verbose mode (output the cleartext being encrypted and compared with the current hash)

<hr>

#### bruteForcer.py
USAGE: `bruteForcer.py <NOOFCHARACTERS> <CHARACTERSET> <ZIPFILE> [-h] [-v]` <br />
NOOFCHARACTERS: The number of characters in the password. If unknown, enter -1; this will test every combination of one character, then every combination of two characters, then three, etc. Be careful, this can easily start an infinite loop with an incorrect character set. <br />
CHARACTERSET: The character set(s) to use. Use A to test upper case letters, a to test lower case letters, n to test numbers and s to test special characters. You can use any combination of A, a, n and s, e.g. A, s, sa, Aans, snaA, etc. <br />
ZIPFILE: The zip file we are trying to crack. <br />
-v, --verbose: verbose mode (outputs word being attempted).
