#!/bin/bash
#\file    git_status.sh
#\brief   Check status of all sub repositories.
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Nov.07, 2017

directories=$(cat _sub_repositories)

for d in $directories; do
  echo "+++$d+++"
  echo "> cd $d"
  cd $d
  echo "> git status"
  git status
  cd ..
done

echo "+++this repository+++"
echo "> git status"
git status
