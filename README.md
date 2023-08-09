# Michael Waryoba Project Porfolio 
[Project 1 - Data Scraping of Covid-19 dataset using SQL](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%201%20-%20Covid-19%20SQL%20Queries.sql)
- Queried the likelihood of dying from Covid-19 from dataset of total cases and deaths
- Filtered out percentage of Covid-19 cases within United States population and highest infection rate between countries and continents
- Created view of percentage of population vaccinated to be used for [Tableau visualization](https://public.tableau.com/app/profile/michael.waryoba/viz/CovidDashboard_16514599746420/Dashboard1)

[Project 2 - Data Cleaning of Nashville Housing dataset using SQL](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%202%20-%20Data%20Cleaning%20with%20Nashville%20Housing%20data.sql)
- Standardized data format for clarity
- Populated null property address data with proper values
- Split address into individual columns to highlight street address, city, and state
- Removed duplicate rows and deleted columns that were not significant

[Project 3 - Data Correlation of Movie Industry dataset using Python](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%203%20-%20Movie%20Industry%20Correlation.ipynb)
- Created scatter plot of Budget vs Gross Earnings with line of regression
- Assigned numeric value for each unique categorical value and created two-dimensional heat map showing correlation coefficient
- Filtered out the correaltion coefficients that were higher than 0.5

[Project 4 - Sales Dashboard using Power BI](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%204%20-%20Sales%20Dashboard%20View.pdf)
- Created seperate views for the [sales dashboard](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%204%20-%20Sales%20Dashboard%20View.pdf) and [detialed table](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%204%20-%20Sales%20Detail%20View.pdf).
- Created key performance indicators for the sales, profit, quantity, and discount values.
- Included area and clustered column charts to display sales data over time. Effective in showing trends and patterns in data by emphasizing the cumulative value of a series of data points.

[Project 5 - Importing data into MySQL database using Python scirpt](https://github.com/michaelwaryoba/ProjectPorfolio/blob/main/Project%205%20-%20Data%20Import%20(Python))

This is a python script that parses through csv, xls,and xlsx files and determines the data types based on sql data types. After parsing the file, it then creates an SQL file that contains an SQL Statement that creates a table based on the datatypes that were determined. Here is a step-by-step process of how to run it: 

Step 1: In a teminal, run "python create_table_sql.py"

Step 2: A window pops up asking the user to select a csv, xls, or xlsx file. Select a file. If no file is selected the scripts ends.

Step 3: The user is prompted to enter the name of the database that the table will be made for. The user is prevented from entering blank data.

Step 4: The user is prompted to enter the name of the table that will will be created. The user is prevented from entering blank data.

Step 5: The file has been parsed, and a new sql file is created in the directory where the script was run from.

Step 6: Open the SQL file and execute the statement.

