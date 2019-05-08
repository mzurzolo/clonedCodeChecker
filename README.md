[![Build Status](https://travis-ci.org/mzurzolo/clonedCodeChecker.svg?branch=master)](https://travis-ci.org/mzurzolo/clonedCodeChecker)
[![codecov](https://codecov.io/gh/mzurzolo/clonedCodeChecker/branch/master/graph/badge.svg)](https://codecov.io/gh/mzurzolo/clonedCodeChecker)
[![GitHub](https://img.shields.io/github/license/mzurzolo/clonedCodeChecker.svg)](https://github.com/mzurzolo/clonedCodeChecker/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# Installing from source with a network connection:

## The easiest install method assumes internet connection.

### Steps:

1. __Get the project:__ `git clone https://github.com/mzurzolo/clonedCodeChecker.git`
2. cd into the project `cd clonedCodeChecker`

  2.1 __Full install, including eclipse plugin:__

      for python: `python setup.py install --user`

      for eclipse: `mvn -f clonedcodecheckerplugin package`

      Now you need to copy the generated package to the *dropins* directory of your eclipse install. Assuming eclipse is installed in *eclipse* under the *home* directory, the command `cp clonedcodecheckerplugin/target/clonedcodechecker-1.0.0-SNAPSHOT.jar $HOME/eclipse/dropins/` should do it. Users can also use a file explorer.


  2.2 __Easily-removable, python-only install:__

  *You will not be able to use the eclipse plugin, and this step will need to be repeated for every new terminal you open.*

  python only: `source scripts/work_here.sh`


# Online install (not from source):

  Zipped Distributions can be found under RELEASES.

  Unzip: `tar -xzvf ccc.lastest.tar.gz`

  python: `python3 -m pip install clonedcodechecker --user --find-links=ccc.latest/`

  **OR**

  python: `python36 -m pip install clonedcodechecker --user --find-links=ccc.latest/`

  eclipse: *you must know where your eclipse/dropins/ directory is*

  `cp ccc.latest/clonedcodechecker-1.0.0-SNAPSHOT.jar <ABSOLUTE/PATH/TO>/eclipse/dropins/`

  you may need sudo:

  `sudo cp ccc.latest/clonedcodechecker-1.0.0-SNAPSHOT.jar <ABSOLUTE/PATH/TO>/eclipse/dropins/`
