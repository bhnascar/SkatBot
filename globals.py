import collections

from pymatbridge import Matlab

Play = collections.namedtuple('Play', ['pid', 'card'])
mlab = Matlab(matlab='/Applications/MATLAB_R2011a.app/bin/matlab')