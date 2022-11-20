FROM debian:bullseye

# default shell to bash
SHELL ["/bin/bash", "--login", "-c"]
ENV TERM=xterm

RUN apt-get update
# Debian dependencies
RUN apt-get install --yes sqlite3 python3 python3-pip
# Copy source code and python dependencies
RUN mkdir -p /usr/share/moro-books
RUN mkdir -p /opt
COPY ./src/* /usr/share/moro-books/
COPY ./requirements.txt /usr/share/moro-books/requirements.txt
COPY ./testing_requirements.txt /usr/share/moro-books/testing_requirements.txt
COPY docker_entrypoint /opt/docker_entrypoint

RUN python3 -m pip install -r /usr/share/moro-books/requirements.txt
RUN python3 -m pip install -r /usr/share/moro-books/testing_requirements.txt

RUN chmod -R +x /usr/share/moro-books/
RUN chmod +x /opt/docker_entrypoint
EXPOSE 9999

ENTRYPOINT ["/opt/docker_entrypoint"]