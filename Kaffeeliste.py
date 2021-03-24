import sqlite3
from board import SCL, SDA
import busio, sys, logging, hashlib, base58check
import adafruit_ssd1306
from RPi import GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
from ky040.KY040 import KY040

# Define your pins
CLOCKPIN, DATAPIN, SWITCHPIN = 22, 23, 24

logging.basicConfig(filename='Kaffee.log', level=logging.DEBUG)

i2c = busio.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
reader = SimpleMFRC522()

# Callback for rotary change
def rotaryChange(direction):
    global names, i_name
    maxnum = len(names)
    if direction==1:
        i_name=(i_name+1)%maxnum
    else:
        i_name=(i_name-1)%maxnum
    oled_print(names[i_name])
    print("turned - " + str(direction))

# Callback for switch button pressed
def switchPressed():
    results, conn = query_db()
    name,db_id,coffees = search_by_name(results,names[i_name])
    update_count(conn, coffees+1, db_id)
    print("button pressed")

def oled_print(text,size=2):
    if size==2:
        y_offset = 12
    else:
        y_offset = 10
    oled.fill(0)
    oled.text(text,0,y_offset,color='WHITE', size=size)
    oled.show()

def search_by_hash(results, mhash):
    for r in results:
        if r['hash'] == mhash:
            print("Hash found")
            logging.info(r['id'],r['name'],r['coffees'])
            return r['name'], r['id'],r['coffees']
    return None, None, 0

def search_by_name(results, name):
    for r in results:
        if r['name'] == name:
            print("Name found")
            logging.info(r['id'],r['name'],r['coffees'])
            return r['name'], r['id'],r['coffees']
    return None, None, 0

def query_db():
    conn = sqlite3.connect('Kaffee.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * from KAFFEELISTE")
    results = cursor.fetchall()    
    return results,conn

def update_count(conn, new_count, db_id):
    logging.info("Starting update count")
    sql = ''' UPDATE KAFFEELISTE\
              SET COFFEES = ?\
              WHERE ID = ?'''
    logging.info(sql)
    entries = (new_count, db_id)
    logging.info(entries)
    cur = conn.cursor() 
    logging.info("Using connection")  
    cur.execute(sql, entries)
    logging.info("Execution done")
    conn.commit()    
    print("Count updated: ",new_count)

def create_new_key(conn,mhash):
    sql =   "INSERT INTO Kaffeeliste (HASH, COFFEES) \
            VALUES ( ? , 1 )"
    cur = conn.cursor()
    cur.execute(sql, (mhash,))
    conn.commit()    
    print("New Hash entered into DB")

def main():

    # Create a KY040 and start it
    ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChange, switchPressed)
    ky040.start()
    print("started KY040")
    global names,i_name
    names  = []
    i_name = 0
    try:
        while True:
            rows,_=query_db()
            for r in rows:
                name = r['name']
                if name != None:
                    names.append(name)

            print("Hold a tag near the reader")            
            id, text = reader.read()
            print("ID: %s" % (id))
            id_hash=hashlib.md5(str(id).encode()).digest()
            hash_str = base58check.b58encode(id_hash).decode().upper()[:6]
            print("Hash String: %s" % (hash_str))
            results, conn = query_db()
            registered, db_id, coffees = search_by_hash(results,hash_str)
            
            print(registered,": ",coffees)

            if not db_id:
                print("Not registered")                
                try:
                    create_new_key(conn,hash_str)
                    oled_print(hash_str,size=3)                   

                except:
                    print("Failed to insert new hash into DB")
                    oled_print("DB w ERROR", size=3)                                   
                sleep(10)

            else:
                print("Updating count")                
                new_count = coffees+1
                try:
                    logging.info("Trying...")
                    update_count(conn, new_count, db_id)
                    logging.info("Count updated in main")
                    if not registered:
                        registered = "Unknown"
                        oled_print(hash_str,size=3)
                        sleep(5)    
                    dname = registered
                    while len(dname)>11:                   
                        oled_print(dname,size=2)
                        sleep(0.3)
                        dname = dname[1:]
                    sleep(2)
                    s_count = str(new_count)+" Kaffees"    
                    oled_print(s_count,size=2)
                except:
                    logging.error("Unsuccessful in updating count")
                    oled_print("DB up Error!",size=2)
                    sleep(3)
                oled_print(registered,size=2)                

    except KeyboardInterrupt:
        logging.error("Keyboard Interrupt handling")
        ky040.stop()
        GPIO.cleanup()
        

if __name__ == "__main__":
    main()