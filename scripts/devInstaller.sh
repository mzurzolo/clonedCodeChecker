#!/bin/sh

printf "\n\n\nThis script will set up a dev environment\n"

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

printf "Do you want to be able to submit changes from here? (Requires a SourceForge account)\n"
select yn in "Yes" "No" ; do
  case $yn in
    Yes ) read -p "SourceForge Username: " username ; hg clone ssh://${username}@hg.code.sf.net/p/clonedcodechecker/mercurial -r SPRINT1 $TARGET/clonedcodechecker-mercurial ; break ;;
    No ) hg clone http://hg.code.sf.net/p/clonedcodechecker/mercurial -r SPRINT1 $TARGET/clonedcodechecker-mercurial ; break ;;
  esac
done

printf "Would you like to download C source code for testing?\n"
select yn in "Yes" "No" ; do
    case $yn in
        Yes ) git clone --depth 1 https://github.com/torvalds/linux.git $TARGET/linux ; break;;
        No ) printf "ok\n"; break;;
    esac
done

python3 -m venv $TARGET/py37 ;
echo "export PATH=\"$TARGET/py37/bin:$PATH\"" >> $HOME/.bashrc
echo "export CCC_ENV=$TARGET" >> $HOME/.bashrc
ln -s -T $TARGET/clonedcodechecker-mercurial/runClonedCodeChecker.sh $TARGET/py37/bin/ccc
source $HOME/.bashrc ;
python3 -m pip install -r $TARGET/clonedcodechecker-mercurial/requirements.txt ;

printf "\n\nDone! The repository you cloned to get this script can now be safely removed with rm -R\n"
printf "Please run \'source \$HOME/.bashrc\' (or open a new terminal) to get started\n\n"

printf "run \'jupyter lab --no-browser\' to start the ide (it runs in your browser)\n"
printf "Assuming you've forwarded port 8888 correctly, you should be able to visit\n"
printf "the URL that gets displayed when you run that command in your local browser.\n"
printf "if the URL displays a different port (8889 if 8888 is already taken) add an\n"
printf "additional port forward from 8889 to localhost:8889 (but don\'t remove the old one)\n"
printf "You can use --port <portnum> to specify your preferred port.\n"

#jupyter lab ;
