import os
from gensim.models.doc2vec import Doc2Vec
import time
from doc2vec_helper import DocumentsIterator, EpochLogger

outdir = '/data/doc2vec/'

# Choose hyperparameters
params = {'window': 2,  # max distance between current word and predicted word
          'min_count': 2,  # minimum number of occurrences of words in vocab
          'workers': len(os.sched_getaffinity(0)),  # number of available cpus
          'vector_size': 300,  # output (feature) dimensionality
          'epochs': 100  # number of training iterations over dataset
          }
print(params)

# Train model, we can either pass Iterator or Array
documents = DocumentsIterator()
version = str(int(time.time()))
epoch_logger = EpochLogger(outdir + 'model_' + version) # stores model every epoch
model = Doc2Vec(documents, callbacks=[epoch_logger], **params)
model.delete_temporary_training_data(
    keep_doctags_vectors=True, keep_inference=True)
print('Model trained')

# Save model
fname = outdir + 'model_' + version
model.save(fname)
print('Model saved to ' + fname)

# Build embeddings
# We write directly to output file to avoid data loss due to unexpected errors
with open(outdir + 'results_' + version + '.csv', 'w') as f:
    for document in documents:
        f.write(document.tags[0] + ',' + ','.join(['%.16f' %
                                                   num for num in model.infer_vector(document.words)]) + '\n')
print('Saved embeddings to ' + outdir)
