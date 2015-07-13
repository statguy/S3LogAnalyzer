#!/usr/bin/python

import optparse
import sys
import re

parser = optparse.OptionParser("usage: %prog [options]")
parser.add_option("-!", "--invert", dest="filter_invert", action="store_true", default=False, help="invert match")
parser.add_option("-i", "--ip", metavar="IP", dest="filter_ip", type="string", help="IP address regex")
parser.add_option("-r", "--request", metavar="REQUEST", dest="filter_request", type="string", help="request regex")
parser.add_option("-u", "--useragent", metavar="USERAGENT", dest="filter_useragent", type="string", help="useragent regex")
# TODO: add more filtering options

(options, args) = parser.parse_args()

log_entry_prog = re.compile(r'(?P<target_bucket>"[^"]*") (?P<target_object>"[^"]*") ' +
r'(?P<owner>\S+) (?P<bucket>\S+) (?P<time>\[[^]]*\]) (?P<ip>\S+) ' +
r'(?P<requester>\S+) (?P<reqid>\S+) (?P<operation>\S+) (?P<key>\S+) ' +
r'(?P<request>"[^"]*") (?P<status>\S+) (?P<error>\S+) (?P<bytes>\S+) ' +
r'(?P<size>\S+) (?P<totaltime>\S+) (?P<turnaround>\S+) (?P<referrer>"[^"]*") ' +
r'(?P<useragent>".*?") (?P<version>\S)')

def strip_double_quotes(str):
    if str.startswith('"') and str.endswith('"'):
        return str[1:-1]
    else:
        return str

for log_data in sys.stdin:
    if log_data.isspace():
        continue

    log_match = log_entry_prog.match(log_data)
    if not log_match:
        print log_data
        sys.exit('Log format mismatch.')
    log_entry_dict = log_match.groupdict()
    n_matches = 0

    if options.filter_ip != None:
        if re.match(options.filter_ip, log_entry_dict['ip']) != None:
            n_matches += 1
    if options.filter_request != None:
        if re.match(options.filter_request, strip_double_quotes(log_entry_dict['request'])) != None:
            n_matches += 1
    if options.filter_useragent != None:
        if re.match(options.filter_useragent, strip_double_quotes(log_entry_dict['useragent'])) != None:
            n_matches += 1

    if options.filter_invert:
        if n_matches == 0:
            print log_data
    else:
        if n_matches > 0:
            print log_data
