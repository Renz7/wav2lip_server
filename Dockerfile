FROM linuxserver/ffmpeg as build
LABEL authors="ren"

COPY requirements.txt requirements.txt

ARG SOURCE_DIST=mirrors.tuna.tsinghua.edu.cn
ARG PIP_INDEX=https://pypi.douban.com/simple

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sed -i "s/archive.ubuntu.com/${SOURCE_DIST}/g" /etc/apt/sources.list
RUN sed -i "s/ports.ubuntu.com/${SOURCE_DIST}/g" /etc/apt/sources.list

#RUN --mount=type=cache,target=/var/cache/apt \
RUN apt update -y \
    && apt upgrade -y libc-bin \
    && apt install -yqq --no-install-recommends rustc cargo python3-pip ffmpeg
# non root user will cause permission problem
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt -i ${PIP_INDEX} -v

ENTRYPOINT ["top", "-b"]


FROM build

WORKDIR /ruuner
COPY . /ruuner

RUN chmod 755 entrypoint.sh

EXPOSE 8000
VOLUME ./output/
ENTRYPOINT ["./entrypoint.sh"]