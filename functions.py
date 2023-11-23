import sqlite3 as sq

def CreateDB(naam):
    con = sq.connect(naam)
    cur = con.cursor
    con_cur = [con,cur]
    return con_cur