########
# This script reads text files from an input list containing filenames and
# computes entities using the package spacy. Files are processed on parelell
# according to the number of threads passed as input.
# The output files are saved on the current directory.
# input: file_list with filenames to be processed (full path)
# threads: number of threads to run in pararell
# output: json file with same name as input with dictionary format style.
# on each line = indentity: [token, position]
########

import sys
import spacy
import json
import os
import itertools
import concurrent.futures
import time


start = time.perf_counter()

if len(sys.argv) < 3:
    print("Usage: %s <file_list> <threads>\n" % sys.argv[0])
    exit(1)


def grouper(iterable, n, fillvalue=None):
    """

    https://docs.python.org/3/library/itertools.html#itertools-recipes
    Collect data into fixed-length chunks or blocks
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def multi_threading(target, iterable, batch_size):
    """

    target - function to run
    iterable - iterable object to loop through
    batch_size - number of parallel threads to run
    """
    for batch in grouper(iterable, batch_size):
        # print(f'batch {batch}')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda arg: target(arg) if arg else None, batch)
            # results = (executor.submit(lambda arg: target(arg) if arg else None, item) for item in batch)
            # for fut in concurrent.futures.as_completed(results):
                # fut.result()


class NamedEntityRecogniser:
    def __init__(self, tgt_path):
        """
        tgt_path - path to store json files with recognised entities
        """
        self.nlp = spacy.load("en_core_web_lg")
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
threads = int(sys.argv[2])

# make input list an iterable
task = (FILE_NAME.split()[0] for FILE_NAME in input)

# call the multithread function
multi_threading(lambda name: ent_recogniser(PATH, name), task, threads)


end = time.perf_counter()
print(round(end-start), 2)
