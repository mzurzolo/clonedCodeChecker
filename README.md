[![Build Status](https://travis-ci.org/mzurzolo/clonedCodeChecker.svg?branch=master)](https://travis-ci.org/mzurzolo/clonedCodeChecker)
[![codecov](https://codecov.io/gh/mzurzolo/clonedCodeChecker/branch/master/graph/badge.svg)](https://codecov.io/gh/mzurzolo/clonedCodeChecker)
[![GitHub](https://img.shields.io/github/license/mzurzolo/clonedCodeChecker.svg)](https://github.com/mzurzolo/clonedCodeChecker/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# Installing with a network connection:

## The easiest install method assumes internet connection.

### Steps:

1. Get the project: `git clone https://github.com/mzurzolo/clonedCodeChecker.git`
2. cd into the project `cd clonedCodeChecker`

    2.1 __Easily-removable, python-only install:__

      *You will not be able to use the eclipse plugin, and this step will need to be repeated for every new terminal you open.*

    `source scripts/work_here.sh`

    2.2 __Full install, including eclipse plugin:__

        `python setup.py install --user

         mvn -f clonedcodecheckerplugin package`

    Now you need to copy the generated package to the *dropins* directory of your eclipse install. Assuming eclipse is installed in *eclipse* under the *home* directory, the command `cp clonedcodecheckerplugin/target/clonedcodechecker-1.0.0-SNAPSHOT.jar $HOME/eclipse/dropins/` should do it. Users can also use a file explorer.



# Offline install:

## Avoid using this method. It's old. Will be updated shortly.
  Zipped Distributions (for offline install) can be found under RELEASES.
  Unzip, cd to the extracted folder, and run the following command:

python3 -m pip install --user --no-index --find-links=./ clonedcodechecker
