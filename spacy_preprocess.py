import spacy
import json
import os


class NamedEntityRecogniser:
    def __init__(self, tgt_path):
        """

        tgt_path - path to store json files with recognised entities
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.tgt_path = tgt_path

    def __call__(self, src_path, filename):
        """
        Create json file with the same name as original file
        
        src_path - path to web-page file
        filename - name of web-page file
       """
        ent_dict = {}
        with open(os.path.join(src_path, filename), 'r') as file:
            doc = self.nlp(' '.join(line.strip() for line in file))

            for ent in doc.ents:
                ent_data = (ent.text, ent.start_char, ent.end_char)
                if ent.label_ not in ent_dict:
                    ent_dict[ent.label_] = [ent_data]
                else:
                    ent_dict[ent.label_].append(ent_data)
        if ent_dict:
            with open(f'{os.path.join(self.tgt_path, os.path.splitext(filename)[0])}.json', 'w') as tgt:
                json.dump(ent_dict, tgt)