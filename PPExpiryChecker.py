import os.path
import json
import datetime, dateutil.parser
from datetime import tzinfo, timedelta, datetime
import sys

from pprint import pprint
import re
ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-200)

    ppName = sys.argv[1]

    #look for it in the Provisioning profiles directory
    #will only work for versions > Xcode 5
    directory = "~/Library/MobileDevice/Provisioning Profiles/"

    directory = os.path.expanduser(directory)
    #tentative will change later
    profile = open(os.path.join(directory,ppName),mode='rb')
    lines = profile.read()

    sampleTime = '2015-12-04T11:50:03Z'
    #             YYYY-MM-DDTHH:MM:SSZ
    needle = "<key>ExpirationDate</key>\n\t<date>"
    found = lines.find(needle)
    result = lines[found + len(needle):found + len(needle) + len(sampleTime)]


    expiryDate = dateutil.parser.parse(result)
    currentDate = datetime.now(utc)
    difference = expiryDate - currentDate
    retVal = 0
    print   "Provisioning Profile will expire in " + str(difference.days) + " days"
    if  difference.days < 180:
        print "It is recommended to regenerate the Provisioning profile"
        retVal =  -1
    else :
        print "Everything is good to go"


    sys.exit(retVal)
