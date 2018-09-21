import bson
import json
import sys
import pymongo


def bson_ts_to_long(timestamp):
    """Convert BSON timestamp into integer.

    Conversion rule is based from the specs
    (http://bsonspec.org/#/specification).
    """
    return ((timestamp.time << 32) + timestamp.inc)


def write_oplog_progress(progress_path, progress_dict):
    """ Writes oplog progress to file provided by user
    """
    items = [[name, bson_ts_to_long(progress_dict[name])]
             for name in progress_dict]
    if not items:
        return

    # for each of the threads write to file
    with open(progress_path, 'w') as dest:
        if len(items) == 1:
            # Write 1-dimensional array, as in previous versions.
            json_str = json.dumps(items[0])
        else:
            # Write a 2d array to support sharded clusters.
            json_str = json.dumps(items)
        try:
            dest.write(json_str)
        except IOError:
            exit('Failed to write to file!')

def get_newest_oplog_timestamp(client):
    """Return the timestamp of the newest entry in the oplog.
    """
    curr = client.local.oplog.rs.find(
        {'op': {'$ne': 'n'}}).sort('$natural', pymongo.DESCENDING).limit(-1)

    try:
        ts = next(curr)['ts']
    except StopIteration:
        exit("oplog is empty.")

    return ts


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit('usage: ./write_oplog_progress.py oplog_timestamp_file replica_set_names replica_set_hosts')
    progress_path = sys.argv[1]

    replica_set_names = sys.argv[2].split(',')
    if not isinstance(replica_set_names, list):
        replica_set_names = [replica_set_names]
    
    replica_set_hosts = sys.argv[3].split(',')
    if not isinstance(replica_set_hosts, list):
        replica_set_hosts = [replica_set_hosts]
    if len(replica_set_names) != len(replica_set_hosts):
        exit('size of replica_set_names not equal to size of replica_set_hosts')

    progress_dict = dict(
        (name, get_newest_oplog_timestamp(pymongo.MongoClient(replica_set_hosts[idx])))
                    for idx, name in enumerate(replica_set_names))
    write_oplog_progress(progress_path, progress_dict)
    print('wrote lastest oplog entry to: ' + progress_path)