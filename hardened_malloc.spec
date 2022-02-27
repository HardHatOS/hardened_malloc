Name:       hardened_malloc
Version:    11
Release:    1%{?dist}
Summary:    Hardened memory allocator (light variant) from GrapheneOS

Group:      System Environment/Base
License:    MIT
URL:        https://github.com/noatsecure/hardened_malloc
Source0:    https://api.github.com/repos/GrapheneOS/hardened_malloc/tarball/11
BuildArch:  x86_64
BuildRequires: gcc, gcc-c++, make

%description
The hardened memory allocator (light variant) from GrapheneOS; repackaged for Fedora Linux

%prep
# RPM macro for the file in /etc that will load the hardened malloc
%define _ld_so_preload %{_sysconfdir}/ld.so.preload

# RPM macro for the directory in /lib64 that will contain the compiled hardened malloc
%define _lib_hardened_malloc /%{_lib}/hardened_malloc

# RPM macro for the directory that will contain the source files of the hardened malloc
%define _srcdir hardened_malloc

# RPM macro for the sysctl file in /etc that increases the 'vm.max_map_count'
%define _sysctl_hardened_malloc_conf %{_sysconfdir}/sysctl.d/hardened_malloc.conf

# Create the directory that will contain the source for the hardened malloc
%{__mkdir} %{_srcdir}

# Uncompress the contents of the hardened_malloc archive to the source directory
%{__tar} -x -f %{SOURCE0} -C %{_srcdir} --strip-components 1

%build
# Change directory into the source directory
cd %{_srcdir}

# Compile the hardened malloc with the specified options. The following descriptions were taken directly from the hardened_malloc's GitHub page (https://github.com/GrapheneOS/hardened_malloc)
# CONFIG_NATIVE: true (default) or false to control whether the code is optimized for the detected CPU on the host. If this is disabled, setting up a custom -march higher than the baseline architecture is highly recommended due to substantial performance benefits for this code.
# VARIANT: The light configuration template disables the slab quarantines, write after free check, slot randomization and raises the guard slab interval from 1 to 8 but leaves zero-on-free and slab canaries enabled.
#
# Additionally, there are also CFLAGS specified as well:
# -march=x86_64: Compiles for a generic x86-64 target. This is required because the system the hardened malloc is compiled on will have different hardware than the end-user's machine.
# -fpic: Required since the '-march=x86-64' CFLAG is used.
%{__make} CFLAGS='-march=x86-64 -fpic' CONFIG_NATIVE=false VARIANT=light

%install
# Copy the compiled hardened malloc to the specified target directory
%{__install} -D "%{_srcdir}/out-light/libhardened_malloc-light.so" -t %{buildroot}%{_lib_hardened_malloc}

# Create the /etc and /etc/sysctl.d directories within the buildroot
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysctl.d

# Create a new file that enables the hardened malloc globally   
echo "%{_lib_hardened_malloc}/libhardened_malloc-light.so" > %{buildroot}%{_ld_so_preload}

# Create a new file that increases the 'vm.max_map_count' kernel tunable
echo 'vm.max_map_count = 1048576' > %{buildroot}%{_sysctl_hardened_malloc_conf}

%files
%{_ld_so_preload}
%{_lib_hardened_malloc}/libhardened_malloc-light.so
%{_sysctl_hardened_malloc_conf}

%postun
# Remove the /lib64/hardened_malloc directory
%{__rm} -r %{_lib_hardened_malloc}
