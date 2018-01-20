#!/bin/bash
#\file    git_fetch.sh
#\brief   Fetch from remote in all sub repositories.
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Nov.07, 2017

remote=$1
directories=$(cat _sub_repositories)

if [ "$remote" == "" ];then
  echo "Specify remote (e.g. origin)."
  exit 1
fi

for d in $directories; do
  echo "+++$d+++"
  echo "> cd $d"
  cd $d
  echo "> git fetch $remote"
  git fetch $remote
  cd ..
done
