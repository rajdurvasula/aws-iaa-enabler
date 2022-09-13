#!/bin/bash
CURR_DIR=`pwd`
for i in "setup-iaa-sf3.yaml" "iaa_member_enabler_sm.json"
do
	aws s3 cp $i s3://org-sh-ops/
done
cd src
for i in "enable_iaa_member.zip" "ou_member_accounts.zip";
do
	aws s3 cp $i s3://org-sh-ops/
done
cd $CURR_DIR
