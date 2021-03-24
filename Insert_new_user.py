import sqlite3
import sys
from getopt import getopt

def main(argv):
    user = ''
    mhash = ''
    try:
        opts,args=getopt(argv,"u:h:")        
        for opt, arg in opts:
            if opt == '-u':
                user = arg
            elif opt == '-h':
                mhash = arg
        print("arguments digested")
        conn = sqlite3.connect('Kaffee.db')
        sql = '''UPDATE KAFFEELISTE\
        SET NAME = ?\
        WHERE HASH = ? ;'''
        conn.execute(sql,(user,mhash))
        print("Username assigend to hash")
        conn.commit()
        conn.close()

    except:
        print ('test.py -u <user> -h <hash>')
        sys.exit(2)



    

if __name__ == "__main__":
    main(sys.argv[1:])