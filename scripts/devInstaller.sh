#!/bin/sh

removerepo(){
  printf "Where is it? Please write absolute path.\n"
  printf "Here\'s an example, and also the default: $HOME/clonedcodechecker-mercurial\n"
  printf "If you cloned the repository with \'hg clone <the URL> clonedcodechecker-mercurial\'\n"
  printf "without changing directory, you want the default.\n"
  select yn in "Default: $HOME/clonedcodechecker-mercurial" "Somewhere else" "Cancel"; do
      case $yn in
          "Default: $HOME/clonedcodechecker-mercurial" ) rm -R $HOME/clonedcodechecker-mercurial ; break;;
          "Somewhere else" ) read -p "Absolute Path: " abspath ; rm -R $abspath ; break;;
          Cancel ) exit ;;
      esac
  done
}

printf "\n\n\nThis script will set up a dev environment\n"

mkdir -p $HOME/ccc_env ;
cd $HOME/ccc_env ;

printf "Do you want to be able to submit changes from here? (Requires a SourceForge account)"
select yn in "Yes" "No" ; do
  case $yn in
    Yes ) read -p "SourceForge Username: " username ; hg clone ssh://${username}@hg.code.sf.net/p/clonedcodechecker/mercurial clonedcodechecker-mercurial ; break ;;
    No ) hg clone http://hg.code.sf.net/p/clonedcodechecker/mercurial clonedcodechecker-mercurial ; break ;;
  esac
done

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

printf "Would you like to set up an ssh key?\n"
printf "This is optional. If you already have one (probably in $HOME/.ssh/),\n"
printf "you probably don\'t want to create another one. If you create one, you can\n"
printf "add it to your SourceForge account, and it'll stop prompting you for a password\n"
printf "when you pull new changes (hg pull ; hg update) or push your own changes\n"
printf "(hg commit -m \"<short message about what changed>\" ; hg push)\n"
select yn in "Yes" "No" "Cancel"; do
    case $yn in
        Yes ) ssh-keygen; break;;
        No ) echo "ok"; break;;
        Cancel ) exit ;;
    esac
done

printf "run \'jupyter lab --no-browser\' to start the ide (it runs in your browser)\n"
printf "Assuming you've forwarded port 8888 correctly, you should be able to visit\n"
printf "the URL that gets displayed when you run that command in your local browser.\n"
printf "if the URL displays a different port (8889 if 8888 is already taken) add an\n"
printf "additional port forward from 8889 to localhost:8889 (but don\'t remove the old one)\n"

#jupyter lab ;
