import numpy as np
import json
from jina import Document, DocumentArray, Executor, Flow, requests

class CharEmbed(Executor):  # a simple character embedding with mean-pooling
    offset = 32  # letter `a`
    dim = 127 - offset + 1  # last pos reserved for `UNK`
    char_embd = np.eye(dim) * 1  # one-hot embedding for all chars

    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        for d in docs:
            r_emb = [ord(c) - self.offset if self.offset <= ord(c) <= 127 else (self.dim - 1) for c in d.text]
            d.embedding = self.char_embd[r_emb, :].mean(axis=0)  # average pooling

class Indexer(Executor):
    _docs = DocumentArray()  # for storing all documents in memory

    @requests(on='/index')
    def foo(self, docs: DocumentArray, **kwargs):
        self._docs.extend(docs)  # extend stored `docs`

    @requests(on='/search')
    def bar(self, docs: DocumentArray, **kwargs):
        docs.match(self._docs, metric='euclidean')

f = Flow(port_expose=12345, protocol='http', cors=True).add(uses=CharEmbed, replicas=2).add(uses=Indexer)  # build a Flow, with 2 replica CharEmbed, tho unnecessary
with f:
    catalog_fridges = [json.loads(line) for line in open('../catalogs/full_refrigerators.json', 'r')]
    catalogs_grills = [json.loads(line) for line in open('../catalogs/full_grills.jsonl', 'r')]
    # catalog_clothes = json.load(open('../catalogs/catalog_clothes.json'))

    doc_arr = DocumentArray()
    for doc in catalog_fridges:
        dic = {}
        for k, v in doc.items():
            if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
                dic[k] = v
            if k == 'details':
                for k2, v2 in v.items():
                    if k2 in ['Full Description']:
                        dic['full_description'] = v2

        d = Document(tags={'properties': dic}, text= dic['title'])
        #d = Document(text = dic['title'])
        doc_arr.append(d)

    for doc in catalogs_grills:
        dic = {}
        for k, v in doc.items():
            if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
                dic[k] = v
            if k == 'details':
                for k2, v2 in v.items():
                    if k2 in ['Full Description']:
                        dic['full_description'] = v2

        d = Document(tags={'properties': dic}, text= dic['title'])
        #d = Document(text = dic['title'])
        doc_arr.append(d)
    f.post('/index', (d for d in doc_arr))
    f.block()  # block for listening request

