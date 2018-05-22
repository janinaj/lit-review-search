import sys, os, csv, codecs, citation_filtering
from scopus_publication import ScopusPublication

def main():
    shared = 0.10
    year = 2018

    review = 'seeds'
    studies_folder = ''
    data_folder = ''
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

    print('Getting seed keywords..')
    seed_keywords = set()
    for seed in seeds:
        seed_keywords = seed_keywords.union(scopus_pubs[seed].rake_keywords)

    bigram_trigram_keywords = set()
    for seed_keyword in seed_keywords:
        total_words = len(seed_keyword.split())
        if total_words == 2 or total_words == 3:
            bigram_trigram_keywords.add(seed_keyword)

    print('Filtering by keywords..')
    strong_related_pubs = []
    for strong_cite_related_pub in strong_cite_related_pubs:
        if len(bigram_trigram_keywords.intersection(strong_cite_related_pub.rake_keywords)) > 0:
            strong_related_pubs.append(strong_cite_related_pub)

    print('Writing results to file..')
    with codecs.open(output_file, 'w', 'utf-8') as o:
        fieldnames = ['SCOPUS_ID', 'TITLE', 'ABSTRACT']
        writer = csv.DictWriter(o, delimiter = '\t', fieldnames = fieldnames)
        writer.writeheader()

        for strong_related_pub in strong_related_pubs:
            writer.writerow({'SCOPUS_ID' : strong_related_pub.eid, 'TITLE' : strong_related_pub.title, 'ABSTRACT' : strong_related_pub.abstract})

if __name__ == "__main__":
    main()