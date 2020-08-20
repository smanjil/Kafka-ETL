
# Apache Kafka Learning

## Getting Kafka source for installation
```
Source: https://timber.io/blog/hello-world-in-kafka-using-python/

$ wget https://archive.apache.org/dist/kafka/1.1.0/kafka_2.11-1.1.0.tgz
```

## Un-tar Kafka
```
$ tar -zxvf kafka_2.11-1.1.0.tgz
$ cd kafka_2.11-1.1.0/
```

## Starting zookeper server
```
-- Change line 251 having:

JAVA_MAJOR_VERSION=$($JAVA -version 2>&1 | sed -E -n 's/.* version "([^.-]*).*"/\1/p')


with:

JAVA_MAJOR_VERSION=$($JAVA -version 2>&1 | sed -E -n 's/.* version "([^.-]*).*/\1/p')

Source: https://stackoverflow.com/questions/50513744/apache-kafka-2-12-1-1-0-not-working-with-jdk-10-0-1/51145576

-- Server starting error if not replaced.

$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

## Starting Kafka server
```
$ bin/kafka-server-start.sh config/server.properties
```

## Creating Kafka Topics
```
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sample

-- You can find this port in zookerper server log: 

[2020-08-14 17:12:36,155] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)
```

## List all Kafka topics
```
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
```

## Using desribe topics to get more details on a particular topic
```
$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic sample
```

## Installing Kafka python version (Refer to Pipfile)
```
$ pipenv shell --python 3.8
$ pipenv install
```

## Kafka Producer and Consumer
### Kafka Consumer
```
$ python src/sample/consumer.py (To receive messages)
$ python src/sample/producer.py (To send messages)
```

### ETL process for extracting stackoverflow questions and tags and loading in db
```
- Producer (python src/crawl.py) -- Performs the Extract Process
    - Creating Crawler for StackOVerflow
    - Initating Producer with a topic 'stack' and sending each detail to consumer
- Consumer -- Performs the Transform and Load Process
    - python src/consumer.py
```