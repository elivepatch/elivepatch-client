# elivepatch - Flexible Distributed Linux Kernel Live Patching

# Why?

* 3rd-party trust.
  * Trust on a third-party service can be eliminated by deploying Elivepatch in-house.
* Custom kernel configurations.
  * Live patches can be created for different kernel versions and configurations by varying the parameters to Elivepatch.
* Modified kernels.
  * Support is extended to locally modified kernels (e.g. out-of-tree patch sets) by sending the server a list of patches that should be applied before the live patch creation process starts.
* Client-generated patches.
  * In Elivepatch, clients specify the live patches to be created whereas current systems only support vendor-generated patches.
* Security auditing.
  * Elivepatch is completely open source and thus fully auditable. 

# How?

* [elivepatch-client](https://github.com/gentoo/elivepatch-client)
  * Client to be run on the machine where we want to install the live patch.
* [elivepatch-server](https://github.com/gentoo/elivepatch-server)
  * RESTful API to be run on the server using kpatch for building the live patch.
* [elivepatch-overlay](https://github.com/aliceinwire/elivepatch-overlay)
  * Where to keep you patches.

# User's guide

## Installing

### On Gentoo based distros:

#### client install

    emerge --ask sys-kernel/kpatch
    emerge --ask sys-apps/elivepatch-client

#### server install

    emerge --ask sys-kernel/kpatch
    emerge --ask sys-apps/elivepatch-server

### on Debian based distros:

#### client install

```
apt-get install git
apt-get install python3-pip

git clone  https://github.com/gentoo/elivepatch-client
cd elivepatch-client
pip3 install -r requirements.txt
PYTHONPATH=. python3 bin/elivepatch
```


### Install from source
#### client install

```
git clone  https://github.com/gentoo/elivepatch-client
cd elivepatch-client
pip3 install -r requirements.txt
PYTHONPATH=. python3 bin/elivepatch
```
#### server install

```
git clone  https://github.com/gentoo/elivepatch-server
cd elivepatch-server
pip3 install -r requirements.txt
PYTHONPATH=. python3 elivepatch_server/elivepatch-server
```
## Usage

### Use

#### Server start

    PYTHONPATH=. python3 elivepatch_server/elivepatch-server

#### Client start

    PYTHONPATH=. python3 bin/elivepatch

```
usage: elivepatch [-h] [-c FILE] [-e] [-p PATCH] [-k CONFIG]
                  [-a KERNEL_VERSION] [-l] [-u URL] [-d] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c FILE, --conf_file FILE
                        Specify config file
  -e, --cve             Check for secutiry problems in the kernel.
  -p PATCH, --patch PATCH
                        patch to convert.
  -k CONFIG, --config CONFIG
                        set kernel config file manually.
  -a KERNEL_VERSION, --kernel_version KERNEL_VERSION
                        set kernel version manually.
  -l, --clear           Clear the already installed cve db (Use with
                        caution!).
  -u URL, --url URL     set elivepatch server url.
  -d, --debug           set the debug option.
  -v, --version         show the version.
```
### Creating Live patch
Not all patch can be converted to live patch using kpatch.
* [Patch that change data structure](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#change-the-code-which-uses-the-data-structure)
* [Change content of existing variable](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#use-a-kpatch-load-hook)
* [Add field to existing data structure](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#use-a-shadow-variable)
* Init code changes are incompatible with kpatch
* [Header file changes](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#header-file-changes)
* [Dealing with unexpected changed functions](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#dealing-with-unexpected-changed-functions)
* [Removing references to static local variables](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#removing-references-to-static-local-variables)
* [Code removal](https://github.com/dynup/kpatch/blob/master/doc/patch-author-guide.md#code-removal)


# Developer's guide

## Creating elivepatch-overlay
[elivepatch overlay example](https://github.com/aliceinwire/elivepatch-overlay)

## Contributing

Fork this repo and make a pull request. We are happy to merge it.

Commit message should look like

```
[category/packagename] short decription

Long description
```

This makes reading history easier. GPG signing your changes is a good idea.

If you have push access to this repo it is a good idea to still create a pull request,
so at least one more person have reviewed your code.
Exceptions are trivial changes and urgent changes (that fix something completely broken).

## Communication

 - Join #gentoo-kernel channel on Freenode
 - Open issues [here](https://github.com/gentoo/elivepatch-client/issues)
