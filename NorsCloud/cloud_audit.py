#!/usr/bin/env python3
# NorsCloud - Cloud Infrastructure Misconfiguration Scanner
# License: GPLv3
import sys
import boto3
import argparse
from botocore.exceptions import ClientError

def check_s3_buckets(profile=None):
    print("\n[*] NorsCloud: Scanning S3 Buckets for Public Access...")
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        s3 = session.client('s3')
        buckets = s3.list_buckets().get('Buckets', [])
        
        for bucket in buckets:
            name = bucket['Name']
            try:
                acl = s3.get_bucket_acl(Bucket=name)
                public = False
                for grant in acl.get('Grants', []):
                    grantee = grant.get('Grantee', {}).get('URI', '')
                    if 'AllUsers' in grantee or 'AuthenticatedUsers' in grantee:
                        public = True
                
                if public:
                    print(f"  [\033[91m!\033[0m] PUBLIC BUCKET FOUND: {name}")
                else:
                    print(f"  [+] Secure: {name}")
            except ClientError as e:
                print(f"  [-] Access Denied checking ACL for: {name}")
    except Exception as e:
        print(f"[-] Error: {e}")

def check_iam_policies(profile=None):
    print("\n[*] NorsCloud: Auditing IAM Policies for '*' Privilege...")
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        iam = session.client('iam')
        users = iam.list_users().get('Users', [])
        
        for user in users:
            policies = iam.list_user_policies(UserName=user['UserName']).get('PolicyNames', [])
            if policies:
                print(f"  [!] User {user['UserName']} has inline policies: {policies} (Review Required)")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NorsCloud AWS Security Auditor")
    parser.add_argument("--profile", help="AWS CLI profile name")
    args = parser.parse_args()
    
    print("🦅 NorsCloud Infrastructure Auditor")
    check_s3_buckets(args.profile)
    check_iam_policies(args.profile)
    print("\n[*] Scan Complete.")
