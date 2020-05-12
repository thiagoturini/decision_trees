# config.py

from pathlib import Path, PureWindowsPath

filename = Path("C:/Users/Elizabeth/Documents/GitHub/DecisionTreeAlgorithm/data/iris.data")

# Convert path to Windows format
data_path = PureWindowsPath(filename)
data_windows = PureWindowsPath(filename)

path = "C:/Users/Elizabeth/Documents/GitHub/DecisionTreeAlgorithm/data/iris.data"

#data_dir = Path('C:/Users/Elizabeth/Documents/GitHub/DecisionTreeAlgorithm/data')
#data_path = data_dir / 'iris.data' 

#customer_db_url = 'sql:///customer/db/url'
#purchases_db_url = 'sql:///purchases/db/url'