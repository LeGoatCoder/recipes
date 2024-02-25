# This Dockerfile is used to create a development container for Python development.
# The image used is based on the official Microsoft Python dev container image.
# The Python version can be specified as an argument.

# Define the Python version to use in the container.
# All available options can be found in the following link:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.245.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.10-bullseye"

# Use the specified Python version as the base image.
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Optionally, specify a Node.js version to be installed in the container.
# If this option is not used, no Node.js will be installed.
ARG NODE_VERSION="none"

# If a Node.js version was specified, install it now.
RUN if [ "${NODE_VERSION}" != "none" ]; then \
    su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; \
fi

# Optionally, copy the pip requirements file to the container and install the required packages.
# This step can be uncommented if the pip requirements rarely change.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# Optionally, install additional OS packages.
# This step can be uncommented to install any required OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Optionally, install global node packages.
# This step can be uncommented to install any required global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-
