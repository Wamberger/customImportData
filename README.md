# Custom import data

The program/script is part of software program, but it's modified and is standalone executable in test run. 
However, to use DB (database) or the 'commented' functions you will need some additional coding.

# How to run
Write in terminal:

      python3 run.py ./test.csv 
   or 
      
      python3.9 run.py ./test.csv
  
# Requirements

    You need python 3.9 or higher version.
 
# Description

  The data from file will be read and modified according to the properties.
    From the modified data the classes as a copy of the DB (database) tables will be created.
    The properties for the creation of any db table is defined in a dictionary.
    After validation and initialisation the tables will be updated or inserted into the DB.
    Some tables are update/inserted via REST-API. 
    
  Due to modification the properties (prop) are in the file: prop.py, and any process with the DB 
    will not take place - you will need own code for this.

# Additional information

   Once you run the program. You can look at log file (logFile.log) which process would hapen if there would not be in test run. In output file (output.txt) you have the information about the data which would be inserted with their DB table names.
