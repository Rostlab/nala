import random
import glob
import os

"""
The purpose of this script was to randomly assign to members the last iterations
of annotations (until iteration_60). The purpose was to mix in both training
and test iterations (and IAA iterations) without members being aware which
were which and so not to bias their annotations.
"""

itrs = list(range(42,60+1))
itrs_size = len(itrs) #19
annotators = { 'abojchevski' : [], 'jmcejuela' : [], 'cuhlig' : [] }
test = []
IAA = []

#9 iterations for testing
#3 iterations for IAA, all 3 annotators (jmcejuela, abojchevski, cuhlig)
#6 iterations / 3 --> 2 per annotator (jmcejuela, abojchevski, cuhlig)
#10 iterations left for training / 2 --> 5 per annotator (jmcejuela, cuhlig)
#In the end:
#   abojchevski: 5 testing
#   jmcejuela: 5 training + 5 testing
#   cuhlig: 5 training + 5 testing

random.shuffle(itrs)

# IAA
for i in range(0, 3):
    elem = itrs.pop()
    IAA.append(elem)
    for key in annotators.keys():
        annotators[key].append(elem)

# rest test
for key in annotators.keys():
    for i in range(0, 2):
        elem = itrs.pop()
        test.append(elem)
        annotators[key].append(elem)

test.extend(IAA)

# training
for key in ['jmcejuela', 'cuhlig']:
    for i in range(0, 5):
        elem = itrs.pop()
        annotators[key].append(elem)

def get_itr_docs(itr_number):
    folder = '../resources/bootstrapping/iteration_{}/candidates/html'.format(itr_number)
    for filename in glob.glob(str(folder + "/*.html")):
        filename = os.path.basename(filename)
        filename = filename.replace('.plain.html', '')
        filename = filename.replace('.html', '')
        print("\t", filename)

# Finally, print

print("test", len(test), test)
for i in test:
    get_itr_docs(i)

print("IAA", len(IAA), IAA)
for i in IAA:
    get_itr_docs(i)

print()

for annotator, itrs in annotators.items():
    random.shuffle(itrs)  # randomize training & test
    print(annotator, len(itrs), itrs)
    for i in itrs:
        get_itr_docs(i)
