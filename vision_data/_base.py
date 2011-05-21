import hashlib
import os
import urllib
import subprocess
import shutil


class VisionDataset(object):
    """
    """
    
    def __init__(self, name, data_urls, homepage=None, bibtexs=None,
                 overview=None):
        """
        
        Args:
            name: Dataset name (e.g., voc07, sun09)
            data_urls: Dictionary with keys as (md5_hash, file_name),
                values as lists of urls.  The urls are redundant and are
                attempted in order.
            homepage: A webpage describing the dataset.
            bibtexs: A list of recommended bibtex entries
            overview: A string describing the dataset
        """
        try:
            self._data_root = os.environ['VISION_DATA_ROOT']
        except KeyError:
            raise KeyError('Environmental variable VISION_DATA_ROOT must be set '
                           'to the path where you want to store the data files.')
        self._name = name
        self._data_urls = data_urls
        self._homepage = homepage
        self._bibtexs = bibtexs
        self._overview = overview
        self.dataset_path = '%s/%s/' % (self._data_root, self._name)

    def _unpack_download(self, file_name):
        ext = file_name.split('.', 1)[1]
        dir_name = os.path.dirname(file_name)
        if ext == 'tar':
            cmd = 'tar -xf %s -C %s' % (file_name, dir_name)
        elif ext == 'tar.gz':
            cmd = 'tar -xzf %s -C %s' % (file_name, dir_name)
        elif ext == 'tar.bz2':
            cmd = 'tar -xjf %s -C %s' % (file_name, dir_name)
        else:
            raise ValueError('Extension [%s] not supported' % ext)
        subprocess.call(cmd.split())

    def download(self, force=False):
        if force:
            shutil.rmtree(self.dataset_path)
        if os.path.exists(self.dataset_path):
            return True
        os.makedirs(self.dataset_path)
        for (md5hash, file_name), urls in self._data_urls.items():
            print('Downloading [%s]' % file_name)
            for url in urls:
                # TODO: Make this more robust and check hash
                a = urllib.urlretrieve(url, self.dataset_path + file_name)
                print(a)
                #assert(md5hash == hashlib.md5(data).hexdigest())
                break
        for (md5hash, file_name), urls in self._data_urls.items():
            print('Unpacking [%s]' % file_name)
            self._unpack_download(self.dataset_path + file_name)
            print('Removing Temporary File [%s]' % file_name)
            os.remove(self.dataset_path + file_name)
