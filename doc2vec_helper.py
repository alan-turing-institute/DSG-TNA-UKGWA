from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import glob
import os
import json
from operator import itemgetter


class DocumentsIterator():
    '''Due to the large number of documents, we work with an iterator insteads of arrays'''

    def __init__(self, indirs=None):
        ''' indirs - An array of directories with json files,
                     obtained from spacy_preprocess.py
        '''
        if indirs is None:
            indirs = ['/data/entities/result1',
                      '/data/entities/result2',
                      '/data/entities/result3',
                      '/data/entities/result4',
                      '/data/entities/result5',
                      '/data/entities/result6',
                      '/data/entities/result7',
                      '/data/entities/result8',
                      '/data/entities/result9',
                      '/data/entities/result10']
        self.indirs = indirs
        self.generator = self.documents_generator(self.indirs)

    def __iter__(self):
        # reset the generator
        self.generator = self.documents_generator(self.indirs)
        return self

    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result

    def documents_generator(self, indirs):
        for indir in indirs:
            os.chdir(indir)
            for file in glob.glob('*.json'):
                with open(file) as f:
                    entities = json.load(f)

                    # Remove entity types from spacy
                    flattened = [
                        text for type in entities for text in entities[type]]

                    # Order by position in original document
                    document = [text[0].lower()
                                for text in sorted(flattened, key=itemgetter(2))]

                    yield TaggedDocument(document, [file])


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self, out):
        self.epoch = 1
        self.out = out

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        if (self.epoch % 1 == 0):
            print("Epoch #{} end. Saved model".format(self.epoch))
            model.save(self.out + '_epoch' + str(self.epoch))
        self.epoch += 1
