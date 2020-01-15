from sys import platform
import functools
import subprocess

'''
This script shows a possible advantage of using decorator.
This also serves as a refresher for myself on how to use decorator.
A decorator changes an existing function without changing the existing function's code.
'''

# checks if the system is Linux or not.
def check_system(func):
    # preserve the original calling reference.
    @functools.wraps(func)
    def wrapper(*args):
        # run the function and produces the output if it is linux
        if platform == 'linux':
            return func(*args)
        else:
            # else return the below message.
            return "This is not linux".encode('utf-8')
    # ensure all is returned and not eaten by wrapper.
    return wrapper


@check_system
def linux_cmd(cmd):
    # capture output and send to stdout.
    # See https://docs.python.org/3/library/subprocess.html
    current_user = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    return current_user.stdout


if __name__ == '__main__':
    w = linux_cmd("id cyruslab")
    print(w.decode('utf-8'))