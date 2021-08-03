import re
import psutil
import subprocess
import json
import logging
import logging.config
from datetime import datetime
import os
import sys

LOGFILE = '/tmp/{0}.{1}.log'.format(
    os.path.basename(__file__),
    datetime.now().strftime('%Y%m%dT%H%M%S'))

DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
            'stream': sys.stdout,
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'level': 'INFO',
            'filename': LOGFILE,
            'mode': 'w',
        },
    },
    'loggers': {
        __name__: {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    }
}

logging.basicConfig(level=logging.ERROR)
logging.config.dictConfig(DEFAULT_LOGGING)
log = logging.getLogger(__name__)
#['ss -tulpn']
commands =[['netstat', '-atunp'],['ps','-A']]
def log_running_services():
    known_cgroups = set()
    for pid in psutil.pids():
        try:
            cgroups = open('/proc/%d/cgroup' % pid, 'r').read()
        except IOError:
            continue # may have exited since we read the listing, or may not have permissions
        systemd_name_match = re.search('^1:name=systemd:(/.+)$', cgroups, re.MULTILINE)
        if systemd_name_match is None:
            continue # not in a systemd-maintained cgroup
        systemd_name = systemd_name_match.group(1)
        if systemd_name in known_cgroups:
            continue # we already printed this one
        if not systemd_name.endswith('.service'):
            continue # this isn't actually a service
        known_cgroups.add(systemd_name)
        log.info(systemd_name)

def get_log_network(command):
    network_logs = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = network_logs.communicate()
    log.info(stdout)

if __name__ == '__main__':
    log_running_services()
    print("loggggg network")
    for command in commands:
      print(command)
      log.info(get_log_network(command))


"""
def check_package_installed():
    prereqs = list("httpd", "php", "php-devel", "autoconf", "make", "gcc")

    missing_packages = set()
    for package in prereqs:
        print
        "Checking for {0}... ".format([package]),

        # Search the RPM database to check if the package is installed
        res = yb.rpmdb.searchNevra(name=package)
        if res:
            for pkg in res:
                print(pkg, "installed!")
        else:
            missing_packages.add(package)
            print(package, "not installed!")
            # Install the package if missing
            if not skip_install:
                if testing:
                    print("TEST- mock install ", package)
                else:
                    try:
                        yb.install(name=package)
                    except yum.Errors.InstallError, err:
                        print(>> sys.stderr, "Failed during install of {0} package!".format(package))
                        print(>> sys.stderr, str(err))
                        sys.exit(1)

    # Done processing all package requirements, resolve dependencies and finalize transaction
    if len(missing_packages) > 0:
        if skip_install:
            # Package not installed and set to not install, so fail
            print >> sys.stderr, "Please install the {0} packages and try again.".format(
                ",".join(str(name) for name in missing_packages))
            sys.exit(1)
        else:
            if testing:
                print("TEST- mock resolve deps and process transaction")
            else:   
                yb.resolveDeps()
                yb.processTransaction()
"""