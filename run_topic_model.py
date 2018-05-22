import sys, os, citation_filtering, topic_filtering
from scopus_publication import ScopusPublication

def main():
    shared = 0.10
    year = 2018

    review = 'seeds'
    studies_folder = ''
    data_folder = ''
    topic_output_folder = ''
    output_file = 'rake_results.csv'

    print('Getting list of included studies..')
    seeds = []
    with open(os.path.join(studies_folder, review, 'included.csv')) as f:
        for line in f:
            seeds.append(line.strip().split(',')[1])

    print('Getting citation space..')
    scopus_pubs = {}
    for seed in seeds:
        scopus_pubs[seed] = ScopusPublication(data_folder, seed)
        scopus_pubs[seed].filter_citations(year)
        scopus_pubs[seed].get_co_cited_eids()
        

    print('Getting strong citation relationships..')
    strong_cite_related_pub_eids = set()
    for seed in seeds:
        strong_cite_related_pub_eids = strong_cite_related_pub_eids.union(citation_filtering.get_strong_citation_relationship(scopus_pubs[seed], shared))

    strong_cite_related_pubs = []
    for eid in strong_cite_related_pub_eids:
        strong_cite_related_pubs.append(ScopusPublication(data_folder, eid, False))

    print('Getting topics..')
    topic_filtering.get_topics(topic_output_folder, strong_cite_related_pubs)

    print('Clustering documents..')
    cluster_documents(topic_output_folder, strong_related_pubs)

    print('Filtering by topic cluster..')
    select_topic_clusters(topic_output_folder, strong_related_pubs)        

if __name__ == "__main__":
    main()