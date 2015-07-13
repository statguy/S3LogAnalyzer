#!/usr/bin/python

import optparse
import boto3
from botocore.client import ClientError
import sys

parser = optparse.OptionParser("usage: %prog bucket [prefix]")

(options, args) = parser.parse_args()
if len(args) == 0:
    parser.error("Argument 'bucket' missing.")
target_bucket = args[0]

target_prefix = None
if len(args) == 2:
    target_prefix = args[1]

s3 = boto3.resource('s3')
try:
    s3.meta.client.head_bucket(Bucket=target_bucket)
except ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        sys.exit("Bucket '"+target_bucket+"' does not exists.")
    elif error_code != 200:
        sys.exit("Bucket '"+target_bucket+"' returned error "+error_code+".")

bucket = s3.Bucket(target_bucket)

# TODO: Gets only max 1000 objects, use paginator to obtain more.
bucket_objects = None
if target_prefix != None:
    bucket_objects = bucket.objects.filter(Prefix=target_prefix)
else:
    bucket_objects = bucket.objects.all()

for obj in bucket_objects:
    log_obj = s3.Object(target_bucket, obj.key)
    log_data = log_obj.get()['Body'].read()
    #log_data = '"' + target_bucket + '" "' + obj.key + '":\n' + log_data
    log_data = '\n'.join(['"' + target_bucket + '" "' + obj.key + '" ' + s for s in log_data.splitlines()])
    print log_data
