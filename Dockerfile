FROM alpine:3.9

COPY . /app

WORKDIR /app

RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    curl \
    build-base

# Set Python version
ARG PYTHON_VERSION='3.8.0'

# Set pyenv home
ARG PYENV_HOME=/root/.pyenv

# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH
RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION

#Install project dependencies
RUN pip3 install --upgrade setuptools \
	&& pip3 install -r requirements.txt --src /usr/local/src \
    && pyenv rehash

# Clean
RUN rm -rf ~/.cache/pip /var/cache/apk/*

EXPOSE 3000

CMD ["python3", "api_v1_routes.py"]
