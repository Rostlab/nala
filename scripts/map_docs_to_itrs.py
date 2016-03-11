import random
import glob
import os

itrs = list(range(42,60+1))

def get_itr_docs(itr_number):
    folder = '../resources/bootstrapping/iteration_{}/candidates/html'.format(itr_number)
    for filename in glob.glob(str(folder + "/*.html")):
        filename = os.path.basename(filename)
        filename = filename.replace('.plain.html', '')
        filename = filename.replace('.html', '')
        print(str(itr_number) + " " + filename)

for itr in itrs:
    get_itr_docs(itr)
