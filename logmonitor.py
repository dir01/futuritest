import argparse
from datetime import datetime

from twisted.internet import inotify, reactor
from twisted.python import filepath
from pymongo import Connection

from utils import Signal


class FileWatcher(object):
    EVENT_MODIFIED = 2
    EVENT_RENAMED = 2048

    def __init__(self, path):
        self.path = path
        self.open_file()
        self.bind_events()
        self.on_more_content = Signal()

    def on_file_changed(self, ignored, filepath, mask):
        handler = {
            self.EVENT_MODIFIED: self.read_more,
            self.EVENT_RENAMED: self.rebind_events,
        }.get(mask)
        if not handler:
            print 'Ignoring event %s (%s)' % (
                mask, inotify.humanReadableMask(mask)
            )
            return
        return handler()

    def read_more(self):
        content = self.file.read()
        self.on_more_content.emit(content)

    def rebind_events(self):
        self.open_file()
        self.bind_events()

    def open_file(self):
        self.file = open(self.path, 'r')

    def bind_events(self):
        self.notifier = inotify.INotify()
        self.notifier.startReading()
        self.notifier.watch(
            filepath.FilePath(self.path),
            callbacks=[self.on_file_changed]
        )


class MongoLogWriter(object):
    def __init__(self, db_name, collection_name, host='localhost', port=27017):
        self.collection = Connection(host, port)[db_name][collection_name]

    def parse_and_write(self, content):
        log_entries = content.strip('\n').split('\n')
        log_entries = filter(None, log_entries)
        map(self.parse_and_write_single_log_entry, log_entries)

    def parse_and_write_single_log_entry(self, log_entry):
        timestamp, uid, url, status, response_time, response_length = log_entry.split('|')
        log_dt = datetime.fromtimestamp(float(timestamp))
        self.collection.insert({
            'datetime': log_dt,
            'uid': uid if uid != '-' else None,
            'status': int(status),
            'response_time': float(response_time),
            'response_length': int(response_length)
        })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filename', type=str, nargs=1)
    parser.add_argument(
        '--database', type=str, default='test',
        help='MongoDB database name to store parsed logs to',
    )
    parser.add_argument(
        '--collection', type=str, default='logs',
        help='MongoDB collection name to store parsed logs to',
    )
    args = parser.parse_args()

    watcher = FileWatcher(args.filename[0])
    writer = MongoLogWriter(db_name=args.database, collection_name=args.collection)
    watcher.on_more_content.connect(writer.parse_and_write)
    reactor.run()
