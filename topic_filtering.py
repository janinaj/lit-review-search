import os, subprocess
from scopus_publication import ScopusPublication

HDP_PATH = 'PATH_TO_HDP_FOLDER'
HDP_COMMAND = os.path.join(HDP_PATH, 'hdp')
PRINT_COMMAND = os.path.join(HDP_PATH, 'print.topics.R')

def format_lda_c(str_input):
    global words
    global counter

    counts = Counter(str_input)
    lda_c_string = ''

    for word, count in counts.items():                   
        if word not in words:
            words.append(word)
            counter += 1

            idx = counter
        else:
            idx = words.index(word)

        lda_c_string += ' ' + str(idx) + ':' + str(count)

    return str(len(counts)), lda_c_string

def get_topics(topic_output_folder, pubs, text_sources = ['title']):
    if not os.path.exists(topic_output_folder):
        os.mkdir(topic_output_folder)

    text_file_path = os.path.join(topic_output_folder, 'text.txt')

    topic_dist_file = os.path.join(topic_output_folder, 'final.topics')
    vocab_file = os.path.join(topic_output_folder, 'vocab.txt')
    topic_cluster_file = os.path.join(topic_output_folder, 'topics.txt')
    with open(text_file_path, 'w') as o:
        for pub in pubs:
            if 'title' in text_sources:
                o.write(pub.title)
                o.write('\n')
            if 'abstract' in text_sources:
                o.write(pub.abstract)
                o.write('\n')

    #input('{} --train_data {} --directory {} --random_seed 0'.format(HDP_COMMAND, text_file_path, topic_output_folder))
    subprocess.call('{} --train_data {} --directory {} --random_seed 0'.format(HDP_COMMAND, text_file_path, topic_output_folder), shell=True)
    subprocess.call('{} {}  {} {}'.format(PRINT_COMMAND, topic_dist_file, vocab_file, topic_cluster_file), shell=True)

def cluster_documents():
    topic_cluster_file = os.path.join(topic_output_folder, 'topics.txt')


def select_topic_clusters(user_defined_clusters = None):
    if user_defined_clusters == None:
        pass
    