import json
import requests
from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.utils.readers import HTMLReader
from nala.bootstrapping.iteration import Iteration
import shutil
import os

username = 'your user'
password = 'your password'
url = 'https://www.tagtog.net/api/0.1/documents'


def run():
    itr = Iteration()
    itr.docselection(just_caching=True, nr=100)
    itr.before_annotation(10)


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


def download(n):
    auth = requests.auth.HTTPBasicAuth(username=username, password=password)
    cnd_dir = 'resources/bootstrapping/iteration_{}/candidates/html'.format(n)
    rev_dir = 'resources/bootstrapping/iteration_{}/reviewed'.format(n)

    ids = [file.replace('.html', '') for file in os.listdir(cnd_dir)]

    for tagtog_id in ids:
        params = {'project': 'nala', 'output': 'ann.json', 'owner': 'jmcejuela',
                  'ids': tagtog_id, 'member': username, 'idType': 'tagtogID'}
        response = requests.get(url, params=params, auth=auth)
        if response.status_code == 200:
            try:
                json.dump(response.json(), open(os.path.join(rev_dir, '{}.ann.json'.format(tagtog_id)), 'w'))
                print('downloaded', tagtog_id)
            except json.JSONDecodeError:
                print('error', tagtog_id, response.text)


def validate(n):
    cnd_dir = 'resources/bootstrapping/iteration_{}/candidates/html'.format(n)
    rev_dir = 'resources/bootstrapping/iteration_{}/reviewed'.format(n)

    data = HTMLReader(cnd_dir).read()
    print(len(data))
    AnnJsonAnnotationReader(rev_dir).annotate(data)
    print(len(data))

run()
# upload(22)
# download(22)
# validate(22)