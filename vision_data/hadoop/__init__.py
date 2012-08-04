import hadoopy
import os

def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def flickr_images(tags, images_per_tag, hdfs_output, api_key=None, api_secret=None, remove_output=False):
    if api_key is None or api_secret is None:
        api_key = os.environ['FLICKR_API_KEY']
        api_secret = os.environ['FLICKR_API_SECRET']
    if remove_output and hadoopy.exists(hdfs_output):
        print('Removing output dir[%s]' % hdfs_output)
        hadoopy.rmr(hdfs_output)
    for tag_num, tag in enumerate(tags):
        hadoopy.writetb(hdfs_output + '/tags/%d' % tag_num, [(images_per_tag, tag)])
    hadoopy.launch_frozen(hdfs_output + '/tags', hdfs_output + '/metadata', _lf('flickr_bulk.py'), cmdenvs={'FLICKR_API_KEY': api_key,
                                                                                                            'FLICKR_API_SECRET': api_secret})
    hadoopy.launch_frozen(hdfs_output + '/metadata', hdfs_output + '/image_metadata', _lf('file_downloader.py'))