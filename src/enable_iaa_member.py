import sys
import boto3
import json
import urllib3
import os
import logging
from datetime import date, datetime
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
if 'log_level' in os.environ:
    LOGGER.setLevel(os.environ['log_level'])
    LOGGER.info('Log level set to %s' % LOGGER.getEffectiveLevel())
else:
    LOGGER.setLevel(logging.ERROR)

session = boto3.Session()

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError('Type %s not serializable' % type(obj))

def assume_role(org_id, aws_account_number, role_name):
    sts_client = boto3.client('sts')
    partition = sts_client.get_caller_identity()['Arn'].split(":")[1]
    response = sts_client.assume_role(
        RoleArn='arn:%s:iam::%s:role/%s' % (
            partition, aws_account_number, role_name
        ),
        RoleSessionName=str(aws_account_number+'-'+role_name),
        ExternalId=org_id
    )
    sts_session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken']
    )
    LOGGER.info(f"Assumed region_session for Account {aws_account_number}")
    return sts_session

def get_ct_regions(account_id):
    cf = session.client('cloudformation')
    region_set = set()
    try:
        paginator = cf.get_paginator('list_stack_instances')
        iterator = paginator.paginate(StackSetName='AWSControlTowerBP-BASELINE-CONFIG', StackInstanceAccount=account_id)
        for page in iterator:
            for summary in page['Summaries']:
                region_set.add(summary['Region'])
    except Exception as ex:
        print("Control Tower StackSet not found in this Region")
        print(str(ex))
    print("Control Tower Region Count: {}".format(len(list(region_set))))
    print("Control Tower Regions: {}".format(','.join(list(region_set))))
    return list(region_set)

def create_analyzer(member_session, member_account, region):
    try:
        iaa_client = member_session.client('accessanalyzer', 
        endpoint_url=f"https://access-analyzer.{region}.amazonaws.com", 
        region_name=region)
        name = 'KyndrylAnalyzer-{}'.format(member_account)
        iaa_client.create_analyzer(analyzerName=name,type='ACCOUNT')
        LOGGER.info(f"Analyzer: {name} created for Account: {member_account} in Region: {region}")
        return name
    except Exception as e:
        LOGGER.error(f"failed in create_analyzer(..) for Account: {member_account} in Region: {region}")
        LOGGER.error(str(e))

def lambda_handler(event, context):
    LOGGER.info(f"REQUEST RECEIVED: {json.dumps(event, default=str)}")
    org_id = event['org_id']
    ou_id = event['org_unit_id']
    ct_home_region = event['ct_home_region']
    audit_account = event['audit_account']
    member_account = event['member_account']
    assume_role_name = event['assume_role']
    regions = get_ct_regions(audit_account)
    member_session = assume_role(org_id, member_account, assume_role_name)
    region_analyzers = []
    for region in regions:
        name = create_analyzer(member_session, member_account, region)
        region_analyzers.append({
            'org_id': org_id,
            'org_unit_id': ou_id,
            'ct_home_region': ct_home_region,
            'audit_account': audit_account,
            'member_account': member_account,
            'member_region': region,
            'assume_role': assume_role_name,
            'iaa_name': name
        })
    return {
        'statusCode': 200,
        'analyzers': region_analyzers
    }
    