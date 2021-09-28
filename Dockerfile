FROM openjdk:11
MAINTAINER Anastasia Lukina <alukina@minsait.com>
LABEL version="1.0"
LABEL description="First image with Dockerfile."
ARG releaseVersion

# Install cron and dependencies
RUN apt-get update && apt-get -y install cron rsyslog

RUN update-ca-certificates -f \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
    software-properties-common \
    wget \
    git \
    libatlas3-base \
    libopenblas-base \
    libatlas-base-dev \
    build-essential \
  && apt-get clean

# Hadoop
#ENV HADOOP_HOME /opt/hadoop
#ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
#ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
#WORKDIR /opt
#RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz\
#  && tar -xvzf hadoop-3.2.2.tar.gz \
#  && mv hadoop-3.2.2 hadoop

# Spark
ENV SPARK_HOME=/opt/spark
ENV SPARK_MASTER_PORT 7077
ENV PATH=$PATH:$SPARK_HOME/bin/:$SPARK_HOME/sbin/
WORKDIR /opt
RUN wget https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz\
  && tar -xvzf spark-3.1.1-bin-hadoop3.2.tgz \
  && mv spark-3.1.1-bin-hadoop3.2 spark
RUN mkdir -p /opt/spark/work/ \
  && chmod -R 777 /opt/spark/work/

WORKDIR /$SPARK_HOME
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]

# Miniconda
ENV CONDA_DIR=/root/miniconda3/
ENV PATH=$CONDA_DIR/bin:$CONDA_DIR/envs/spark/:$PATH

ENV PYSPARK_PYTHON=$CONDA_DIR/envs/spark/bin/python3
ENV PYSPARK_DRIVER_PYTHON=$CONDA_DIR/envs/spark/bin/python3

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && conda update -n base -c defaults conda
RUN conda --version

ENV APP_HOME /app/
COPY . /app


WORKDIR $APP_HOME
COPY ingestionpack/app/crontab  /app

ENV PYTHONUNBUFFERED 1
ENV LOGGING_DIR="$APP_HOME"logs
ENV CONFIG_DIR="$APP_HOME"ingestionpack/config/
ENV ENV=DEV
ENV relVersion ${releaseVersion}
ENV TZ Europe/Madrid

RUN crontab /app/crontab
RUN chmod a+x /app/crontab
RUN mkdir -p /app/logs
RUN chmod 777 /app/logs
RUN touch /etc/default/locale

RUN conda init bash \
    && . ~/.bashrc \
    && conda create -n spark python=3.9.1 \
    && conda activate spark \
    && pip install -r requirements.txt \
    && conda list
#&& pip install -r $APP_HOME/requirements.txt \

ENV FLASK_PORT=6200
EXPOSE 6200

# carpeta donde irá el config.properties
VOLUME "$APP_HOME"ingestionpack/config
VOLUME "$LOGGING_DIR"
#ENTRYPOINT ["spark-submit", "--master", "yarn", "--deploy-mode", "client", "--proxy-user", "shelly", "--packages", "app.py"]
#ENTRYPOINT ["python"]
#CMD ["conda activate spark","app.py"]

# Launch the API
CMD ["bash","-c","source activate spark && python main.py" ]
#ENTRYPOINT service rsyslog start && /bin/bash start.sh