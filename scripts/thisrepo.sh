#!/bin/sh

TARGET="$(pwd)"

python3 -m venv $TARGET/py37 ;
echo "export PATH=\"$TARGET/py37/bin:$PATH\"" >> ./.bashrc
echo "export CCC_ENV=$TARGET" >> ./.bashrc
ln -s -T $TARGET/devClonedCodeChecker.sh $TARGET/py37/bin/ccc
source ./.bashrc ;
python3 -m pip install -r $TARGET/requirements.txt ;

printf "\n\n\nThis script will make this environment the default one"
printf " (for testing)\n"
printf "The current install location is: $TARGET\n"
printf "This script assumes you are running \'./scripts/thisrepo.sh\'\n"
printf "from the top level of the repository you want to test"
printf "Please run \'source ./.bashrc\' to test this repository.\n\n"
printf "You should run that command ^^ every time you open a new terminal\n"
printf "or start a new development/testing session\n"
