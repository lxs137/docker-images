#!/bin/sh

if [[ -z ${REPLICA_SET_NAMES} ]]; then
	export REPLICA_SET_NAMES="shard1,shard2,shard3"
fi

if [[ -z ${REPLICA_SET_HOSTS} ]]; then
	export REPLICA_SET_HOSTS="114.212.189.147:10118,114.212.189.147:10123,114.212.189.147:10124"
fi

if [[ -z ${MONGO_URL} ]]; then
	export MONGO_URL="114.212.189.147:10100"
fi

if [[ -z ${ELASTICSEARCH_URL} ]]; then
	export ELASTICSEARCH_URL="114.212.189.147:10056"
fi

python write_oplog_progress.py ./new_oplog.timestamp ${REPLICA_SET_NAMES} ${REPLICA_SET_HOSTS}

mongo-connector --oplog-ts ./new_oplog.timestamp --main ${MONGO_URL} --target-url ${ELASTICSEARCH_URL} --doc-manager elastic2_doc_manager --logfile stdout --namespace-set 'Crawler.*'