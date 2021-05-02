import sqlite3


# creates a connection to a pre-existing database. If the database doesn't exist then create a new one.
def sqlInit(databaseName):
    connection = sqlite3.connect(databaseName)
    print("Opened database successfully")
    return connection


# close an existing connection
def sqlClose(databaseConn):
    databaseConn.close()


# permanently commits any changes made to the database.
def sqlCommit(databaseConn):
    databaseConn.commit()


# Create a new table within a database.
def sqlCreateTable(databaseConn):
    databaseConn.execute('''CREATE TABLE RECIPES
             (ID INT PRIMARY KEY     NOT NULL,
             URL            TEXT        NOT NULL,
             RECIPENAME         TEXT    NOT NULL,
             INGREDIENTS         TEXT     NOT NULL,
             CLEANINGREDIENTS    TEXT       ,
             METHOD             TEXT        NOT NULL,
             INFOTAGS           TEXT       NOT NULL);''')
    print("Table created successfully")


# update an entry within database given primary Key
def sqlUpdateEntry(databaseConn, colName, primaryKeyID, updateVal):
    updateStatement = 'UPDATE RECIPES ' \
                     'SET ' + colName + ' = \'' + str(updateVal) + '\'' \
                     'WHERE ID = ' + str(primaryKeyID) + ';'
    databaseConn.execute(updateStatement)
    # print('Successfully updated')


def sqlDeleteEntry(databaseConn, primaryKeyID):
    databaseConn.execute('DELETE FROM RECIPES WHERE ID = ' + str(primaryKeyID) + ';')
    print('Successfully deleted RecipeID: ' + str(primaryKeyID))


# add a new column to an existing table
def sqlAddColumn(databaseConn, colName, colType):
    databaseConn.execute('ALTER TABLE RECIPES ADD COLUMN ' + colName + ' ' + colType + ';')
    print('Column added successfully')


# print the entire database to console
def sqlPrintAll(databaseConn):
    cursor = databaseConn.execute("SELECT * from RECIPES")
    for row in cursor:
        print(row)


# returns the number of entries in the database
def sqlCount(databaseConn):
    cursor = databaseConn.execute('SELECT COUNT(*) FROM RECIPES;')
    for row in cursor:
        return row


# Returns an array of all the column names
def sqlGetColNames(databaseConn):
    cursor = databaseConn.execute('PRAGMA table_info(RECIPES);')
    colNameArray = []
    for row in cursor:
        colNameArray.append(row[1])

    return colNameArray


# Returns an array of all the entries in a specific column
def sqlGetCol(databaseConn, colName):
    cursor = databaseConn.execute('SELECT ' + str(colName) + ' FROM RECIPES')
    colEntries = []
    for row in cursor:
        colEntries.append(row[0])

    return colEntries


# prints one entry from given PrimaryID
def sqlGetSpecificID(databaseConn, colName, PriID):
    cursor = databaseConn.execute('SELECT ' + str(colName) + ' from RECIPES WHERE ID = ' + str(PriID) + ';')
    for row in cursor:
        return row


# insert a new record to the database
def sqlInsertRecords(databaseConn, PriID, URL, RECIPENAME, INGREDIENTS, CLEANINGREDIENTS, METHOD, INFOTAG):
    insertStatement = "INSERT INTO RECIPES (ID, URL, RECIPENAME, INGREDIENTS, CLEANINGREDIENTS, METHOD, INFOTAGS)  \
                      VALUES ("+str(PriID)+",\'"+str(URL)+"\',\'"+str(RECIPENAME)+"\',\'"+str(INGREDIENTS)+"\', \'"+str(CLEANINGREDIENTS)+"\' , \'"+str(METHOD)+"\',\'"+str(INFOTAG)+"\')"
    databaseConn.execute(insertStatement)
    # print("Records created successfully")


'''
# this is an example of how to create and insert stuff
# -----------------------------
conn = sqlInit("recipeDatabase.db")
# sqlCreateTable(conn)
# sqlInsertRecords(conn, 3, "chicky nuggys", "chicken")
# sqlAddColumn(conn, 'CLEANINGREDIENTS', 'TEXT')
# sqlPrintAll(conn)
print(sqlGetSpecificID(conn, 'INGREDIENTS', 2806))
sqlDeleteEntry(conn, 2806)
print(sqlGetSpecificID(conn, 'INGREDIENTS', 2806))
sqlCommit(conn)

sqlClose(conn)
'''
