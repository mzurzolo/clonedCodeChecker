[![Build Status](https://travis-ci.org/mzurzolo/clonedCodeChecker.svg?branch=master)](https://travis-ci.org/mzurzolo/clonedCodeChecker)
[![codecov](https://codecov.io/gh/mzurzolo/clonedCodeChecker/branch/master/graph/badge.svg)](https://codecov.io/gh/mzurzolo/clonedCodeChecker)
[![GitHub](https://img.shields.io/github/license/mzurzolo/clonedCodeChecker.svg)](https://github.com/mzurzolo/clonedCodeChecker/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Locally-hosted docs:
[DOCS](http://htmlpreview.github.io/?https://github.com/mzurzolo/clonedCodeChecker/blob/master/html/clonedcodechecker/index.html)

# Installing from source with a network connection:

## The easiest install method assumes internet connection.

### Steps:

#### 1. Get the project:
`git clone https://github.com/mzurzolo/clonedCodeChecker.git`
#### 2. cd into the project:
`cd clonedCodeChecker`

##### 2.1 _Full install, including eclipse plugin:_
  for python: `python36 setup.py install --user`

  *or*

  for python: `python3 setup.py install --user`

  for eclipse: `mvn -f clonedcodecheckerplugin package`

Now you need to copy the generated package to the *dropins* directory of your eclipse install. Assuming eclipse is installed in *eclipse* under the *home* directory, the command:

`cp clonedcodecheckerplugin/target/clonedcodechecker-1.0.0-SNAPSHOT.jar $HOME/eclipse/dropins/`

should do it. Users can also use a file explorer.


##### 2.2 _Easily-removable, python-only install:_

  *You will not be able to use the eclipse plugin, and this step will need to be repeated for every new terminal you open.*

  python only: `source scripts/work_here.sh`


# Online install (pre-compiled):

Zipped Distributions can be found under RELEASES.

#### 1. Download the tarball found in RELEASES.

#### 2. Unzip: `tar -xzvf ccc.lastest.tar.gz`

#### 3. Install the python package:
`python36 -m pip install clonedcodechecker --user --find-links=ccc.latest/`

  *or*

`python3 -m pip install clonedcodechecker --user --find-links=ccc.latest/`

#### 4. Eclipse Install:
*you must know where your eclipse/dropins/ directory is*

`cp ccc.latest/clonedcodechecker-1.0.0-SNAPSHOT.jar <ABSOLUTE/PATH/TO>/eclipse/dropins/`

*you may need sudo:*

`sudo cp ccc.latest/clonedcodechecker-1.0.0-SNAPSHOT.jar <ABSOLUTE/PATH/TO>/eclipse/dropins/`
