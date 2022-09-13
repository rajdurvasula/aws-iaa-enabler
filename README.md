# Setup IAM Access Analyzer for Control Tower Landing Zone Accounts
- This automation code enables IAM Access Analyzer on Member accounts

## Instructions

1. Upload files:
  - src/enable_iaa_member.zip to S3 Bucket. Note down the S3 Key
  - src/ou_member_accounts.zip to S3 Bucket. Note down the S3 Key
  - iaa_member_enabler_sm.json to S3 Bucket. Note down the S3 Key
    - *This is referred as* **IAAEnablerSM** *statemachine*
  - setup-iaa-sf3.yaml to S3 Bucket

## Launch sequence
1. Launch CloudFormation stack using setup-iaa-sf3.yaml
2. Execute StateMachine **IAAEnablerSM**
3. Input JSON to StateMachine:
  - **org_unit_id** parameter value is the Organizational Unit comprising of member accounts where IAA should be enabled
```
{
  "org_id": "o-a4tlobvmc0",
  "org_unit_id": "ou-6ulx-t0dafadf",
  "ct_home_region": "us-east-1",
  "audit_account": "413157014023",
  "assume_role": "AWSControlTowerExecution"
}
```

## State Machine
- State Machine attempts to enable IAM Access Analyzer on member accounts that belong to provided Organizational Unit
  - In cases where member account is already enabled, exception is reported and no further action needed

![iaa_member_enabler_sm.png](./iaa_member_enabler_sm.png?raw=true)

## Limitations
- IAA enabler cannot be targeted to a Single Member Account
- All Member Accounts in provided Organizational Unit are effected