
import time
from brping import Ping1D

# maybe check conifidence later
def check_depth(goal, bound, depth):
    if depth > (goal + bound):
        return "D"
    if depth < (goal- bound):
        return "U"
    return

