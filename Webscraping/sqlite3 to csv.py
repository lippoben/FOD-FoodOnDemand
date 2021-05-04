import sqlDatabaseManagement as sql
import pandas as pd


def dbToCSV(dbFileName, csvFileName):
    conn = sql.sqlInit(dbFileName)
    colNameArray = sql.sqlGetColNames(conn)

    colEntriesArray = []
    for colName in colNameArray:
        colEntries = sql.sqlGetCol(conn, colName)
        colEntriesArray.append(colEntries)

    d = {colNameArray[0]: colEntriesArray[0], colNameArray[1]: colEntriesArray[1], colNameArray[2]: colEntriesArray[2]
        , colNameArray[3]: colEntriesArray[3], colNameArray[4]: colEntriesArray[4],
         colNameArray[5]: colEntriesArray[5], colNameArray[6]: colEntriesArray[6]}

    CSVFileDF = pd.DataFrame(d)

    CSVFileDF.to_csv(csvFileName)
