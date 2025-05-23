FROM archlinux:base-devel AS build_prep

RUN echo "[multilib]" >> /etc/pacman.conf && echo "Include = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf
RUN echo 'MAKEFLAGS="-j$(nproc)"' >> /etc/makepkg.conf
RUN pacman-key --init && pacman -Sy --noconfirm archlinux-keyring && pacman -Su --noconfirm && pacman -Syyuq --noconfirm

FROM build_prep AS build

RUN pacman -S tar unzip wget git pacutils perl-json-xs reflector --noconfirm
RUN useradd -u 10002 -m buildhelper
RUN echo "buildhelper ALL=(root) NOPASSWD: /usr/bin/pacman, /usr/bin/pacsync" | sudo EDITOR='tee -a' visudo
WORKDIR /home

# workaround: error: redefinition of ‘__fastfail’
#RUN pacman -S mingw-w64-gcc --noconfirm
#RUN sed -i 's@#if __MINGW_FASTFAIL_IMPL == 1@#if __MINGW_FASTFAIL_IMPL == 1 && !defined(i386)@g' /usr/i686-w64-mingw32/include/_mingw.h

ARG commit=65124f15acc5705eb159d5d920877f0ac4835d27
ARG branch=master
#ARG branch=msys2-hacks-18
#ARG repo=https://gitlab.winehq.org/bernhardu/wine.git
ARG repo=https://gitlab.winehq.org/jhol/wine.git
#ARG repo=https://gitlab.winehq.org/wine/wine.git

RUN wget -q --content-disposition 'https://aur.archlinux.org/cgit/aur.git/snapshot/wine-git.tar.gz' -P ./ && tar xzf *.tar.gz && chown -R buildhelper:buildhelper ./wine-git
RUN sed -i "s@https://gitlab.winehq.org/wine/wine.git@${repo}#commit=${commit}@g" ./wine-git/PKGBUILD
RUN sed -i 's@pkgver=.*@pkgver=msys@g' ./wine-git/PKGBUILD
RUN sed -i 's@pkgrel=.*@pkgrel=1@g' ./wine-git/PKGBUILD

# disable pkgver()
RUN sed -i 's@pkgver()@disabled_pkgver()@g' ./wine-git/PKGBUILD

RUN su buildhelper -c "cd ./wine-git && makepkg -m -f -c -C -s -i --noconfirm"

FROM build_prep

LABEL org.opencontainers.image.title="conan-wine"
LABEL org.opencontainers.image.authors="Björn Stresing <bjoern.stresing@gmx.de>"
LABEL org.opencontainers.image.description="This image provides a wine environment with python & conan & msys2 already installed"
LABEL org.opencontainers.image.source="https://github.com/Privatehive/g-spot-runner-github-actions"
LABEL org.opencontainers.image.url="https://github.com/Privatehive/g-spot-runner-github-actions/pkgs/container/conan-wine"

COPY --from=build /home/wine-git/wine-git-msys-1-x86_64.pkg.tar.zst /tmp/wine_pkg.tar.zst
RUN pacman -U /tmp/wine_pkg.tar.zst --noconfirm && rm /tmp/wine_pkg.tar.zst
RUN pacman -S xorg-server-xvfb vulkan-swrast lib32-vulkan-swrast samba unzip wget --noconfirm

RUN mkdir -p /opt/wineprefix
ENV WINEDEBUG -all
ENV WINEPREFIX /opt/wineprefix

COPY wine-init.sh SHA256SUMS.txt /tmp/helper/
COPY mkuserwineprefix /opt/

RUN xvfb-run sh /tmp/helper/wine-init.sh

ARG PYTHON_VERSION=3.12.7
ARG UPX_VERSION=4.2.4
ARG CONAN_VERSION=2.6.0
ARG MSYS2_VERSION=20221216

RUN umask 0 && cd /tmp/helper && \
  curl -LOOO \
    https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-amd64.exe{,.asc} \
    https://github.com/upx/upx/releases/download/v${UPX_VERSION}/upx-${UPX_VERSION}-win64.zip \
  && \
  xvfb-run sh -c "\
    wine python-${PYTHON_VERSION}-amd64.exe /quiet TargetDir=C:\\Python \
      Include_doc=0 InstallAllUsers=1 PrependPath=1; \
    wineserver -w" && \
  unzip upx*.zip && \
  mv -v upx*/upx.exe ${WINEPREFIX}/drive_c/windows/ && \
  cd .. && rm -Rf helper

RUN umask 0 && xvfb-run sh -c "\
  wine pip install --no-warn-script-location conan==$CONAN_VERSION pyinstaller; \
  wineserver -w"

#oldest
#RUN wget q -O- https://github.com/msys2/msys2-installer/releases/download/2020-11-09/msys2-base-x86_64-20201109.tar.xz | tar -C "${WINEPREFIX}/drive_c" -xJf -
#newest
#https://github.com/msys2/msys2-installer/releases/download/2021-11-30/msys2-base-x86_64-20211130.tar.xz
RUN wget q -O- https://github.com/msys2/msys2-installer/releases/download/2021-01-05/msys2-base-x86_64-20210105.tar.xz | tar -C "${WINEPREFIX}/drive_c" -xJf -

RUN sed -i 's/SigLevel    = Required DatabaseOptional/SigLevel = TrustAll DatabaseNever/g' "${WINEPREFIX}/drive_c/msys64/etc/pacman.conf"
RUN sed -i 's/SigLevel    = Required/SigLevel = TrustAll DatabaseNever/g' "${WINEPREFIX}/drive_c/msys64/etc/pacman.conf"

#RUN cd $WINEPREFIX/drive_c && WINEPATH="c:/msys64/usr/bin" wine64 c:/msys64/usr/bin/bash.exe -c 'pacman --help'
#wine64 msys.exe in -c -t "C:/msys2"

RUN useradd -d /home/conan -u 10000 conan
RUN mkdir -p ${WINEPREFIX}/drive_c/drivers/etc
RUN chown -R conan:conan ${WINEPREFIX}

USER conan
WORKDIR /home/conan
COPY --chown=conan:conan --chmod=744 entrypoint.sh /
COPY --chown=conan:conan --chmod=744 global.conf ${WINEPREFIX}/drive_c/users/conan/.conan2/global.conf
# initial msys2 setup
ENV WINEPATH="c:/msys64/usr/bin"
ENV MSYSTEM=MSYS
RUN wine64 bash --login -c 'exit'
RUN wine64 bash -c 'wget https://repo.msys2.org/msys/x86_64/make-4.4.1-1-x86_64.pkg.tar.zst -P /tmp/pkg && pacman -U --noconfirm /tmp/pkg/make-4.4.1-1-x86_64.pkg.tar.zst && rm -r /tmp/pkg'
ENTRYPOINT ["/entrypoint.sh"]
CMD ["cmd"]


#RUN xvfb-run sh /tmp/helper/wine-init.sh

#ENV DEBIAN_FRONTEND noninteractive

#RUN dpkg --add-architecture i386 && apt update && apt -y upgrade
#RUN apt install -y git build-essential flex bison xserver-xorg-dev libxft-dev gcc-multilib
#RUN git clone -b msys2-hacks-18 --single-branch https://gitlab.winehq.org/jhol/wine.git /tmp/wine
#RUN cd /tmp/wine && mkdir _build_64 && cd _build_64 && ../configure --enable-win64 --prefix=/usr && make -j$(nproc)
#RUN cd /tmp/wine && mkdir _build_32 && cd _build_32 && PKG_CONFIG_PATH=$(which pkg-config) ../configure --with-wine64=../_build_64 --prefix=/usr && make -j$(nproc)

#FROM ubuntu:20.04
#LABEL org.opencontainers.image.title="conan-wine"
#LABEL org.opencontainers.image.authors="Björn Stresing <bjoern.stresing@gmx.de>"
#LABEL org.opencontainers.image.description="This image provides a wine environment with python & conan already installed"
#LABEL org.opencontainers.image.source="https://github.com/Privatehive/g-spot-runner-github-actions"
#LABEL org.opencontainers.image.url="https://github.com/Privatehive/g-spot-runner-github-actions/pkgs/container/conan-wine"

#ENV DEBIAN_FRONTEND noninteractive
#RUN apt update && apt install -y xvfb curl

#COPY --from=build /opt/wineprefix /opt/wineprefix
# RUN mkdir -p /opt/wineprefix
# ENV WINEDEBUG -all
# ENV WINEPREFIX /opt/wineprefix

# COPY wine-init.sh SHA256SUMS.txt /tmp/helper/
# COPY mkuserwineprefix /opt/

# RUN xvfb-run sh /tmp/helper/wine-init.sh

# ARG PYTHON_VERSION=3.12.7
# ARG UPX_VERSION=4.2.4

# RUN umask 0 && cd /tmp/helper && \
#   curl -LOOO \
#     https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-amd64.exe{,.asc} \
#     https://github.com/upx/upx/releases/download/v${UPX_VERSION}/upx-${UPX_VERSION}-win64.zip \
#   && \
#   xvfb-run sh -c "\
#     wine python-${PYTHON_VERSION}-amd64.exe /quiet TargetDir=C:\\Python \
#       Include_doc=0 InstallAllUsers=1 PrependPath=1; \
#     wineserver -w" && \
#   unzip upx*.zip && \
#   mv -v upx*/upx.exe ${WINEPREFIX}/drive_c/windows/ && \
#   cd .. && rm -Rf helper

# RUN umask 0 && xvfb-run sh -c "\
#   wine pip install --no-warn-script-location pyinstaller; \
#   wineserver -w"

#ARG CONAN_VERSION="2.6.0"
#RUN useradd -d /home/conan -u 10000 conan
#RUN wine64 pip install conan==$CONAN_VERSION

#USER conan
#WORKDIR /home/conan
#COPY --chown=conan:conan --chmod=744 entrypoint.sh /
#ENTRYPOINT ["/entrypoint.sh"]
#CMD ["cmd"]
