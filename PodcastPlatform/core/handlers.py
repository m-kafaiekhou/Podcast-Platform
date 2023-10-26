from elasticsearch import Elasticsearch
import logging
import json
from urllib.parse import parse_qs


class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts, index_name):
        super().__init__()
        self.hosts = hosts
        self.index_name = index_name
        self.es = Elasticsearch(hosts)

    def emit(self, record):
        print("*#" * 20)
        print(parse_qs(record.getMessage()))
        print("*#" * 20)
        try:
            msg = dict(record.msg)
        except ValueError:
            msg = record.msg
        
        doc = {
            'name': f'{record.name}',
            'level': f'{record.levelname}',
            'levelno': f'{record.levelno}',
            'msg': parse_qs(record.getMessage()),
            'proccess': f'{record.processName}',
            'exc_info': f'{record.exc_info}',
            'exc_text': f'{record.exc_text}',
        }
        self.es.index(index=self.index_name, body=doc)
