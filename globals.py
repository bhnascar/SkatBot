import collections

from pymatbridge import Matlab

Play = collections.namedtuple('Play', ['pid', 'card'])
mlab = Matlab(matlab='C:\Program Files/ (x86)\MATLAB\R2011a/ Student\bin\matlab.exe')