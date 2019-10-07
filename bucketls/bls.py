from bucketls import AWSFunctions
import bucketls as bls
import bucketls.utilities as utilities

directory_level = 0
prefixes = {}


def format_folders(folders):
    return [folder + '/' for folder in folders]


def get_and_show_objects(aws, bucket_name, prefix_path):
    objects = aws.get_objects(bucket_name, prefix_path=prefix_path)
    folders, previous_folder, end_of_path = aws.get_folders(objects)
    formatted_folders = format_folders(folders)
    files = aws.get_files(objects)
    files = [file.replace(prefix_path + '/', '') for file in files]
    aws.show_objects('', formatted_folders + files)
    return folders, previous_folder, end_of_path


def browse_bucket(aws, bucket_name, directories):
    flag = True
    previous_folder = ''
    end_of_path = False
    prefix_path = ''
    while flag:
        display_prefix_path = bucket_name + '/' + prefix_path
        directory = utilities.get_input(directories, display_prefix_path)
        directory = utilities.parse_input(directory)
        valid_directory = utilities.validate(directory, directories)

        if directory == 'exit':
            flag = False
            bucket_flag = False
            break

        elif directory == 'cd /':
            flag = False
            bucket_flag = True
            break

        elif directory == 'cd ..':
            previous_folder = previous_folder.split('/')
            if len(previous_folder) > 2:
                previous_folder = previous_folder[:len(previous_folder) - 2]
                prefix_path = '/'.join(previous_folder)

            elif previous_folder[0] == '':
                flag = False
                bucket_flag = True
                break
            else:
                previous_folder = previous_folder[:len(previous_folder) - 2]
                prefix_path = '/'.join(previous_folder)
            directories, previous_folder, end_of_path = get_and_show_objects(
                aws, bucket_name, prefix_path)

        elif valid_directory:
            if previous_folder == '':
                prefix_path = directory
            else:
                prefix_path = previous_folder + directory
            prefix_path = prefix_path.strip()
            directories, previous_folder, end_of_path = get_and_show_objects(
                aws, bucket_name, prefix_path)

        elif end_of_path:
            text = 'Reached end of folder path. Run, cd .. to go back one folder up (or) cd / to go to the root folder.'
            bls.format_print(text, ['bold', 'dark'])

        else:
            print('Enter valid folder name')
            bls.format_print('Folders:', ['bold'])
            for folder in directories:
                print(folder)

    return flag, bucket_flag


def browse_all(aws):
    bucket_flag = True
    show_buckets = True
    while bucket_flag:
        if show_buckets:
            buckets = aws.get_buckets()
            aws.show_objects('Buckets', buckets)
        bucket_name = utilities.get_input(buckets)
        bucket_name = utilities.parse_input(bucket_name)
        valid_bucket = utilities.validate(bucket_name, buckets)

        while valid_bucket:
            directories, previous_folder, end_of_path = get_and_show_objects(aws, bucket_name, '')
            flag, bucket_flag = browse_bucket(aws, bucket_name, directories)
            if not flag:
                show_buckets = True
                break

        if bucket_name == 'exit':
            bucket_flag = False
            break

        if not valid_bucket:
            bls.format_print('Enter valid bucket name', ['bold'])
            show_buckets = False

        if not bucket_flag:
            break


def run():
    aws = AWSFunctions()
    browse_all(aws)
    print('Bye')
