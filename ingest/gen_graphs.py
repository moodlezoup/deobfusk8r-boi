import os
import multiprocessing
from subprocess import call


def getFilePaths():
    file_paths = []
    for family in os.listdir('~/amd_data'):
        path = '~/amd_data/' + family
        for apk in os.listdir(path):
            file_paths.append(path + '/' + apk)
    return file_paths


def genGraphs(file_path):
    print file_path
    call('java -jar flowdroid/target/flowdroid-cfg-0.1.0.jar ' + file_path + ' ~/sdk/platforms')


if __name__ == '__main__':
    file_paths = getFilePaths()
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(genGraphs, file_paths)