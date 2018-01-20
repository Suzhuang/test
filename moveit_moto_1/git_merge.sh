#!/bin/bash
#\file    git_merge.sh
#\brief   Merge in all sub repositories.  For safety, fast-forward option is added.
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Nov.07, 2017

commit=$1
directories=$(cat _sub_repositories)

if [ "$commit" == "" ];then
  echo "Specify commit (e.g. origin/master)."
  exit 1
fi

for d in $directories; do
  echo "+++$d+++"
  echo "> cd $d"
  cd $d
  echo "> git merge --ff-only $commit"
  git merge --ff-only $commit
  cd ..
done
