#! /usr/bin/env python

import hashlib
import hashtable

def calc_hash(word,hash_alg='md5'):
    if hash_alg not in hashlib.algorithms:
        print ("%s isn't exists in 'hashlib'!" % hash_alg)
        return None

    hash_obj = hashlib.new(hash_alg)
    hash_obj.update(word.encode())
    return hash_obj.hexdigest()


htable = hashtable.hashtable('htable-main.db')

print
try:
    htable.createtable(hashlib.algorithms)
except:
    pass

print
try:
    with open('wordlist.txt','r') as file:
        line = file.readline()
	i = 1
        while line != None and i < 10:
	    if line == '\n' or line == ' ':
                line = file.readline()
                continue
	    line = (line.split(' ')[0]).split('\n')[0]
	    for alg in htable.hash_algs:
		hash_string = calc_hash(line,alg)
		if hash_string != None and len(hash_string) > 0:
		    htable.addentry(line,hash_string,alg)
	    print '(%d) added %s' % (i,line)
	    i += 1
	    line = file.readline()
except:
    htable.con.close()

print
for item in htable.con.execute('select * from hashlist order by wordid').fetchall():
    print (htable.con.execute('select word from wordlist where rowid=%d' \
		% item[len(item)-1]).fetchone()[0])
    print str(item[0:len(item)-1])
    print

htable.con.close()

