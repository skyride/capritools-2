import os
import pytz
from datetime import datetime

from capritools import local_settings

from capritools2.parsers.dscanparser import DscanParser


# Scan folder
location = local_settings.OLD_SCANS_ROOT
parser = DscanParser()

files = os.listdir(location)
for i, filename in enumerate(files):
    h = open(location + filename, "r")
    scan = "\n".join(h.readlines())
    h.close()

    added = datetime.fromtimestamp(int(os.path.getmtime(location + filename)))
    added = pytz.utc.localize(added)
    status = parser.parse(scan, oldFormat=True, key=filename, added=added)

    print "(%s/%s) Parsed %s %s" % (i+1, len(files), filename, status)
