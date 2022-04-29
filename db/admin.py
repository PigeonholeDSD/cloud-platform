import sqlite3

from db.__config import ADMIN

USERNAME='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
PASSWORD='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '

con=sqlite3.connect(ADMIN,check_same_thread=False)
cur=con.cursor()
cur.execute('create table if not exists admin(username varchar(64) primary key,email varchar(1024),password varchar(1024))')
con.commit()

def add(username:str,password:str)->bool:
    cur.execute('select 1 from admin where username=?',(username,))
    s=cur.fetchone()
    if s:
        return False

    if not username:
        raise ValueError('username is empty')
    if not password:
        raise ValueError('password is empty')
    if len(username)>40:
        raise ValueError('username is too long')
    if len(password)>40:
        raise ValueError('password is too long')
    if not all(c in USERNAME for c in username):
        raise ValueError('username contains invalid characters')
    if not all(c in PASSWORD for c in password):
        raise ValueError('password contains invalid characters')

    cur.execute('insert into admin(username,email,password) values(?,?,?)',(username,None,password))
    con.commit()
    return True

add('testadmin','testpwd114514@')

def check(username:str,password:str)->bool:
    cur.execute('select password from admin where username=?',(username,))
    s=cur.fetchone()
    if not s or s[0]!=password:
        return False
    else:
        return True

def remove(username:str)->None:
    cur.execute('delete from admin where username=?',(username,))
    con.commit()
