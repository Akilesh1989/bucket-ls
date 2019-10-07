import boto3
import os
from termcolor import colored


def get_aws_profile():
    profile = os.environ['AWS_PROFILE']
    print('AWS PROFILE: ' + str(profile))
    print('----------')
    return profile


def format_print(text, attrs):
    print(colored(text, attrs=attrs))


def get_common_prefixes(result):
    return result.get('CommonPrefixes', [])


def get_folder(prefix):
    folder = prefix.split('/')
    return folder[-2]


def get_folders_from_prefix(common_prefixes):
    folders = []
    if common_prefixes:
        for common_prefix in common_prefixes:
            prefix = common_prefix.get('Prefix')
            if prefix:
                folders.append(get_folder(prefix))
    return folders


def get_previous_folder(result):
    return result['Prefix']


class AWSFunctions:
    def __init__(self):
        profile = get_aws_profile()
        session = boto3.Session(profile_name=profile)
        self.client = session.client('s3')
        self.resource = session.resource('s3')

    def get_objects(self, bucket, prefix_path):
        paginator = self.client.get_paginator('list_objects')
        operation_parameters = {}
        operation_parameters['Bucket'] = bucket
        operation_parameters['Delimiter'] = '/'
        if prefix_path == '':
            operation_parameters['Prefix'] = ''
        else:
            prefix_path = prefix_path + '/'
            operation_parameters['Prefix'] = prefix_path

        objects = paginator.paginate(**operation_parameters)
        return objects

    def get_buckets(self):
        buckets = [bucket.name for bucket in self.resource.buckets.all()]
        return buckets

    def get_folders(self, objects):
        end_of_path = False
        for page in objects:
            previous_folder = get_previous_folder(page)
            common_prefixes = get_common_prefixes(page)
            if common_prefixes:
                folders = get_folders_from_prefix(common_prefixes)
            else:
                folders = []
                end_of_path = True
        return folders, previous_folder, end_of_path

    def get_files(self, objects):
        files = []
        for page in objects:
            if 'Contents' in page.keys():
                if page['Contents']:
                    for file in page['Contents']:
                        files.append(file['Key'])
        return files

    def show_objects(self, display_text, objects):
        attrs = list(['bold', 'underline'])
        format_print(display_text, attrs)
        for object in objects:
            print(object)
