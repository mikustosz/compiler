import os
import sys
from src.main import main

if __name__ == "__main__":
    base_path = 'test/good/'
    names = []
    for f in (os.listdir('test/good')):
        if f[-4:] == '.lat':
            names.append(f[:-4])
    names.sort()
    for name in names:
        main(['main', f'{base_path}{name}.lat'], "llvm")
        os.system(f'{base_path}{name}.bc')
