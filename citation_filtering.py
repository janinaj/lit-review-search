import math, os
from scopus_publication import ScopusPublication

def get_strong_co_citing(scopus_pub, shared):
    min_count = math.ceil(scopus_pub.reference_count * shared)

    eids = []
    for eid, count in scopus_pub.co_citing_counts.items():
            if count >= min_count:
                eids.append(eid)

    return eids

def get_strong_co_cited(scopus_pub, shared):
    min_count = math.ceil(scopus_pub.citation_count * shared)
    
    eids = []
    for eid, count in scopus_pub.co_cited_counts.items():
        if count >= min_count:
            eids.append(eid)

    return eids

def get_strong_citation_relationship(scopus_pub, shared, store = False, overwrite = False):
    strong_related_pub_eids = set()

    for reference in scopus_pub.references_:
        strong_related_pub_eids.add(reference['eid'])

    for citation in scopus_pub.citations_:
        strong_related_pub_eids.add(citation['eid'])

    strong_related_pub_eids = strong_related_pub_eids.union(get_strong_co_citing(scopus_pub, shared))
    strong_related_pub_eids = strong_related_pub_eids.union(get_strong_co_cited(scopus_pub, shared))

    if store:
        if overwrite or not os.path.exists():
            with open(os.path.join('data', scopus_pub.eid, 'top_shared.txt'), 'w') as o:
                for pub in strong_related_pub_eids:
                    o.write(pub)
                    o.write('\n')

    return strong_related_pub_eids