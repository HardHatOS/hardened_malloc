# hardened_malloc
This repository tracks the hardened memory allocator from GrapheneOS ([link](https://github.com/GrapheneOS/hardened_malloc)). This is performed using GitHub's continuous integration, where the `ci-hardened_malloc.py` script is ran every 3 hours to check for new updates. If there are any, then the `hardened_malloc.spec` file is automatically updated, triggering the Hard Hat Copr repository ([link](https://copr.fedorainfracloud.org/coprs/hardhat/release)) to automatically start the build process for the latest version of Fedora Linux. Note that this will built the light variant of the hardened malloc and enable it globally using `/etc/ld.so.preload`.

## Instructions
To enable this repository, enter the following commands as the root user:

1. Enable the Copr repository: `dnf copr enable hardhat/release`

2. Update the cache: `dnf update`

3. Install the hardened_malloc package: `dnf install hardened_malloc`
