FROM tobix/pywine:3.12
LABEL org.opencontainers.image.title="conan-wine"
LABEL org.opencontainers.image.authors="Björn Stresing <bjoern.stresing@gmx.de>"
LABEL org.opencontainers.image.description="This image provides a wine environment with python & conan already installed"
LABEL org.opencontainers.image.source="https://github.com/Privatehive/g-spot-runner-github-actions"
LABEL org.opencontainers.image.url="https://github.com/Privatehive/g-spot-runner-github-actions/pkgs/container/conan-wine"

ARG CONAN_VERSION="2.3.1"
RUN useradd -d /home/conan -u 10000 conan
RUN wine64 pip install conan==$CONAN_VERSION

USER conan
WORKDIR /home/conan
COPY --chown=conan:conan --chmod=744 entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["cmd"]
