import sys
import os
import json
import time
from kafka import KafkaConsumer
from kafka import KafkaClient
from kafka.producer.kafka import KafkaProducer
from kafka.structs import TopicPartition
from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload


class PYTHONKAFKA:
    def __init__(self, brokers):
        self.brokers = brokers

    def _python_kafka_consumer(self, topic):
        """
            Populate total message dump into console
        """
        self.topic = topic
        # KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)
        KafkaConsumer(auto_offset_reset='latest', enable_auto_commit=False, group_id='smsgrp')
        # brokers = 'lppbdsvd061.gso.aexp.com:9092,lppbdsvd560.gso.aexp.com:9092,lppbdsvd561.gso.aexp.com:9092'
        consumer = KafkaConsumer(topic, bootstrap_servers=self.brokers)
        for msg in consumer:
            print(msg)

    def _testpkg(self):
        return self.brokers

    def _python_kafka_listtopics(self):
        """
            Return list of the topics of the kafka cluster
        """
        client = KafkaClient(hosts=self.brokers)
        topics = client.topics
        topic_list = list()
        for topic in topics:
            topic_list.append(topic)
        return topic_list

    def _python_kafka_partitionoffset(self, topic):
        """
            Return offset and partition of the topic
        """
        topic = self.topic
        client = SimpleClient(self.brokers)
        # topic = "test_fast_messages"
        partitions = client.topic_partitions[topic]
        offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
        offsets_responses = client.send_offset_request(offset_requests)
        for r in offsets_responses:
            print("partition = %s, offset = %s" % (r.partition, r.offsets[0]))

    def _python_kafka_offsetcount(self, topic):
        """
            Count no of offset of the topic
        """
        client = SimpleClient(self.brokers)
        self.topic = topic
        partitions = client.topic_partitions[self.topic]
        offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
        offsets_responses = client.send_offset_request(offset_requests)
        totaloffset = 0
        for r in offsets_responses:
            totaloffset = totaloffset + r.offsets[0]
        return totaloffset
