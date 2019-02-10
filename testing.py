import os
from src.main import main

if __name__ == "__main__":
    base_path = 'test/good2/'
    names = []
    for f in (os.listdir(base_path)):
        if f[-4:] == '.lat':
            names.append(f[:-4])
    names.sort()
    print(names)
    failed_tests = []
    for name in names:
        try: main(['main', f'{base_path}{name}.lat'], 'llvm')
        except:
            pass
        os.system(f'lli {base_path}{name}.bc > {base_path}{name}.output2')
        out = open(f'{base_path}{name}.output').read()
        my_out = open(f'{base_path}{name}.output2').read()
        if out != my_out:
            failed_tests.append((name, out, my_out))

    print(f'\n===== Falied tests:')
    for test, out, out2 in failed_tests:
        print(f'Name: {test}')
        print('=== Original out:')
        print(out)
        print('=== My out:')
        print(out2)
    print(f'{len(failed_tests)} failed tests')
