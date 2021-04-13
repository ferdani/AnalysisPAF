import os

samples = []

class sample(object):
  def __init__(self,name, cores, split = False):
    self.name  = name
    self.cores = str(cores)
    if not(split):
      self.command = "root -l -b -q 'RunAnalyserPAF.C(\"" + self.name + "\"    , \"WZ\"," + self.cores + ")'"
    else:
      self.command = "root -l -b -q 'RunAnalyserPAF.C(\"" + self.name + "\"    , \"WZ\"," + self.cores + ", -" + split+")'"
    samples.append(self)

def createsh(text, numb):
  textfile = open("/mnt_pool/ciencias_users/user/carlosec/AnalysisPAF/plotter/WZ/submit_" + str(numb) + ".sh", "w")
  textfile.write(text)
  textfile.close()

base = """cd /mnt_pool/ciencias_users/user/carlosec/AnalysisPAF/\nsource /cms/slc6_amd64_gcc530/external/gcc/5.3.0/etc/profile.d/init.sh; source /cms/slc6_amd64_gcc530/external/python/2.7.11-giojec2/etc/profile.d/init.sh; source /cms/slc6_amd64_gcc530/external/python/2.7.11-giojec2/etc/profile.d/dependencies-setup.sh; source /cms/slc6_amd64_gcc530/external/cmake/3.5.2/etc/profile.d/init.sh;source /opt/root6/bin/thisroot.sh\nsource /opt/PAF/PAF_setup.sh\n"""

#sample("ZZZ",16)
sample("WZZ",16)
sample("WWZ",16)
sample("WWW",16)
sample("ZZTo4L", 16)
sample("WZTo3LNu", 16)
#sample("WWTo2L2Nu",60)

for i in range(len(samples)):
  createsh(base + "\n" + samples[i].command, i)
  os.system("qsub -q batch -l nodes=1:ppn="+ samples[i].cores +" submit_"+ str(i) + ".sh")
  #os.remove("/mnt_pool/ciencias_users/user/carlosec/AnalysisPAF/plotter/WZ/submit_" + str(i) + ".sh")



