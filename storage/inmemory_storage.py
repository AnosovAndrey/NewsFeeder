import hashlib
import pickle
import os.path

from storage.storage_base import StorageBase


class InmemoryStorage(StorageBase):
    def __init__(self):
        self.dict = {}

    def add_element(self, service_key, feed_element):
        body = (feed_element.body if feed_element.body else "") + \
            (feed_element.nested.body if feed_element.nested else "") + \
            feed_element.date + feed_element.author
        key = service_key + hashlib.md5(body.encode('utf-8')).hexdigest()
        if not key in self.dict:
            self.dict[key] = feed_element
        self.data_save(key, feed_element)

    def find_elements(self, service_key, filter_lambda):
        return {k: v for k, v in self.dict.items() if k.startswith(service_key) and filter_lambda(v)}
    
    def data_save(self, key, feed_element):
        if os.path.isfile('./storage/data.pickle'):
            with open('./storage/data.pickle', 'rb') as handle:
                b = pickle.load(handle)
            if not key in b:
                b[key] = feed_element
                with open('./storage/data.pickle', 'wb') as handle:
                    pickle.dump(b, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open('./storage/data.pickle', 'wb') as handle:
                pickle.dump(self.dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
