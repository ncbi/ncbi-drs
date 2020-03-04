import re
import subprocess

pkg = {} # version info from dpkg
pip = {} # version info from pip
rel = '' # version info from lsb-release

# build the image and get its ID
image = subprocess.run('docker build -qq .', shell=True, capture_output=True, check=True, encoding='utf-8').stdout.strip()

# query pip for version info of installed modules
for l in subprocess.run('docker run --rm '+image+' pip3 freeze', shell=True, capture_output=True, check=True, encoding='utf-8').stdout.split():
    m = re.match(r'^([^=]+)==(.+)$', l)
    if m: pip[m[1]] = m[2]

# query dpkg for version info of installed packages
for l in subprocess.run('docker run --rm '+image+' dpkg-query -W --showformat \'${Package}=${Version}\\\n\'', shell=True, capture_output=True, check=True, encoding='utf-8').stdout.split():
    m = re.match(r'^([^=]+)=(.+)$', l)
    if m: pkg[m[1]] = m[2]

# query lsb-release for ubuntu release number
for l in subprocess.run('docker run --rm '+image+' cat /etc/lsb-release', shell=True, capture_output=True, check=True, encoding='utf-8').stdout.split():
    m = re.match(r'^DISTRIB_RELEASE=(.+)$', l)
    if m: rel = m[1]

# rewrite the Dockerfile with the pinned versions
with open('Dockerfile', 'r') as f:
    st = 0
    for l in f:
        l = l.rstrip()
        if st == 0:
            if re.match('^FROM\s+', l) and rel:
                l = re.sub('ubuntu:latest', 'ubuntu:'+rel, l) # pin ubuntu version
            if 'apt-get -qq install' in l:
                st = 1
            print(l)
            continue
        if st == 1:
            if re.match(r'^\s*>>\s*', l):
                st = 2
                print(l)
                continue
            n = l.strip().rstrip('\\').strip()
            print(re.sub(n, n+'='+pkg[n], l)) # pin package versions
            continue
        if st == 2:
            if 'pip3 -q install' in l:
                st = 3
            print(l)
            continue
        if st == 3:
            if re.match(r'^\s*&&\s*', l):
                st = 4
                print(l)
                continue
            n = l.strip().rstrip('\\').strip()
            print(re.sub(n, n+'=='+pip[n], l)) # pin pip module versions
            continue
        if st == 4:
            print(l)
