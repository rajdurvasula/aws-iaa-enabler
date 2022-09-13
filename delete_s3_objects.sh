#!/bin/bash
for i in "setup-iaa-sf3.yaml" "iaa_member_enabler_sm.json" "enable_iaa_member.zip" "ou_member_accounts.zip";
do
	aws s3 rm s3://org-sh-ops/$i
done
