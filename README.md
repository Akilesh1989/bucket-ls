# bucketls

A interactive way to work with files in an `s3` bucket.

## Motivation
More often in my job, I found myself having to look through s3 buckets to validate if the required fodlers/files were present and download a couple of files. To verify if a folder was present within another folder, I had to manually copy the `folder` name and create a new `s3` url by appending the folder name to the existing url. This became a quick annoyance when I had a `year, month, day` combination of folders. (i.e `s3://ROOT_BUCKET/2018/01/12`, `s3://ROOT_BUCKET/2018/01/03` etc). An alternative way was to download the contents locally and verify using a simple `bash/python` script but this meant I had to always have the disk space and also proved to be time consuming. I wanted a way to view an `s3` bucket the way I browse through my filesystem locally.

This project only has `cd`, `cd ..` and `cd /` implemented for now but will have commands like `find`, `cp`, `mv` in the future.

## Getting Started

Locally, run,
```
git clone https://github.com/Akilesh1989/bucketls.git
```
and then run,
```
pip install -e .
```

Set your `AWS_PROFILE` as environment variable for the script to pick up the correct credentials from the `credentials` file.
```
export AWS_PROFILE=foo
```
### Prerequisites

- Make sure you have your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) setup.
- Make sure you have `python 3.6.4`. [How to install a version of python](https://realpython.com/installing-python/).
- Make sure you have `git` installed. Otherise, [install](https://www.atlassian.com/git/tutorials/install-git) git.
- Install [direnv](https://direnv.net/) if you have not already installed it.

### Usage
In your terminal, run
```
bls
```
This will bring up an interactive shell listing all your root level buckets.

From there, use the following commands to browse through your buckets,

- switch to a directory

You can simply type `cd` to bring up the list of available directories(if you're in the root bucket) or sub-directories (if you're in a directory) as a dropdown list. You can use `tab` to autocomplete suggestions. Press `enter` to switch to the directory/sub-directory.
Alternatively, you can type the directory name, like so:
```
cd DIRECTORY_NAME
```
In the output, every folder will be suffixed with a `/`.

*Note*: Using `cd` in your local filesystem, will only `cd` into the directory and not list any files but running `cd` here will show you the list of folders and files within the `directory`.  I have come to realise that this is not desired if a `directory` had a large number of files. At the time of building this tool,I wanted to make the listing automated for the user and hence this behaviour. I am working on fixing this.

- go back one level
```
cd ..
```

- go to the root directory
```
cd /
```

- exit shell
```
exit
```

## Future implementaions
I am not sure how far I would be able to get with these commands, but here are some ideas I have thought about,
- `ll` - list all the folders and files in a directory
- `cp filename <local_path>` - copies file to local path provided
- `cp filename <path_in_s3>` - copies file from one s3 directory to another like it would be copying a file in the local filesystem.
- `rm filename` - remove file from s3
- `find all <ext> files` - list all files with that `<ext>` as the extension
- `find all <ext> files starting_with <string>` - list all files with that staring with `<string>`. `ext` is optinal
- `find all <ext> files ending_with <string>` - list all files with that staring with `<string>`. `ext` is optinal
- `find all <ext> files containing <string>` - list all files with that staring with `<string>`. `ext` is optinal

- Ability to chain commands, for e.g.
```
    find all csv files starting_with 'foo' && cp all <local_path>
```
The above command should find all the csv files and download it to the local path specified.
