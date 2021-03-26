import tests
import os
import sys
import unittest
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

project_name = os.path.basename(os.getcwd())

print("Starting Unit Tests...")


tests = subprocess.run(["py -m unittest"], capture_output=True, shell=True)

if tests.returncode != 0:
    print(tests.stdout)
    print("ABORTING PUSH!")
    sys.exit(1)

sys.exit(0)
