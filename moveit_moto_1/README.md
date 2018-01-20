ay_tools
=====================
`ay_tools` is a container repository of ay_*.  Unlike git subtree and submodule, this repository simply contains sub repositories.

Usage
=====================

git_clone.sh
-------------------
Clone all sub-repositories.

```
./git_clone.sh user@server:ros_ws/ay_tool/
```

Note: `server:ros_ws/ay_tool/` should contain all sub repositories.

git_status.sh
-------------------
Check status of all sub repositories.

```
./git_status.sh
```

git_fetch.sh
-------------------
Fetch from remote in all sub repositories.

```
./git_fetch.sh origin
```

git_merge.sh
-------------------
Merge in all sub repositories.

```
./git_merge.sh origin/master
```

