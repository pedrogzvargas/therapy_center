kafka-topics \
--create \
--topic app-events \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1

kafka-topics \
--create \
--topic backoffice-events \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1