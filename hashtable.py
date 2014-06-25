import sqlite3

class hashtable(object):
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def commit(self):
        self.con.commit()

    def createtable(self,hash_algs=['md5']):
	print hash_algs
	self.hash_algs = hash_algs
        self.con.execute('create table wordlist(word)')
	hash_query = "create table hashlist("
	for alg in self.hash_algs:
            hash_query += alg+','
	hash_query += "wordid integer)"
	self.con.execute(hash_query)
        self.con.execute('create index hashwordidx on hashlist(wordid)')
	for alg in self.hash_algs:
	    self.con.execute('create index %s on hashlist(%s)' % (alg+'idx',alg))

    def getwordid(self, word):
        res = self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
        if res == None:
            cur = self.con.execute("insert into wordlist(word) values ('%s')" % word)
            return cur.lastrowid
        else:
            return res[0]

    def isexists(self,hash_value,hash_alg='md5'):
	if hash_alg not in self.hash_algs: return None
	h = self.con.execute("select wordid from hashlist where %s='%s'" \
		% (hash_alg,hash_value)).fetchone()
	if h != None:
	    w = self.con.execute("select * from wordlist where rowid='%d'" \
		% h[0]).fetchone()
	    if w != None:
	        return True
	return False

    def addentry(self, word, hash_value,hash_alg='md5'):
	if hash_alg not in self.hash_algs: return None
	if not self.isexists(hash_value,hash_alg):
	    wordid = self.getwordid(word)
	    #cur = self.con.execute("insert into hashlist(%s,wordid) values ('%s','%d')" \
			#% (hash_alg,hash_value,wordid))
	    u = self.con.execute('select * from hashlist where wordid=%d' % wordid).fetchone()
	    if u != None:
		cur = self.con.execute("update hashlist set %s='%s' where wordid=%d" \
			% (hash_alg,hash_value,wordid))
	    else:
		cur = self.con.execute("insert into hashlist(%s,wordid) values ('%s','%d')" \
			% (hash_alg,hash_value,wordid))
	    self.commit()
	    return cur.lastrowid
	return None

    def search(self, hash_value,hash_alg='md5'):
	if hash_alg not in self.hash_algs: return None
	wordid = self.con.execute("select wordid from hashlist where %s='%s'" \
			% (hash_alg,hash_value)).fetchone()[0]
	return self.con.execute("select word from wordlist where rowid='%d'" \
		% wordid).fetchone()[0]


