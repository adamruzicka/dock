dock
====

Simple python library with command line interface for building docker images. It is written on top of [docker-py](https://github.com/docker/docker-py).

It supports several building modes:

 * building within a docker container using docker from host by mounting docker.sock inside container
 * building within a privileged docker container (new instance of docker is running inside)
 * building images in current environemt

## Installation

Clone this git repo and install it using python installer:

```bash
$ git clone https://github.com/DBuildService/dock.git
$ cd dock
$ sudo pip install .
```

## Usage

If you would like to build your images within containers, you need to obtain images for those containers. We call them build images. dock is installed inside and used to take care of build itself.

At some point, these will be available on docker hub, but right now, you need to build them yourself. Here's how:

```bash
$ dock create-build-image --dock-local-path ${PATH_TO_DOCK_GIT} ${PATH_TO_DOCK_GIT}/images/privileged-build privileged-buildroot
```

Why is it so long? Okay, let's get through. First thing is that dock needs to install itself inside the build image. You can pick several sources for dock: you local copy, (this) official upstream repo, your forked repo or even distribution tarball. In the example above, we are using our locally cloned git repo (`--dock-local-path ${PATH_TO_DOCK_GIT}`).

You have to provide dockerfile too. Luckily these are part of upstream repo (see folder images). It's the first argument: `${PATH_TO_DOCK_GIT}/images/privileged-build`.

And finally, you need to name the image: `privileged-buildroot`.


As soon as our build image is built, we can start building stuff in it:

```bash
$ dock build --method privileged --build-image privileged-buildroot --image test-image --git-url "github.com/TomasTomecek/docker-hello-world.git"
```

Bear in mind that you shouldn't mix build methods: if you use _hostdocker_ method with build image for _privileged_ method, it won't work.

## API

dock has proper python API. You can use it in your scripts or service without invoking shell:

```python
from dock.api import build_image_in_privileged_container
response = build_image_in_privileged_container(
    "privileged-buildroot",
    git_url="github.com/TomasTomecek/docker-hello-world.git",
    image="dock-test-image",
)
# response contains a lot of useful information: logs, information about images, plugin results
```

## RPM build

Install tito and mock:

```bash
dnf install tito mock
```

Build RPM locally:

```bash
# build from the latest tagged release
tito build --rpm
# or build from the latest commit
tito build --rpm --test
```

Build RPM using mock:

```bash
SRPM=`tito build --srpm --test | egrep -o '/tmp/tito/dock-.*\.src\.rpm'`
sudo mock -r fedora-21-x86_64 $SRPM
```

## Submit Build in Copr

First you need to set up rel-eng/releasers.conf:

```bash
sed "s/<USERNAME>/$USERNAME/" < rel-eng/releasers.conf.template > rel-eng/releasers.conf
```

Now you may submit build:

```bash
# submit build from latest commit
tito release copr-test
# or submit build from the latest tag
tito release copr
```

## TODO

* Enable managing repositories within built image (changing source of packages during build without dockerfile modification)
* Add support for different registries

