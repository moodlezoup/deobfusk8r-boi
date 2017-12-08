import os
import multiprocessing
from subprocess import call

def makeCommand(apk_path, edges_path, key_path, tmp_data_path):
    return 'java -jar target/scala-2.12/Argus-SAF-CFG-Extractor.jar %s %s %s %s' % (apk_path, edges_path, key_path, tmp_data_path)

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

tmp_container = '/home/ec2-user/argus-tmp/'
def getJobs():
    jobs = []
    outer_output = '/home/ec2-user/output'
    makeDir(outer_output)
    output_parent = outer_output + '/argus' 
    makeDir(output_parent)
    makeDir(tmp_container)
    for family in os.listdir('/home/ec2-user/ssd1/amd_data'):
        path = '/home/ec2-user/ssd1/amd_data/' + family
        output_path = output_parent + '/' + family
        makeDir(output_path)
        for apk in os.listdir(path):
            apk_path = path + '/' + apk
            basename = apk.rsplit('.',1)[0]
            edges_path = output_path + '/' + basename + '.edges'
            key_path = output_path + '/' + basename + '.key'
            tmp_data_path = tmp_container + family + '-' + basename
            command = makeCommand(apk_path, edges_path, key_path, tmp_data_path)
            jobs.append((apk, tmp_data_path, command))
    return jobs 


def run(job):
    apk, tmp_data_path, command = job
    print apk
    call(command, shell=True)
    call("rm -rf " + tmp_data_path, shell=True)


if __name__ == '__main__':
    jobs = getJobs()
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(run, jobs)
