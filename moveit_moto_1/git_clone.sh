#!/bin/bash
#\file    git_clone.sh
#\brief   Clone all sub repositories.
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Nov.07, 2017

repository_prefix=$1
directories=$(cat _sub_repositories)

if [ "$repository_prefix" == "" ];then
  echo "Specify repository_prefix (e.g. user@server:ros_ws/ay_tool/)."
  exit 1
fi

for d in $directories; do
  echo "> git clone $repository_prefix$d"
  git clone $repository_prefix$d
done
