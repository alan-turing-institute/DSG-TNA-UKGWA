# Computes statistics about the entities
from doc2vec_helper import DocumentsIterator
import pandas as pd

docs = DocumentsIterator()

counts = []
for doc in docs:
    counts.append(len(doc.words))

df = pd.DataFrame(counts)
df.describe()
# Output:
# count 	357831.000000
# mean 	73.753962
# std 	52.557982
# min 	8.000000
# 25% 	45.000000
# 50% 	61.000000
# 75% 	86.000000
# max 	3493.000000
