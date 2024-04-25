"""
    These tests verify that the same versions of Python and packages are installed on your computer as on recodex.
    You can turn these tests off but this may cause some errors due to incompatibilities which are hard to debug on recodex.
"""

import sys

if sys.version_info.major != 3 or sys.version_info.minor != 11:
    print("Python version 3.11 is required for testing since it is installed on ReCodEx. You are using Python version", sys.version)
    sys.exit()


import pkg_resources

with open("../requirements.txt") as f:
    installed = {d.project_name: d.version for d in pkg_resources.working_set}
    dependencies = [line.strip().split("==") for line in f if "==" in line]
    for package, version in dependencies:
        if not package in installed:
            print(f"Package {package} is required to be installed.")
            sys.exit()
        if version != installed[package]:
            print(f"Package {package} version {installed[package]} is installed but required version is {version}.")
            sys.exit()


"""
    This code tests determinism and portability of random number generators.
    If these tests fail, contact your teacher and write your operation system, versions of python and numpy, etc.
    You can turn off these tests since assignments work also with different random number generators, 
    but limits may differ (significantly).
"""

import numpy
import random

rng = numpy.random.default_rng(42)
assert [rng.random() for _ in range(5)] == [0.7739560485559633, 0.4388784397520523, 0.8585979199113825, 0.6973680290593639, 0.09417734788764953]
assert [rng.integers(1000000) for _ in range(5)] == [526478, 975622, 735752, 761139, 717477]
assert [rng.beta(1, 3) for _ in range(5)] == [0.05014086883548152, 0.2817671069441921, 0.4516645021220816, 0.0672174548533563, 0.42291529387311344]
assert [rng.gamma(1.1, 5) for _ in range(5)] == [3.1958255956841795, 2.489130034785006, 5.666142693548989, 6.045713496867781, 2.3151495783803098]
assert [rng.random() for _ in range(5)] == [0.3704597060348689, 0.4695558112758079, 0.1894713590842857, 0.12992150533547164, 0.47570492622593374]
rng = numpy.random.default_rng(rng.integers(numpy.iinfo(numpy.int64).max))
assert [rng.random() for _ in range(5)] == [0.05150646550151439, 0.1311545379699941, 0.43471542711857125, 0.5700228355179155, 0.6573906601071987]

rng = random.Random(123)
assert [rng.random() for _ in range(5)] == [0.052363598850944326, 0.08718667752263232, 0.4072417636703983, 0.10770023493843905, 0.9011988779516946]
rng = random.Random(rng.random())
assert [rng.random() for _ in range(5)] == [0.1535654669409675, 0.5114053063351236, 0.9471954752909987, 0.9625254384162786, 0.9526039615660795]
