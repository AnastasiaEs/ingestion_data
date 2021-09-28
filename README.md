Microservices Ingestion data

# Prepare
Install Hadoop Test Local
Getting Started
First, you will need to update your system packages to the latest version. You can update all of them with the following command:
* apt-get update -y

Install Java
Apache Spark is a Java-based application. So Java must be installed in your system. You can install it with the following command:
* apt-get install default-jdk -y
* java --version

Install Apache Spark
First, you will need to download the latest version of Apache Spark from its official website. 
At the time of writing this tutorial, the latest version of Apache Spark is 2.4.6. You can download it to the /opt directory with the following command:

* cd /opt
* sudo wget https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz
* sudo tar -xvzf spark-3.1.1-bin-hadoop3.2.tgz
* sudo mv spark-3.1.1-bin-hadoop3.2/ spark
* sudo rm -r spark-3.1.1-bin-hadoop3.2.tgz

# nano ~/.bashrc
* export SPARK_HOME="/opt/spark"
* export PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:/home/alukina/miniconda3/envs/territories/bin"
* export PYSPARK_PYTHON="/home/alukina/miniconda3/envs/territories/bin/python3"
* export PYSPARK_DRIVER_PYTHON="/home/alukina/miniconda3/envs/territories/bin/python3"
* source ~/.bashrc

# Start Spark Master Server

At this point, Apache Spark is installed and configure. Now, start the Spark master server using the following command:

* start-master.sh
* ss -tpln | grep 8080

Now, open your web browser and access the Spark web interface using the URL   
http://localhost:8080

You should see the following screen:
# Start Spark Worker Process:
 * start-slave.sh spark://anastasia-minsait:7077

# Stop Spark Worker Process:
 * stop-master.sh
 * stop-slave.sh

## Docker Local
* docker build -t alukina/ingestion:v1 . 
* docker build --no-cache --pull -t alukina/ingestion:v1 . 
//entrar al contenedor docker: * docker run -it alukina/ingestion:v1 /bin/bash  
* docker run -it -p 6200:6200 alukina/ingestion:v1  
##  Llamar a la api desde postman    
Postman Get: http://localhost:6200/ingestion_data/v1/example_table 
--------------------------------------------
#Docker
* docker images  
Parar o eliminar todos los contenedores docker:
Para pararlos puede usarse:
* sudo docker stop $(sudo docker ps -a -q)
Y para eliminarlos:
* sudo docker rm $(sudo docker ps -a -q)
* sudo docker system prune
* sudo docker builder prune
* Eliminar un contenedor al cerrarlo  docker run --rm image_name
* Eliminar imágenes
* docker rmi $(docker images -q) -f


# Definir variables de entorno local
 *export LOGGING_DIR=TuDirenv  
 Ejemplo: /user/TERRITORIOS/ingestion_data/.local/logs
* export CONFIG_DIR=TuDir
Ejemplo:  /user/TERRITORIOS/ingestion_data/.local/config;
* export ENV=LOCAL  
 posibles valores: [LOCAL,DEV, PRE, PRO]

#Error ResourceWarning: unclosed 
* add def _init__(self):  
        self.session = requests.Session()

