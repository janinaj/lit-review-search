from lxml import etree
from datetime import datetime
import os, json, urllib2, time, xml.etree.ElementTree as ET

API_KEY = ''
CURRENT_YEAR = 2018

class ScopusPublication():
    @property
    def eid(self):
        return self.eid_

    @property
    def references(self):
        return self.references_

    @property
    def reference_count(self):
        return len(self.references_)

    @property
    def citations(self):
        return self.citations_

    @property
    def citation_count(self):
        return len(self.citation_)

    @property
    def co_citing_eids(self):
        return self.co_citing_eids_

    @property
    def co_cited_eids(self):
        return self.co_cited_eids_

    @property
    def abstract(self):
        return self.abstract_

    @property
    def pub_year(self):
        return self.pub_year_

    def __init__(self, data_folder, eid):
        self.eid_ = eid.rjust(10, '0')
        self.data_folder_ = data_folder
        self.pub_directory_ = os.path.join(data_folder, self.eid_)
        
        #create publication directory if it does not exist yet
        if not os.path.exists(self.pub_directory_):
            os.makedirs(self.pub_directory_)

        self.references_ = []
        self.citations_ = []
        self.co_citing_eids_ = []
        self.co_cited_eids_ = []

        reference_file = os.path.join(data_folder, self.eid_, 'references.xml')

        # download file containing references and abstract if it does not exist
        if not os.path.exists(reference_file):
            self.download_reference_file(reference_file)
        
        self.get_reference_file(reference_file)
        self.get_reference_eids()

        self.get_abstract()
        self.get_year()

        self.citations_folder_ = os.path.join(self.pub_directory_, 'citations')

        if not os.path.exists(self.citations_folder_):
            self.download_citation_files()
        self.get_citation_eids()

    def get_abstract(self):
        self.abstract_ = ''
        if self.reference_xml_ != None:
            abstract_xmls = self.reference_xml_.xpath('/ns0:abstracts-retrieval-response/ns0:coredata/dc:description/abstract[@xml:lang="eng"]', \
                namespaces={'ns0':'http://www.elsevier.com/xml/svapi/abstract/dtd', \
                'dc':'http://purl.org/dc/elements/1.1/'})

            for abstract_xml in abstract_xmls:
                paragraph_xmls = abstract_xml.xpath('ns3:para', namespaces={'ns3':'http://www.elsevier.com/xml/ani/common'})
                for paragraph_xml in paragraph_xmls:
                    self.abstract_ = ' '.join([self.abstract_, paragraph_xml.xpath('string(.)')])

    def get_year(self):
        try:
            pub_date = self.reference_xml_.xpath('/ns0:abstracts-retrieval-response/ns0:coredata/ns1:coverDate', \
            namespaces={'ns0':'http://www.elsevier.com/xml/svapi/abstract/dtd', \
            'ns1': 'http://prismstandard.org/namespaces/basic/2.0/'})

            self.pub_year_ = datetime.strptime(pub_date[0].text, '%Y-%m-%d').year
        except Exception as e:
            self.pub_year_ = 1900

    def download_reference_file(self, reference_file):
        try:
            abstract_url = 'https://api.elsevier.com/content/abstract/scopus_id/{}?apiKey={}'.format(self.eid_, API_KEY)
            
            #change ET to lxml
            xml_file = urllib2.urlopen(abstract_url, timeout = 1000)
            data = xml_file.read()
            xml_file.close()
            xml = ET.fromstring(data)

            # save xml data to file
            with open(os.path.join(reference_file), 'w') as f:
                f.write(ET.tostring(xml))

        except Exception as e:
            print('Error getting reference file: ' + self.eid_)
            print(e)
        
        time.sleep(5)

    def get_reference_file(self, reference_file):
        try:
            tree = etree.parse(reference_file)
            self.reference_xml_ = tree.getroot()
        except Exception as e:
            self.reference_xml_ = None

    def get_reference_eids(self):
        if self.reference_xml_ != None:
            references = self.reference_xml_.xpath('/ns0:abstracts-retrieval-response/item/bibrecord/tail/bibliography/reference', \
                namespaces={'ns0':'http://www.elsevier.com/xml/svapi/abstract/dtd'})

            for reference in references:
                title = reference.xpath('ref-info/ref-title/ref-titletext')
                ref_eid = reference.xpath('ref-info/refd-itemidlist/itemid[@idtype="SGR"]')[0].text

                if ref_eid not in self.references_:
                    if len(title) > 0:
                        self.references_.append({'eid' : ref_eid, 'title' : title[0].text})
                    else:
                        self.references_.append({'eid' : ref_eid, 'title' : None})

    def get_citation_eids(self):
        if os.path.exists(self.citations_folder_):
            for file in os.listdir(self.citations_folder_):
                if '.json' in file:
                    with open(os.path.join(self.citations_folder_, file), 'r') as f:
                        json_data = json.load(f)

                        if 'entry' in json_data['search-results']:
                            for result in json_data['search-results']['entry']:
                                if 'eid' in result:
                                    cit_eid = result['eid'].replace('2-s2.0-', '')

                                    if 'dc:title' in result:
                                        title = result['dc:title'].replace('<inf>', '').replace('</inf>', '').replace('<sup>', '').replace('</sup>', '')
                                    else:
                                        title = ''

                                    try:
                                        year = datetime.strptime(result['prism:coverDate'], '%Y-%m-%d').year
                                    except:
                                        year = None

                                    #add year
                                    self.citations_.append({'eid' : cit_eid, 'title' : title, 'year' : year})

    def download_citation_files(self):
        try:         
            if not os.path.exists(self.citations_folder_):
                os.makedirs(self.citations_folder_)

            current_year = 2018
            count_results = 0

            year = 1900 #start from 1900 because some publication years are wrong
            while year <= current_year:
                page_count = 0
                while True:
                    json_file = urllib2.urlopen('https://api.elsevier.com/content/search/scopus?' + \
                        'query=refeid(2-s2.0-{})&apiKey={}&date={}&count=200&start={}'.format(self.eid_, API_KEY, year, page_count * 200))
                    data = json_file.read()

                    json_data = json.loads(data)
                    results = int(json_data['search-results']['opensearch:totalResults'])

                    if page_count == 0 and results > 5000:
                        print('More than 5000: ' + self.eid_)
                        print('Year: ' + str(year))

                    if results == 0 or 'entry' not in json_data['search-results']:
                        break

                    count_results += len(json_data['search-results']['entry'])

                    #save citations to file
                    with open(os.path.join(self.citations_folder_, str(year) + '-' + str(page_count) + '.json'),'w') as f:
                        f.write(data)

                    page_count += 1

                    if page_count * 200 > results:
                        break

                year += 1
        except urllib2.HTTPError:
            print('Error getting citations: ' + self.eid)

        time.sleep(5)

    def filter_citations(self, year):
        filtered_citations = []
        for citation in self.citations_:
            if citation['year'] <= year:
                filtered_citations.append(citation)

        self.citations_ = filtered_citations
        self.get_cociting_eids() #update co


    def get_cociting_eids(self):
        co_citing_eids = {}

        for reference in self.references_:
            pub = ScopusPublication(self.data_folder_, reference['eid'])

            for citation in pub.citations:
                if citation['eid'] != self.eid_:
                    if citation['eid'] not in co_citing_eids.keys():
                        co_citing_eids[citation['eid']] = citation
                        co_citing_eids[citation['eid']]['count'] = 0

                    co_citing_eids[citation['eid']]['count'] += 1

        self.co_citing_eids = co_citing_eids.values()

    def get_co_cited_eids(self):
        pass