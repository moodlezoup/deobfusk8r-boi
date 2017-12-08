import os
import multiprocessing
from subprocess import call

def makeCommand(apk_path, edges_path, key_path):
    return 'java -jar target/scala-2.12/Argus-SAF-CFG-Extractor.jar %s %s %s' % (apk_path, edges_path, key_path)

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getJobs():
    jobs = []
    outer_output = '/home/ec2-user/output'
    makeDir(outer_output)
    output_parent = outer_output + '/argus' 
    for family in os.listdir('/home/ec2-user/ssd1/amd_data'):
        path = '/home/ec2-user/ssd1/amd_data/' + family
        output_path = output_parent + '/' + family
        makeDir(output_path)
        for apk in os.listdir(path):
            apk_path = path + '/' + apk
            basename = apk.rsplit('.',1)[0]
            edges_path = output_path + '/' + basename + '.edges'
            key_path = output_path + '/' + basename + '.key'
            jobs.append((apk, makeCommand(apk_path, edges_path, key_path)))
    return jobs 


def run(job):
    apk, command = job
    call(command, shell=True)


if __name__ == '__main__':
    jobs = getJobs()
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(run, jobs)
