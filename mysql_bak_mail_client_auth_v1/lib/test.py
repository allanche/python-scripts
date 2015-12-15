__author__ = 'allanche'
import os
import tarfile




tar = tarfile.open("/data/sh/test.tar.gz","w:gz")
for root,dir,files in os.walk("/data/sh"):
    for file in files:
        fullpath = os.path.join(root,file)
        tar.add(fullpath)
tar.close()

def extract(tar_path, target_path):
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception, e:
        raise Exception, e

