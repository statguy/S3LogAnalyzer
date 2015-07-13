#!/usr/bin/python

import optparse
import sys
import boto3
import re

parser = optparse.OptionParser("usage: %prog action [options]")

(options, args) = parser.parse_args()
if len(args) == 0:
    parser.error("Argument 'action' missing.")
action = args[0]

if action not in ['print', 'delete']:
    sys.exit("Invalid action ''" + action + "'.")

s3 = boto3.resource('s3')
obj_prog = re.compile(r'^(?P<target_bucket>"[^"]*") (?P<target_object>"[^"]*")') # First word must be bucket name, second object key, rest are ignored

target_bucket = None
target_object = None

def strip_double_quotes(str):
    if str.startswith('"') and str.endswith('"'):
        return str[1:-1]
    else:
        return str

for obj_data in sys.stdin:
    if obj_data.isspace():
        continue

    obj_match = obj_prog.match(obj_data)
    if not obj_match:
        sys.exit('Object information mismatch.')
    obj_dict = obj_match.groupdict()

    if target_bucket == obj_dict['target_bucket'] and target_object == obj_dict['target_object']:
        continue

    target_bucket = obj_dict['target_bucket']
    target_object = obj_dict['target_object']
    obj = s3.Object(strip_double_quotes(target_bucket), strip_double_quotes(target_object))

    if action == 'print':
        print obj.get()['Body'].read()
    elif action == 'delete':
        print "Deleting " + strip_double_quotes(target_object) + " in bucket " + strip_double_quotes(target_bucket)
        obj.delete()
