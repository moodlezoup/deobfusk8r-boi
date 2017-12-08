import os
import multiprocessing
from subprocess import call

def makeCommand(apk_path, edges_path, key_path):
    return 'java -jar target/scala-2.12/Argus-SAF-CFG-Extractor.jar %s %s %s' %
        (apk_path, edges_path, key_path)

def getJobs():
    jobs = []
    for family in os.listdir('/home/ec2-user/ssd1/amd_data'):
        path = '/home/ec2-user/ssd1/amd_data/' + family
        output_path = '/home/ec2-user/output/argus/' + family
        for apk in os.listdir(path):
            apk_path = path + '/' + apk
            basename = apk.rsplit('.',1)[0]
            edges_path = output_path + '/' + basename + '.edges'
            key_path = output_path + '/' + basename + '.key'
            jobs.append((apk, makeCommand(apk_path, edges_path, key_path)))
    return jobs 


def run(job):
    apk, command = job
    print apk
    call(job, shell=True)


if __name__ == '__main__':
    jobs = getJobs()
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(run, jobs)
