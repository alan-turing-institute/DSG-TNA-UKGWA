import tagme
import os
import json
from collections import Counter


class NamedEntityRecogniserTagMe:

    def __init__(self, token, tgt_path, rho_score=0.1):
        """

        token - TagMe token
        tgt_path - path to store json files with recognised entities
        rho_score - likelihood of an annotation being correct

        """
        self.token = token
        tagme.GCUBE_TOKEN = self.token
        self.tgt_path = tgt_path
        self.rho_score = rho_score

    def __call__(self, src_path, filename):
        """

        src_path - path to web-page file
        filename - name of web-page file
        """
        with open(os.path.join(src_path, filename), 'r') as file:
            doc = ' '.join(line.strip() for line in file)
            cnt = Counter(ent.entity_title for ent in tagme.annotate(doc).get_annotations(self.rho_score))
        if cnt:
            with open(f'{os.path.join(self.tgt_path, os.path.splitext(filename)[0])}.json', 'w') as tgt:
                json.dump(dict(cnt), tgt)