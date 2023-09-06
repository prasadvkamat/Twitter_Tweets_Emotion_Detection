import sqlite3
conn = sqlite3.connect("tweets.db")
print("opened database successfully")

conn.execute("CREATE TABLE adminlogin (ausername varchar,apassword varchar)")
conn.execute("CREATE TABLE tweet (utweet varchar)")
conn.execute("CREATE TABLE signup (uname varchar,uphone varchar,username varchar,upassword varchar)")
conn.execute("CREATE TABLE contact (uname varchar,uemail varchar,uphone Number, umessage varchar,uprasad varchar)")
print("table created successfully")
conn.close()
