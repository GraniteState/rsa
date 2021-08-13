#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 07:39:37 2021

@author: katebelisle
"""

import logging
import boto3
from botocore.exceptions import ClientError
#%%
# 90 day expiry
expiration=3600*24*90
client_method_name=""
method_parameters=""
#%%

    # Generate a presigned URL for the S3 client method
s3_client = boto3.client('s3')
try:
    response = s3_client.generate_presigned_url(ClientMethod=client_method_name,
                                                Params=method_parameters,
                                                ExpiresIn=expiration)
except ClientError as e:
    logging.error(e)
