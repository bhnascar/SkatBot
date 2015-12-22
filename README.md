SkatBot
============================
Final project for CS229. For a detailed description, please see [our project writeup] (http://cs229.stanford.edu/proj2014/Ivan%20Leung,%20Pedro%20Milani,%20Ben-han%20Sung,%20SkatBot.pdf).

Dependencies
------------
* Python 3.4.2 (https://www.python.org/download/releases/3.4.2/)
* Matlab R2011a or newer

Setup
-----
Edit line 6 of globals.py to point to the location of the Matlab executable:
```
mlab = Matlab(matlab='C:\\Program Files (x86)\\MATLAB\\R2011a Student\\bin\\matlab.exe')
```

Running
-------
On Windows, double-click "start_server.bat" or "start_client.bat".
On OS X, double-click "start_server.command" or "start_client.command".

Note that the start scripts are set up for local development. That means that it automatically uses the IP address of your computer. If you would like to run the Skat client with a Skat server on a different computer, you must edit the IP address in start_client.bat/command.

The default parameters are:
```
"-d" flag for debug (write to debug.txt instead of a log file)
"-b 2" flag to play against two bots instead of two human players
"-sa Matlab/PythonInterface/PredictSuitSoftmax.m" flag to specify suit prediction algorithm
"-ra Matlab/PythonInterface/PredictRankSoftmax.m" flag to specify rank prediction algorithm
```

Other notes
-----------
Updates for pymatbridge have only been tested on Windows 7. It has been patched to support Python 3.4.2 and deal with encoding errors due to Windows paths.
