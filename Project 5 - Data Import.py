#import libraries
import pyinputplus as pyip
import tkinter as tk
import tkinter.filedialog 
import re
import numpy as np
import pandas as pd
import xlrd

#using the tkinter module, allows users to select files
root = tk.Tk()
root.withdraw()
dataFile = tkinter.filedialog.askopenfilename(filetypes=[("Data files", "*.csv; *.xlsx; *.xls")])



#unused used code. left in for reference.
#decimal regex
#^(\d|-)?(\d|,)*\.?\d*$
#def maxColumnLen(col):
    #length = col.astype(str).map(len).max()
    #if length < 5:
        #datatype = "VARCHAR(5)"
    #elif 5 <= length < 10:
        #datatype = "VARCHAR(15)"
    #elif 10 <= length < 20:
        #datatype = "VARCHAR(25)"
    #elif 20 <= length < 50:
        #datatype = "VARCHAR(55)"
    #else:
        #datatype = "VARCHAR(255)"

#if a file has not been selected, it is given the value = "". a condidional statement will determine if it has been selected and run the rest of the script.
if dataFile != "":

    #user input that asks users to enter the database name and table name and stores those each in a corresponding variable.
    db = input("Database: ")
    table = input("Table Name: ")

    #writes the first part of the sql statement to a new sql file labeled by the input defined by the user. creates a table defined by the user in the previous prompt in a database defined by the user in the previous prompt
    create_table = "CREATE TABLE {0}.{1} (\n"
    file_name = "{0}_{1}.sql"
    f = open(file_name.format(db, table), "x")
    f.write(create_table.format(db,table))

    #checks the file type of the data file. And reads the file. variable df2 is then created to tabulate the data that has been read.
    if dataFile.endswith(".csv"):
        df = pd.read_csv(dataFile, low_memory=False, encoding_errors="ignore")
    elif dataFile.endswith(".xlsx"):
        df = pd.read_excel(dataFile, index_col=None)
    elif dataFile.endswith(".xls"):
        df = pd.read_excel(dataFile, index_col=None)

    df2 = pd.DataFrame(df)

    #initiates for loop that parses through each column in the df2 table. stores column name in column_name variable. adds a new variable making the column name lower case, removes special characters, and camelcases column names that contain spaces
    for col in df2:
        column_name = df2[col].name
        new_column_name = column_name.replace(".","").replace("#","").replace("!","").replace("$","").replace("%","").replace("&","").replace("'","").replace("(","").replace(")","").replace("*","").replace("+","").replace(",","").replace("-","").replace("/","").replace(":","").replace(";","").replace("<","").replace(">","").replace("=","").replace("?","").replace("@","").replace("[","").replace("]","").replace("^","").replace("{","").replace("}","").replace("|","").replace("~","").replace("\\","").replace('"','')
        lowerCaseName = new_column_name.lower()
        new4_column_name = "`" + new_column_name + "`"
        splitx = new4_column_name.split(" ")
        corrected_name = splitx[0] + ''.join(ele.title() for ele in splitx[1:])


        #checks to see if the datatype of the column is "float64"
        #if a column is completely null, then the datatype variable becomes VARCHAR(255)
        #if a column contain no null values, then at least one of the values in the column is a decimal, in which case the datatype variable becomes DECIMAL(14,5) unless the column contains values with a large max character length
        #if a column name is "Quantity" or "Qty", then the datatype variable becomes SMALLINT(6)
        #if a column name references a column typically containing common numeric values, the datatype variable becomes DECIMAL(14,5)
        if df2[col].dtype == "float64":
            if df2[col].isnull().all():
                datatype = "VARCHAR(255)"
            elif df2[col].notnull().all():
                rounded_value = np.round(df2[col])
                length = rounded_value.astype(str).map(len).max()
                r = re.compile(r'^(\d|-)?(\d|,)*\.?\d*$')
                regmatch = np.vectorize(lambda x: bool(r.match(x)))
                list2 = regmatch(list([str(row) for row in df2[col]]))
                if "quantity" in lowerCaseName:
                    datatype = "SMALLINT(6)"
                elif "qty" in lowerCaseName:
                    datatype = "SMALLINT(6)"
                elif "zip" in lowerCaseName:
                    datatype = "VARCHAR(15)"
                elif "amount" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("rate"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("rate"):
                    datatype = "DECIMAL(14,5)"
                elif "variance" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("net"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("gross"):
                    datatype = "DECIMAL(14,5)"
                elif "difference" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "percentage" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "pct" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "total" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("price"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("sales"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("revenue"):
                    datatype = "DECIMAL(14,5)" 
                     

                #added to deal with potential numbers in scientific notation in order to keep it in it's exact format.
                #if the values all pass a regex that checks if the value is a real number then it checks the max length of the values rounded to the nearest hundredth. if it's smaller than 15, then the datatype becomes decimal, else the datatype varies depending on the max length of the values (will be a function)
                elif all(regmatch(list([str(row) for row in df2[col]]))) == True:
                    if length < 15:
                        datatype = "DECIMAL(14,5)"
                    else:
                        if length < 5:
                            datatype = "VARCHAR(5)"
                        elif 5 <= length < 10:
                            datatype = "VARCHAR(15)"
                        elif 10 <= length < 20:
                            datatype = "VARCHAR(25)"
                        elif 20 <= length < 50:
                            datatype = "VARCHAR(55)"
                        else:
                            datatype = "VARCHAR(255)"

                #if the data doesn't match any of the above criteria, the datatype varies depending on the max length of the values (will be a function)        
                else:
                    if 15 <= length < 20:
                        datatype = "VARCHAR(25)"
                    elif 20 <= length < 50:
                        datatype = "VARCHAR(55)"
                    else:
                        datatype = "VARCHAR(255)"

            #if a column name ends with "id" or "code", the datatype varies depending on the max length of the values (will be a function)
            #if a column name is "Quantity" or "Qty", then the datatype variable becomes SMALLINT(6)
            #if a column name references a column typically containing common numeric values, the datatype variable becomes DECIMAL(14,5)
            #if any of the values pass a regex that checks if the value is a real number, then the datatype variable becomes DECIMAL(14,5)
            #else the datatype varies depending on the max length of the values (will be a function)
            else:
                length = df2[col].astype(str).map(len).max()
                r = re.compile(r'^(\d|-)?(\d|,)*\.?\d*$')
                regmatch = np.vectorize(lambda x: bool(r.match(x)))
                if lowerCaseName.endswith("id"):
                    if length < 5:
                        datatype = "VARCHAR(5)"
                    elif 5 <= length < 10:
                        datatype = "VARCHAR(15)"
                    elif 10 <= length < 20:
                        datatype = "VARCHAR(25)"
                    elif 20 <= length < 50:
                        datatype = "VARCHAR(55)"
                    else:
                        datatype = "VARCHAR(255)"
                elif lowerCaseName.endswith("code"):
                    if length < 5:
                        datatype = "VARCHAR(5)"
                    elif 5 <= length < 10:
                        datatype = "VARCHAR(15)"
                    elif 10 <= length < 20:
                        datatype = "VARCHAR(25)"
                    elif 20 <= length < 50:
                        datatype = "VARCHAR(55)"
                    else:
                        datatype = "VARCHAR(255)"
                elif lowerCaseName.endswith("no"):
                    if length < 5:
                        datatype = "VARCHAR(5)"
                    elif 5 <= length < 10:
                        datatype = "VARCHAR(15)"
                    elif 10 <= length < 20:
                        datatype = "VARCHAR(25)"
                    elif 20 <= length < 50:
                        datatype = "VARCHAR(55)"
                    else:
                        datatype = "VARCHAR(255)"
                elif lowerCaseName.endswith("number"):
                    if length < 5:
                        datatype = "VARCHAR(5)"
                    elif 5 <= length < 10:
                        datatype = "VARCHAR(15)"
                    elif 10 <= length < 20:
                        datatype = "VARCHAR(25)"
                    elif 20 <= length < 50:
                        datatype = "VARCHAR(55)"
                    else:
                        datatype = "VARCHAR(255)"
                elif "quantity" in lowerCaseName:
                    datatype = "SMALLINT(6)"
                elif "qty" in lowerCaseName:
                    datatype = "SMALLINT(6)"
                elif "zip" in lowerCaseName:
                    datatype = "VARCHAR(15)"
                elif "amount" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("rate"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("rate"):
                    datatype = "DECIMAL(14,5)"
                elif "variance" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("net"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.startswith("gross"):
                    datatype = "DECIMAL(14,5)"
                elif "difference" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "percentage" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "pct" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif "total" in lowerCaseName:
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("price"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("sales"):
                    datatype = "DECIMAL(14,5)"
                elif lowerCaseName.endswith("revenue"):
                    datatype = "DECIMAL(14,5)"  
                elif any(regmatch(list([str(row) for row in df2[col]]))) == True :
                    datatype = "DECIMAL(14,5)"
                elif length < 5:
                    datatype = "VARCHAR(5)"
                elif 5 <= length < 10:
                    datatype = "VARCHAR(15)"
                elif 10 <= length < 20:
                    datatype = "VARCHAR(25)"
                elif 20 <= length < 50:
                    datatype = "VARCHAR(55)"
                else:
                    datatype = "VARCHAR(255)"

        #checks to see if the datatype of the column is "int64"
        #if a column name is "Quantity" or "Qty", then the datatype variable becomes SMALLINT(6)
        #if a column name references a column typically containing common numeric values, the datatype variable becomes DECIMAL(14,5)
        #else the datatype varies depending on the max length of the values (will be a function)
        elif df2[col].dtype == "int64":
            if "quantity" in lowerCaseName:
                datatype = "SMALLINT(6)"
            elif "qty" in lowerCaseName:
                datatype = "SMALLINT(6)"
            elif "zip" in lowerCaseName:
                datatype = "VARCHAR(15)"
            elif "amount" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.startswith("rate"):
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.endswith("rate"):
                datatype = "DECIMAL(14,5)"
            elif "variance" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.startswith("net"):
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.startswith("gross"):
                datatype = "DECIMAL(14,5)"
            elif "difference" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif "percentage" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif "pct" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif "total" in lowerCaseName:
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.endswith("price"):
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.endswith("sales"):
                datatype = "DECIMAL(14,5)"
            elif lowerCaseName.endswith("revenue"):
                    datatype = "DECIMAL(14,5)"       
            else:
                length = df2[col].astype(str).map(len).max()
                if length < 5:
                    datatype = "VARCHAR(5)"
                elif 5 <= length < 10:
                    datatype = "VARCHAR(15)"
                elif 10 <= length < 20:
                    datatype = "VARCHAR(25)"
                elif 20 <= length < 50:
                    datatype = "VARCHAR(55)"
                else:
                    datatype = "VARCHAR(255)"
        
        #if a datatype is "bool" then the datatype variable becomes VARCHAR(10)
        elif df2[col].dtype == "bool":
            datatype = "VARCHAR(10)"
        
        #if a datatype is "datetime64[ns]" then the datatype variable becomes VARCHAR(20)
        elif df2[col].dtype == "datetime64[ns]":
            datatype = "VARCHAR(20)"

        #checks to see if the datatype of the column is "object"
        #if a column name is "City", "County", "State", "PostalCode", "Plus4", or "Country", then the datatype variable becomes VARCHAR(55),(55),(25),(15),(5),(25) respectively
        #else the datatype varies depending on the max length of the values (will be a function)
        elif df2[col].dtype == "object":
            if "city" in lowerCaseName:
                datatype = "VARCHAR(55)"
            elif "county" in lowerCaseName:
                datatype = "VARCHAR(55)"
            elif "state" in lowerCaseName:
                datatype = "VARCHAR(25)"
            elif "postal" in lowerCaseName:
                datatype = "VARCHAR(15)"
            elif "zip" in lowerCaseName:
                datatype = "VARCHAR(15)"
            elif "plus4" in lowerCaseName:
                datatype = "VARCHAR(5)"
            elif "country" in lowerCaseName:
                datatype = "VARCHAR(25)"
            else:
                length = df2[col].astype(str).map(len).max()
                if length < 5:
                    datatype = "VARCHAR(5)"
                elif 5 <= length < 10:
                    datatype = "VARCHAR(15)"
                elif 10 <= length < 20:
                    datatype = "VARCHAR(25)"
                elif 20 <= length < 50:
                    datatype = "VARCHAR(55)"
                else:
                    datatype = "VARCHAR(255)"
        else:

            #VARCHAR(255) returns if a column meets none of the above criteria
            datatype = "VARCHAR(255)"

        #writes the corrected_name and datatype variables to new sql file
        add_column = "{0} {1} DEFAULT NULL,\n"
        f.write(add_column.format(corrected_name, datatype))

    #writes the finle parts of the sql statment to the sql file. prints a statement to notify the user that the script is complete.
    statement_end = "id INT(11) NOT NULL AUTO_INCREMENT,\nPRIMARY KEY (id))"
    f.write(statement_end.format(db,table))
    f.close()

    print(file_name.format(db,table),"has been created.")

#if the dataFile variable is empty meaning no file was selected, then the script notifies the user.
else:
    print("No file selected.")