FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    python3.7-dev \
    net-tools \
    strace \
    htop \
 && rm -rf /var/lib/apt/lists/*

ARG app_whl_file=""

COPY dist/${app_whl_file} /

RUN pip install /${app_whl_file}
COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
