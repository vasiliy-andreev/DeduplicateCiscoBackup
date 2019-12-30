import re
import os
import filecmp
from datetime import date

prefs = ['ASA',
'ASR',
'C2950',
'C2960',
'AP_',
]

lastConfChange = re.compile('! Last configuration.+?\n')
NVRAMConfigUpdate = re.compile('! NVRAM config last updated.+?\n')
NTP = re.compile('ntp clock-period.+?\n')
ASA = re.compile('Written by.+?\n')
CurrConf = re.compile('Current configuration\s:\s\d+\sbytes\n')
#array of files
files = []
for pref in prefs:
    for file in os.listdir('.'):
        if file.startswith(pref):
            files.append(file)
#deleting regex lines
for file in files:
    print('Processing file', file)
    with open(file) as f:
        a = f.read()
    try:
        a = a.replace((CurrConf.findall(a))[0],'')
    except:
        pass
    try:
        a = a.replace((NTP.findall(a))[0],'')
    except:
        pass
    try:
        a = a.replace((NVRAMConfigUpdate.findall(a))[0],'')
    except:
        pass
    try:
        a = a.replace((lastConfChange.findall(a))[0],'')
    except:
        pass
    try:
        a = a.replace((ASA.findall(a))[0],'')
    except:
        pass
    with open(file, 'w') as f:
        f.write(a)
#delete useless clones
for file in files:
	for filea in files:
		if file == filea:
			continue
		try:
			if filecmp.cmp(file,filea):
				try:
					print ('removing ',filea)
					os.remove(filea)
				except:
					continue
		except:
			continue
#remaining files to tar archive
tarname = 'Backup_'+str(date.today())+'.tar'
files = []
for pref in prefs:
    for file in os.listdir('.'):
        if file.startswith(pref):
            files.append(file)
for file in files:
    command = 'tar --append --file={tarname} {file}'.format(tarname = tarname,file = file)
    os.system(command)
#delete junk files
filesInTar = os.popen('tar -tvf {tarname}'.format(tarname=tarname)).read()
for file in files:
    if file in filesInTar:
        os.system('rm -f '+file)
