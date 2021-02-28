Summary:	The ultimate status-line/prompt utility
Name:		powerline
Version:	2.1.4
Release:	0.2
License:	MIT
Group:		Applications/System
Source0:	https://github.com/powerline/powerline/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c3663676cf24fb738a0dd09d95159ba5
URL:		https://github.com/powerline/powerline
BuildRequires:	fontconfig
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg
Requires:	fontconfig
Requires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Powerline is a status-line plugin for Vim, and provides status-lines
and prompts for several other applications, including zsh, bash, tmux,
IPython, Awesome and Qtile.

%package docs
Summary:	Powerline Documentation
Group:		Documentation
BuildArch:	noarch

%description docs
This package provides the powerline documentation.

%package -n vim-plugin-powerline
Summary:	Powerline VIM plugin
Group:		Applications/Editors/Vim
Requires:	%{name} = %{version}-%{release}
Requires:	vim
BuildArch:	noarch

%description -n vim-plugin-powerline
Powerline is a status-line plugin for vim, and provides status-lines
and prompts.

%package -n tmux-powerline
Summary:	Powerline for tmux
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	tmux
BuildArch:	noarch

%description -n tmux-powerline
Powerline for tmux.

Add to your ~/.tmux.conf file: "source /usr/share/tmux/powerline.conf"

%prep
%setup -q

sed -i -e "/DEFAULT_SYSTEM_CONFIG_DIR/ s@None@'%{_sysconfdir}/xdg'@" powerline/config.py
sed -i -e "/TMUX_CONFIG_DIRECTORY/ s@BINDINGS_DIRECTORY@'/usr/share'@" powerline/config.py

%build
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build

# build docs
cd docs
%{__make} html \
	SPHINXBUILD=%{_bindir}/sphinx-build
rm _build/html/.buildinfo
# A structure gets initialized while building the docs with os.environ.
# This works around an rpmlint error with the build dir being in a file.
sed -i -e 's/abuild/user/g' _build/html/develop/extensions.html

%{__make} man \
	SPHINXBUILD=%{_bindir}/sphinx-build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# config
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/%{name}
cp -a powerline/config_files/* $RPM_BUILD_ROOT%{_sysconfdir}/xdg/%{name}/

# fonts
install -d $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
install -d $RPM_BUILD_ROOT%{_datadir}/fonts/truetype
install -d $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail

cp -p font/PowerlineSymbols.otf $RPM_BUILD_ROOT%{_datadir}/fonts/truetype/PowerlineSymbols.otf
cp -p font/10-powerline-symbols.conf $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf

ln -s %{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf

# manpages
install -d $RPM_BUILD_ROOT%{_mandir}/man1
for f in powerline-config.1 powerline-daemon.1 powerline-lint.1 powerline.1; do
cp -p docs/_build/man/$f $RPM_BUILD_ROOT%{_mandir}/man1/$f
done

# awesome
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/awesome/
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/awesome/powerline.lua $RPM_BUILD_ROOT%{_datadir}/%{name}/awesome/
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/awesome/powerline-awesome.py $RPM_BUILD_ROOT%{_datadir}/%{name}/awesome/

# bash bindings
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/bash
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/bash/powerline.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/bash/

# fish
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/fish
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/fish/powerline-setup.fish $RPM_BUILD_ROOT%{_datadir}/%{name}/fish

# i3
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/i3
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/i3/powerline-i3.py $RPM_BUILD_ROOT%{_datadir}/%{name}/i3

# ipython
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/ipython
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/ipython/post_0_11.py $RPM_BUILD_ROOT%{_datadir}/%{name}/ipython
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/ipython/pre_0_11.py $RPM_BUILD_ROOT%{_datadir}/%{name}/ipython

# qtile
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/qtile
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/qtile/widget.py $RPM_BUILD_ROOT%{_datadir}/%{name}/qtile

# shell bindings
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/shell
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/shell/powerline.sh $RPM_BUILD_ROOT%{_datadir}/%{name}/shell/

# tcsh
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/tcsh
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/tcsh/powerline.tcsh $RPM_BUILD_ROOT%{_datadir}/%{name}/tcsh

# tmux plugin
install -d $RPM_BUILD_ROOT%{_datadir}/tmux
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/tmux/powerline*.conf $RPM_BUILD_ROOT%{_datadir}/tmux/

# vim plugin
install -d $RPM_BUILD_ROOT%{_datadir}/vim/site/plugin/
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/vim/plugin/powerline.vim $RPM_BUILD_ROOT%{_datadir}/vim/site/plugin/powerline.vim
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/vim/plugin
install -d $RPM_BUILD_ROOT%{_datadir}/vim/site/autoload/powerline
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/vim/autoload/powerline/debug.vim $RPM_BUILD_ROOT%{_datadir}/vim/site/autoload/powerline/debug.vim
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/vim/autoload

# zsh
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/zsh
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/zsh/__init__.py $RPM_BUILD_ROOT%{_datadir}/%{name}/zsh
mv $RPM_BUILD_ROOT%{py_sitescriptdir}/powerline/bindings/zsh/powerline.zsh $RPM_BUILD_ROOT%{_datadir}/%{name}/zsh

# cleanup
rm -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/config_files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf
%config(noreplace) %{_sysconfdir}/xdg/%{name}
%attr(755,root,root) %{_bindir}/powerline
%attr(755,root,root) %{_bindir}/powerline-config
%attr(755,root,root) %{_bindir}/powerline-daemon
%attr(755,root,root) %{_bindir}/powerline-render
%attr(755,root,root) %{_bindir}/powerline-lint
%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf
%dir %{_datadir}/fonts/truetype
%{_datadir}/fonts/truetype/PowerlineSymbols.otf
%{_mandir}/man1/powerline.1*
%{_mandir}/man1/powerline-config.1*
%{_mandir}/man1/powerline-daemon.1*
%{_mandir}/man1/powerline-lint.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/awesome
%{_datadir}/%{name}/awesome/powerline.lua
%{_datadir}/%{name}/awesome/powerline-awesome.py*
%dir %{_datadir}/%{name}/bash
%{_datadir}/%{name}/bash/powerline.sh
%dir %{_datadir}/%{name}/fish
%{_datadir}/%{name}/fish/powerline-setup.fish
%dir %{_datadir}/%{name}/i3
%{_datadir}/%{name}/i3/powerline-i3.py*
%dir %{_datadir}/%{name}/ipython
%{_datadir}/%{name}/ipython/post_0_11.py*
%{_datadir}/%{name}/ipython/pre_0_11.py*
%dir %{_datadir}/%{name}/qtile
%{_datadir}/%{name}/qtile/widget.py*
%dir %{_datadir}/%{name}/shell
%{_datadir}/%{name}/shell/powerline.sh
%dir %{_datadir}/%{name}/tcsh
%{_datadir}/%{name}/tcsh/powerline.tcsh
%dir %{_datadir}/%{name}/zsh
%{_datadir}/%{name}/zsh/__init__.py*
%{_datadir}/%{name}/zsh/powerline.zsh
%{py_sitescriptdir}/*

%files docs
%defattr(644,root,root,755)
%doc docs/_build/html/*

%files -n vim-plugin-powerline
%defattr(644,root,root,755)
%dir %{_datadir}/vim/site
%dir %{_datadir}/vim/site/autoload
%dir %{_datadir}/vim/site/autoload/powerline
%{_datadir}/vim/site/autoload/powerline/debug.vim
%dir %{_datadir}/vim/site/plugin
%{_datadir}/vim/site/plugin/powerline.vim

%files -n tmux-powerline
%defattr(644,root,root,755)
%dir %{_datadir}/tmux
%{_datadir}/tmux/powerline*.conf
