import pymysql as pms

class QPFSQLDB:
    def __init__(self,host,user,password,stages,dbname,tablename,keepconnection):
        #Set up the connection and cursor
        self.connection = pms.connect(host = host,user = user,password = password)
        self.c = self.connection.cursor()
        self.dictc = self.connection.cursor(pms.cursors.DictCursor)

        """
            STAGES:
            
            0 only sets up the connection
            1 does the above + puts everything in an existing table called tablename (removing everything from tablename) in a db called dbname
            2 does the above + creates said table in an existing db called dbname
            3 does the above + creates a db to put it in called dbname
        """
        if stages <= 0:
            return

        if stages >= 3:
            self.c.execute("CREATE DATABASE " + dbname + "; USE " + dbname + ";")

        if stages == 1:
            self.c.execute("USE " + dbname + "; DROP TABLE " + tablename + ";")

        self.c.execute("USE " + dbname + "; " + "CREATE TABLE " + tablename + " ("
                        + "time datetime, "
                        + "moisture float, "
                        + "temperature float, "
                        + "light float, "
                        + "pump_on bool, "
                        + "light_on bool"
                        + "); CREATE UNIQUE INDEX idx_time ON " + tablename +  " (time);")

        if keepconnection == False:
            self.close()

    def execute(self,query):
        self.c.execute(query)
        self.connection.commit();

    def insert(self,table,data,rows=""):
        t = "INSERT INTO " + table + " "
        if rows != "": t += "(" + rows + ") "
        t += "VALUES (" + data + ");"

        self.execute(t);
        self.connection.commit();

    def update(self,table,moistureval,temperatureval,lightval,pumpstatus,lightstatus):
        self.insert(table, "NOW(), " + str(moistureval) + ", " + str(temperatureval) + ", " + str(lightval) + ", " + str(pumpstatus).upper() + ", " + str(lightstatus).upper(), "time, moisture, temperature, light, pump_on, light_on")

    def select(self,db,table,stuff):
        self.dictc.execute("USE " + db)
        self.dictc.execute("SELECT " + stuff + " FROM " + table)
        ret = ""
        for i in self.dictc:
            ret += str(i)
        return ret

    def use(self,db):
        self.c.execute("USE " + db)
        self.dictc.execute("USE " + db)

    def close(self):
        self.connection.close()

conn = QPFSQLDB("localhost","python","python",1,"testdb","testtable", True)
conn.update("testtable",2.3,2.4,2.5,True,False)
print(conn.select("testdb","testtable","*"))