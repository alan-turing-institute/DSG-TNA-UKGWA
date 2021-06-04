########
# This script reads text files from an input list containing filenames and
# compute the entities.
# The script saves json files on the current directory.
# output: json file with same name as input with dictionary format style.
# on each line = indentity: [token, position]
########

import sys
import spacy
import json
import os


if len(sys.argv) < 2:
    print("Usage: %s <file_list> \n" % sys.argv[0])
    exit(1)


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
            doc = self.nlp(' '.join([line.strip() for line in file]))
            for ent in doc.ents:
                ent_data = (ent.text, ent.start_char, ent.end_char)
                if ent.label_ not in ent_dict:
                    ent_dict[ent.label_] = [ent_data]
                else:
                    ent_dict[ent.label_].append(ent_data)
        if ent_dict:
            # save json file on current dir with same name as input + .json
            with open(f'{os.path.basename(filename)}.json', 'w') as tgt:
            # with open(f'{os.path.join(self.tgt_path, os.path.splitext(filename)[0])}.json', 'w') as tgt:
                json.dump(ent_dict, tgt)


# Initialise envionment
PATH = os.getcwd()
ent_recogniser = NamedEntityRecogniser(PATH)
input = open(sys.argv[1], "r").readlines()

# loop over file list
for FILE_NAME in input:
    FILE_NAME = FILE_NAME.split()[0]
    ent_recogniser(PATH, FILE_NAME)
