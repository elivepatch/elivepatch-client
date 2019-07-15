# elivepatch-client
[![Maintainability](https://api.codeclimate.com/v1/badges/67c1cd220ba85837d96f/maintainability)](https://codeclimate.com/github/gentoo/elivepatch-client/maintainability)

Flexible Distributed Linux Kernel Live Patching


## Features

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

## User's guide

### Installing from source

```
$ git clone https://github.com/gentoo/elivepatch-client
$ cd elivepatch-client/
$ virtualenv .venv
$ python setup.py install
```

### Example usage

```
elivepatch-client -p example/2.patch -k example/config_5.1.6  -a 5.1.6 --url http://localhost:5000
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

## Repository

* [elivepatch-client](https://github.com/gentoo/elivepatch-client)
  * Client to be run on the machine where we want to install the live patch.
* [elivepatch-server](https://github.com/gentoo/elivepatch-server)
  * RESTful API to be run on the server using kpatch for building the live patch.
* [elivepatch-overlay](https://github.com/elivepatch/livepatch-overlay)
  * Where to keep your livepatch patches.
* [elivepatch-docker](https://github.com/elivepatch/elivepatch-docker)
  * Simplyfing elivepatch-server start.

## Developer's guide

### Contributing

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

### Communication

 - Join #gentoo-kernel channel on Freenode
 - Open issues [here](https://github.com/gentoo/elivepatch-client/issues)
