import sqlite3
import numpy as np


# creates a connection to a pre-existing database. If the database doesn't exist then create a new one.
def sqlInit(databaseName):
    connection = sqlite3.connect(databaseName)
    print("Opened database successfully\n")
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
    print("Table created successfully\n")


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
    print('Column added successfully\n')


# print the entire database to console
def sqlPrintAll(databaseConn):
    cursor = databaseConn.execute("SELECT * from RECIPES")
    for row in cursor:
        print(row)


# returns the number of entries in the database
def sqlCount(databaseConn):
    cursor = databaseConn.execute('SELECT COUNT(*) FROM RECIPES;')
    for row in cursor:
        return row[0]


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
        return row[0]


# insert a new record to the database
def sqlInsertRecords(databaseConn, PriID, URL, RECIPENAME, INGREDIENTS, CLEANINGREDIENTS, METHOD, INFOTAG):
    insertStatement = "INSERT INTO RECIPES (ID, URL, RECIPENAME, INGREDIENTS, CLEANINGREDIENTS, METHOD, INFOTAGS)  \
                      VALUES ("+str(PriID)+",\'"+str(URL)+"\',\'"+str(RECIPENAME)+"\',\'"+str(INGREDIENTS)+"\', \'"+str(CLEANINGREDIENTS)+"\' , \'"+str(METHOD)+"\',\'"+str(INFOTAG)+"\')"
    databaseConn.execute(insertStatement)
    # print("Records created successfully")


# returns an array of all the labeled vegan recipes
def sqlGetAllVeganRecipes(databaseConn):
    cursor = databaseConn.execute('SELECT ID FROM RECIPES WHERE INFOTAGS = \'Vegan\';')
    veganRecipeArray = []
    for row in cursor:
        veganRecipeArray.append(row[0])

    return veganRecipeArray


# returns an array of all the labeled non vegan recipes
def sqlGetAllNonVeganRecipes(databaseConn):
    cursor = databaseConn.execute('SELECT ID FROM RECIPES WHERE NOT INFOTAGS = \'Vegan\';')
    nonVeganRecipeArray = []
    for row in cursor:
        nonVeganRecipeArray.append(row[0])

    return nonVeganRecipeArray


# allows for a custom query to be made if a the functionality hasn't been added to this module yet
def sqlCustomQuery(databaseConn, query):
    cursor = databaseConn.execute(query)
    return cursor
