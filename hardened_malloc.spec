BuildArch: x86_64
BuildRequires: gcc, gcc-c++, make
License: MIT
Name: hardened_malloc
Release: 1%{?dist}
Source0: https://api.github.com/repos/GrapheneOS/hardened_malloc/tarball/11
Source1: hardened_malloc.8
Summary: Hardened memory allocator from GrapheneOS
URL: https://github.com/HardHatOS/hardened_malloc
Version: 11

%description
The hardened memory allocator from GrapheneOS; packaged for Fedora Linux

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

# Compile the hardened malloc, both the default and light variants, with the specified options. The following descriptions were taken directly from the hardened_malloc's GitHub page (https://github.com/GrapheneOS/hardened_malloc)
# CONFIG_NATIVE: true (default) or false to control whether the code is optimized for the detected CPU on the host. If this is disabled, setting up a custom -march higher than the baseline architecture is highly recommended due to substantial performance benefits for this code.
# VARIANT: The default configuration template has all normal optional security features enabled (just not the niche CONFIG_SEAL_METADATA) and is quite aggressive in terms of sacrificing performance and memory usage for security. The light configuration template disables the slab quarantines, write after free check, slot randomization and raises the guard slab interval from 1 to 8 but leaves zero-on-free and slab canaries enabled.
%{__make} CONFIG_NATIVE=false VARIANT=default
%{__make} CONFIG_NATIVE=false VARIANT=light

%install
# Copy the compiled hardened mallocs, both default and light variants, to the specified target directory
%{__install} -D "%{_srcdir}/out/libhardened_malloc.so" -t %{buildroot}%{_lib_hardened_malloc}
%{__install} -D "%{_srcdir}/out-light/libhardened_malloc-light.so" -t %{buildroot}%{_lib_hardened_malloc}

# Create the /etc and /etc/sysctl.d directories within the buildroot
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysctl.d

# Create a new file within the buildroot, /etc/ld.so.preload, that allows the hardened malloc to be enabled globally
touch %{buildroot}%{_ld_so_preload}

# Add instructions to users reading the file on how to switch between the light and default variants globally
echo "# By default, the light variant of the hardened malloc is used globally. If you wish to use the default, more secure, variant, then change the line below to: '%{_lib_hardened_malloc}/libhardened_malloc.so'. Be warned, this may break your system." >> %{buildroot}%{_ld_so_preload}

# Enable the light variant of the hardened malloc globally by default
echo "%{_lib_hardened_malloc}/libhardened_malloc-light.so" >> %{buildroot}%{_ld_so_preload}

# Create a new file that increases the 'vm.max_map_count' kernel tunable
echo 'vm.max_map_count = 1048576' > %{buildroot}%{_sysctl_hardened_malloc_conf}

# Copy the man page to the section 8 man page directory
install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_mandir}/man8

%files
%{_ld_so_preload}
%{_lib_hardened_malloc}/libhardened_malloc.so
%{_lib_hardened_malloc}/libhardened_malloc-light.so
%{_sysctl_hardened_malloc_conf}
%{_mandir}/man8/hardened_malloc.8.*

%postun
# Remove the /lib64/hardened_malloc directory
%{__rm} -r %{_lib_hardened_malloc}
