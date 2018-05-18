import os, subprocess
from scopus_publication import ScopusPublication

HDP_PATH = 'PATH_TO_HDP_FOLDER'
HDP_COMMAND = os.path.join(HDP_PATH, 'hdp')
PRINT_COMMAND = os.path.join(HDP_PATH, 'print.topics.R')

get_topics(topic_output_folder, eids, text_sources = ['title, abstract']):
    text_file_path = os.path.join(topic_output_folder, 'text.txt')

    topic_dist_file = os.path.join(topic_output_folder, 'final.topics')
    vocab_file = os.path.join(topic_output_folder, 'vocab.txt')
    topic_cluster_file = os.path.join(topic_output_folder, 'topics.txt')
    with open(text_file_path) as o:
        for pub in pubs:
            if 'title' in text_sources:
                o.write(pub.title)
                o.write('\n')
            if 'abstract' in text_sources:
                o.write(pub.abstract)
                o.write('\n')

    subprocess.run('.{} --train_data {} --directory {} --random_seed 0'.format(HDP_COMMAND, text_file_path, topic_output_folder), shell=True, check=True)
    subprocess.run('.{} {}  {} {}'.format(PRINT_COMMAND, topic_dist_file, vocab_file, topic_cluster_file), shell=True, check=True)

cluster_documents():
    