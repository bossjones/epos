from __future__ import absolute_import, division, print_function

import os
import pytest

from collections import Iterator

from epos.odo import Kafka
from odo import resource, odo

kafka = pytest.importorskip('pykafka')

from pykafka import KafkaClient
from pykafka.topic import Topic

from ..kafka import filter_kwargs, simple_consumer, producer


kafka_host = os.environ.get('KAFKA_HOST')


def test_kafka_resource(kafka):
    res1 = resource('kafka://{}/topic1'.format(kafka_host))
    res2 = resource('kafka://{}/topic2.dot'.format(kafka_host))
    res3 = resource('kafka://host/topic3._-', kafka=kafka)
    res4 = resource('kafka:///topic4', kafka=kafka)

    assert isinstance(res1, Kafka)
    assert isinstance(res2, Kafka)
    assert isinstance(res3, Kafka)
    assert isinstance(res4, Kafka)

    assert isinstance(res1.client, KafkaClient)
    assert isinstance(res2.client, KafkaClient)
    assert res3.client == kafka
    assert res4.client == kafka

    assert isinstance(res1.topic, Topic)
    assert res1.topic._name == 'topic1'
    assert isinstance(res2.topic, Topic)
    assert res2.topic._name == 'topic2.dot'
    assert isinstance(res3.topic, Topic)
    assert res3.topic._name == 'topic3._-'
    assert isinstance(res4.topic, Topic)
    assert res4.topic._name == 'topic4'


def test_kafka_with_list(kafka):
    uri = 'kafka:///listtest'

    odo(range(15), uri, kafka=kafka)
    result = odo(uri, list,
                 kafka=kafka,
                 consumer_timeout_ms=100,
                 consumer_group='test',
                 auto_commit_enable=True)

    assert result == range(15)


def test_kafka_with_iterator(kafka):
    uri = 'kafka://{}/iteratortest'.format(kafka_host)

    odo((i for i in range(10)), resource(uri), kafka=kafka)
    result = odo(uri, Iterator,
                 kafka=kafka,
                 consumer_timeout_ms=100,
                 consumer_group='test',
                 auto_commit_enable=True)

    assert isinstance(result, Iterator)
    assert list(result) == range(10)


def test_create_connection(mocker):
    pconn = create_connection(available_kwargs=('x', 'y', 'z'))

    fn = mocker.Mock()
    fn.__name__ = 'wrapped'
    conn = pconn(fn)

    conn(1, 2, x=1, y=2, i=0)
    fn.assert_called_with(1, 2, x=1, y=2)


def run_for_kafka_conns(mocker, pconn):
    fn = mocker.Mock()
    fn.__name__ = 'wrapped'
    conn = pconn(fn)

    conn(shit=1, topic='channel', dshape='var * {}')
    fn.assert_called_with(topic='channel', dshape='var * {}')


def test_simple_consumer(mocker):
    run_for_kafka_conns(mocker, simple_consumer())


def test_producer(mocker):
    run_for_kafka_conns(mocker, producer())
