FROM registry.njuics.cn/fluentd/python:3.5

ADD ./* /root/

RUN pip install mongo-connector[elastic5] pymongo

WORKDIR /root

CMD ["bash", "start.sh"]