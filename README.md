# hardened_malloc
This repository tracks the hardened memory allocator from GrapheneOS [[Link](https://github.com/GrapheneOS/hardened_malloc)]. This is performed using GitHub's continuous integration, where the `ci-hardened_malloc.py` script is ran every 3 hours to check for new updates. If there are any, then the `hardened_malloc.spec` file is automatically updated, triggering the Hard Hat OS Copr repository to automatically start the build process for the latest version of Fedora Linux. Note that this will build both the default and light variants, but the light variant will be enabled globally by default using `/etc/ld.so.preload`. 

## Instructions
This package is in the Hard Hat OS Copr repository. To install it, enter the following commands as the root user:

1. Enable the Copr repository: `dnf copr enable hardhatos/release`

2. Update the cache: `dnf update`

3. Install the package: `dnf install hardened_malloc`
