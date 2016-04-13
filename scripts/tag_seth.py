# import os
#
# from nalaf.utils.annotation_readers import SETHAnnotationReader, DownloadedSETHAnnotationReader
# from nalaf.utils.readers import PMIDReader
#
# pmids = [file[:-4] for file in
#          os.listdir('/home/abojchevski/projects/nala/resources/corpora/seth/annotations')]
# print(len(pmids))
# dataset = PMIDReader(pmids).read()
#
#
#
# DownloadedSETHAnnotationReader('/home/abojchevski/projects/nala/resources/corpora/seth/annotations').annotate(dataset)
from nala.utils.corpora import get_corpus

data = get_corpus('SETH')

for ann in data.annotations():
    print(ann)