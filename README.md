# John the Ripper on Golem network
## Demo (Youtube)
[![Everything Is AWESOME](https://img.youtube.com/vi/d6UIb0i9ePI/0.jpg)](https://youtu.be/d6UIb0i9ePI "Everything Is AWESOME")
## Prerequisites
### Install yagna
```$ sh curl -sSf https://join.golem.network/as-requestor | bash -```
### Install python requirements
```sh
$ # Using python3.6+
$ source ~/your/virtual/env
$ pip install -r requirements.txt
```
### Build using docker
```sh
$ docker build -t golem-jtr:latest
```
### Build/push Golem vm
```sh
$ gvmkit-build golem-jtr:latest
$ gvmkit-build golem-jtr:latest --push
```
### Run yagna daemon
```sh
$ yagna service run
```
### Run JtR on Golem!
```sh
$ yagna app-key create requestor
$ yagna payment init -r
$ export YAGNA_APPKEY=<your-key>
$ python jtr.py
usage: jtr.py [-h] --password PASSWORD [--num_nodes NUM_NODES] [--timeout TIMEOUT]
jtr.py: error: the following arguments are required: --password/-p
```
#### Watch full steps on [Youtube](https://youtu.be/d6UIb0i9ePI)!

