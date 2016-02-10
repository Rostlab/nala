import json
import requests
from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.utils.readers import HTMLReader
from nala.bootstrapping.iteration import Iteration
import shutil
import os
import sys

url = 'https://www.tagtog.net/api/0.1/documents'

try:
    # username = sys.argv[1]
    # password = sys.argv[2]
    # if len(sys.argv) > 3:
    #     itr_number = sys.argv[3]
    # else:
    #     itr_number = None
    username = 'abojchevski'
    password = 'nt?tagtog'
except:
    print("You must pass in tagtog username and password")
    raise



def run():
    itr = Iteration(iteration_nr=30)
    print("Running iteration #: ", itr.number)
    # itr.docselection(10)
    # itr.docselection(just_caching=True, nr=100)
    itr.before_annotation(10)
    return itr.number


def upload(n):
    auth = requests.auth.HTTPBasicAuth(username=username, password=password)
    params = {'project': 'nala', 'output': 'null', 'owner': 'jmcejuela'}
    iter_dir = 'resources/bootstrapping/iteration_{}/candidates'.format(n)

    file = shutil.make_archive(iter_dir, 'zip', iter_dir)
    files = {'files': open(file, 'rb')}

    response = requests.put(url, params=params, auth=auth, files=files)
    if response.status_code == 200:
        for id in response.json()['ids']:
            print('uploaded', id)
            os.rename(os.path.join(os.path.join(iter_dir, 'html'), '{}.html'.format(id.split('-')[-1])),
                      os.path.join(os.path.join(iter_dir, 'html'), '{}.html'.format(id)))

        print("Warnings:", response.json()['warnings'])
        return response.json()['ids']
    else:
        raise Exception(response.status_code, response.text)


def download(n, ids=None):
    cnd_dir = 'resources/bootstrapping/iteration_{}/candidates/html'.format(n)
    if not ids:
        ids = [file.replace('.html', '') for file in os.listdir(cnd_dir)]

    rev_dir = 'resources/bootstrapping/iteration_{}/reviewed'.format(n)
    if not os.path.exists(rev_dir):
        os.makedirs(rev_dir)

    auth = requests.auth.HTTPBasicAuth(username=username, password=password)

    for tagtog_id in ids:
        params = {'project': 'nala', 'output': 'ann.json', 'owner': 'jmcejuela',
                  'ids': tagtog_id, 'member': username, 'idType': 'tagtogID'}
        response = requests.get(url, params=params, auth=auth)
        if response.status_code == 200:
            try:
                json.dump(response.json(), open(os.path.join(rev_dir, '{}.ann.json'.format(tagtog_id)), 'w'))
                print('downloaded', tagtog_id)
            except json.JSONDecodeError:
                print('error', tagtog_id, response.status_code, response.text)
        else:
            print('error', tagtog_id, response.status_code, response.text)


def validate(n, ids):
    cnd_dir = 'resources/bootstrapping/iteration_{}/candidates/html'.format(n)
    rev_dir = 'resources/bootstrapping/iteration_{}/reviewed'.format(n)

    data = HTMLReader(cnd_dir).read()
    print(len(data))
    AnnJsonAnnotationReader(rev_dir, delete_incomplete_docs=True).annotate(data)
    print(len(data))

itr_number = run()

# ids = upload(itr_number)
# print('The following documents are now uploaded to tagtog', ids)
# print('Now review them on tagtog')
# while True:
#     answer = input('Are you done reviewing the documents? ')
#     if answer.lower() in ['yes', 'y']:
#         break
#
# download(itr_number, ids)
# validate(itr_number, ids)
# print(":-) Congrats for finishing Iteration #", itr_number)
