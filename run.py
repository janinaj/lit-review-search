import sys, os, math
from scopus_publication import ScopusPublication

def get_strong_co_citing(scopus_pub, shared):
    min_count = math.ceil(scopus_pub.reference_count * shared)

    eids = []
    for eid, count in scopus_pub.co_citing_counts.items():
            if count >= min_count:
                eids.append(eid)

    return eids

def get_strong_co_cited(scopus_pub, shared):
    min_count = math.ceil(seed.citation_count * shared)
    
    eids = []
    for eid, count in seed.co_cited_counts.items():
        if count >= min_count:
            eids.append(eid)

    return eids

def get_strong_citation_relationship(scopus_pub, shared):
    scopus_pub.strong_cit_pubs = set()

    for reference in scopus_pub.references_:
        scopus_pub.strong_cit_pubs.add(reference['eid'])

    for citation in scopus_pub.citations_:
        scopus_pub.strong_cit_pubs.add(citation['eid'])

    scopus_pub.strong_cit_pubs.union(get_strong_co_citing(scopus_pub, shared))
    scopus_pub.strong_cit_pubs.union(get_strong_co_cited(scopus_pub, shared))

    # with open(os.path.join('data', eid, 'top_shared_' + str(top) + '_' + citation_type + '.txt'), 'w') as o:
    #     for top_pub in top_pubs:
    #         o.write(top_pub)
    #         o.write('\n')

def main():
    shared = 0.10
    year = 2013

    review = '84925226708'
    studies_folder = 'data/included-studies'
    output_folder = 'data/scopus-download'

    print('Getting list of included studies..')
    seeds = []
    with open(os.path.join(studies_folder, review, 'included.csv')) as f:
        for line in f:
            seeds.append(line.strip().split(',')[1])

    print('Getting citation space..')
    scopus_pubs = {}
    for seed in seeds:
        scopus_pubs[seed] = ScopusPublication(output_folder, seed)
        scopus_pubs[seed].filter_citations(year)

    print('Getting strong citation relationships..')
    for seed in seeds:
        get_strong_citation_relationship(scopus_pubs[seed], shared)



if __name__ == "__main__":
    main()