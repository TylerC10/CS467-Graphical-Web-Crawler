#### Pre-Requisites
###### OS
* Mac OSX/Linux/Windows

###### Softwares
* Python v2.7.x or above  
* Python PIP v8.0 or above  
* Postgres v9.5 or above  

Installation steps according to any given platform can be found easily on the web  
Verify your installation with commands `python --version` (expected is 2.7.x) and `pip --version` (expcted is 8.x or higher)

#### Set Up
1. Install OS dependencies, if any. ex. for Ubuntu, `sudo apt-get install python-dev libxml2-dev libxslt1-dev`  
2. Install external dependencies - `pip install -r requirements.txt`  
3. Start the Postgres server, if it isn't running already  
4. In a Postgres client, execute the file `db_init.sql` and make sure you have the required schema & tables created

###### If you want to use a Python Virtual Environment
1. Install Python Virtualenv - `pip install virtualenv`  
2. Open the terminal/command prompt and navigate to the script directory - `cd <DIR>`  
3. Create a virtual environment, well, if there is not one already. If you dont see a `env` directory already, execute- `virtualenv -p <PATH-TO-PYTHON2.7-EXECUTABLE> env`  
4. Activate the virtual environment - `source env/bin/activate`  
5. Install external dependencies - `pip install -r requirements.txt`  
6. Deactivate the virtual environment, after the script completes execution - `deactivate`  

Make sure all the above steps executed without any errors  

#### Execution
1. Open the terminal/command prompt  
2. Navigate to the script directory - `cd <DIR>`  
3. If using a Python Virutal Environment, activate the virtual environment - `source env/bin/activate`
4. Now execute the Example Python script - `python example.py` (see Section _Sample Script_ below)  
5. Upon successful execution you should see _PROCESSING_ logs on your console indicating what is being processed
6. If using a Python Virtual Environment, deactivate the virtual environment, after the script completes execution - `deactivate`

#### Sample Script
* If you want to test the persistence part of the code, before executing example.py , open it and make sure the DB config details are proper  
* This is a backend script, so, any developer who wishes to invoke the BFS/DFS crawl/search should invoke the code as shown in the file example.py  
* Each public method in the whole web-crawler code base is clearly documents (in Sphinx style). Developers can reference to the Python docs for further clarity
