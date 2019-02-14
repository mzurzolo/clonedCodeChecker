#!/bin/sh

removerepo(){
  printf "Where is it? Please write absolute path.\n"
  printf "Here\'s an example, and also the default: $HOME/clonedcodechecker-mercurial\n"
  select yn in "Default: $HOME/clonedcodechecker-mercurial" "Somewhere else" "Cancel"; do
      case $yn in
          "Default: $HOME/clonedcodechecker-mercurial" ) rm -R $HOME/clonedcodechecker-mercurial ; break;;
          "Somewhere else" ) read -p "Absolute Path: " abspath ; rm -R $abspath ; break;;
          Cancel ) exit ;;
      esac
  done
}

printf "\n\n\nThis script will set up a dev environment\n"

echo "Would you like to set up an ssh key?"
echo "This is optional. If you already have one (probably in $HOME/.ssh/),"
echo "you probably don't want to create another one. To quit environment setup"
echo "select option 3"
select yn in "Yes" "No" "Cancel"; do
    case $yn in
        Yes ) ssh-keygen; break;;
        No ) echo "ok"; break;;
        Cancel ) exit ;;
    esac
done

read -p "SourceForge Username: " username

mkdir -p $HOME/ccc_env ;
cd $HOME/ccc_env ;

hg clone ssh://${username}@hg.code.sf.net/p/clonedcodechecker/mercurial clonedcodechecker-mercurial ;

printf "Would you like to download C source code for testing?\n"
select yn in "Yes" "No" ; do
    case $yn in
        Yes ) git clone --depth 1 https://github.com/torvalds/linux.git ; break;;
        No ) echo "ok"; break;;
    esac
done

python3 -m venv py37 ;
echo "export PATH=\"$HOME/ccc_env/py37/bin:$PATH\"" >> $HOME/.bashrc
source $HOME/.bashrc ;
python3 -m pip install -r $HOME/ccc_env/clonedcodechecker-mercurial/scripts/requirements.txt ;

printf "\n\nDone! The repository you cloned to get this script can now be safely\n"
printf "removed. Would you like to do this now?\n"
select yn in "Yes" "No" ; do
    case $yn in
        Yes ) removerepo; break;;
        No ) echo "ok"; break;;
    esac
done

printf "run \'jupyter lab --no-browser\' to start the ide (it runs in your browser)\n"
printf "Assuming you've forwarded port 8888 correctly, you should be able to visit\n"
printf "the URL that gets displayed when you run that command in your local browser.\n"

#jupyter lab ;
