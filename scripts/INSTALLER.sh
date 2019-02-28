#!/bin/sh

printf "\n\n\nThis script will install the cloned code checker\n"
printf "Suggested install location: any directory under $HOME\n"
printf "After successful installation, the command \"ccc -h\" will print the program\'s help\n"

TARGET="$(pwd)"

printf "The current install location is: $TARGET/ccc_env\n"

printf "Is this ok?\n"
select yn in "Yes" "Specify different install location" ; do
  case $yn in
    Yes ) TARGET="$TARGET/ccc_env" ; break ;;
    "Specify different install location" ) read -p "Install location: " TARGET ; TARGET="$TARGET/ccc_env" ; break ;;
  esac
done

mkdir -p $TARGET ;

hg clone http://hg.code.sf.net/p/clonedcodechecker/mercurial $TARGET/clonedcodechecker-mercurial

python3 -m venv $TARGET/py37 ;
echo "export PATH=\"$TARGET/py37/bin:$PATH\"" >> $HOME/.bashrc
echo "export CCC_ENV=$TARGET/clonedcodechecker-mercurial" >> $HOME/.bashrc
source $HOME/.bashrc ;
python3 -m pip install -r $TARGET/clonedcodechecker-mercurial/scripts/requirements.txt ;

ln -s -T $TARGET/clonedcodechecker-mercurial/runClonedCodeChecker.sh $TARGET/py37/bin/ccc

printf "Please run \'source \$HOME/.bashrc\' (or open a new terminal) to get started\n\n"
