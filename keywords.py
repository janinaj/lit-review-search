from scopus_publication import ScopusPublication
from rake_nltk import Rake
from shutil import copyfile
import os

source_folder = ''
output_folder = ''
studies_folder = ''

for file in os.listdir(output_folder):
    if file != '.DS_Store':
        pub = ScopusPublication(output_folder, file)
        
        pub.abstract = pub.abstract.encode('ascii', 'ignore') 
        if pub.abstract != '':
            keywords_file = os.path.join(output_folder, file, 'rake_keywords.txt')
            
            if not os.path.exists(keywords_file):
                try:
                    r = Rake()
                    r.extract_keywords_from_text(pub.abstract)
                    keywords = r.get_ranked_phrases()
                
                    if len(keywords) > 0:
                        with open(keywords_file, 'w') as o:
                            for keyword in keywords:
                                o.write(keyword)
                                o.write('\n')
                except:
                    pass