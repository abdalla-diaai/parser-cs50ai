from parser import *
from nltk.tree import *

dp1 = Tree('dp', [Tree('d', ['the']), Tree('np', ['dog'])])
dp2 = Tree('dp', [Tree('d', ['the']), Tree('np', ['cat'])])
vp = Tree('vp', [Tree('v', ['chased']), dp2])
tree = Tree('s', [dp1, vp])

for subtree in tree.subtrees(filter = lambda t: t.height() == 2):
    print(subtree)
 