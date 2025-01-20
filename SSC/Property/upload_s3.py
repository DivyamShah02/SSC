import os
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
import base64
import requests


def base64_to_text(b64_text):
    return base64.b64decode(b64_text.encode()).decode()


def upload_to_s3_from_request_files(request_files, s3_folder):
    """
    Upload files from request.FILES to an S3 bucket and return their links.
    
    :param request_files: Django's request.FILES['extra_file']
    :param bucket_name: S3 bucket name
    :param s3_folder: Folder path in the S3 bucket
    :return: List of S3 file URLs
    """
    
    # Configuration
    AWS_ACCESS_KEY = base64_to_text('QUtJQVQ3SkpVMkpCQkNMTVA0Tko=')
    AWS_SECRET_KEY = base64_to_text('ZnE4SHdESHZxdkVWUEMwbHI0TUxWYlgzRDQxbjBZV1hXeUxuMlBGbA==')
    S3_BUCKET_NAME = 'ssc-disrupt'
    AWS_REGION = 'eu-north-1'

    S3_BACKUP_FOLDER = "backups/"

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    uploaded_file_links = []
    for file in request_files:
        file_name = file.name
        file_extension = file_name.split('.')[-1]
        file_base_name = '.'.join(file_name.split('.')[:-1])

        # Check if file already exists and generate a unique name
        counter = 0
        s3_key = f"{s3_folder}{file_name}"
        while True:
            try:
                # If the file exists, modify the name
                counter += 1
                s3_key = f"{s3_folder}{file_base_name} ({counter}).{file_extension}"
                url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
                file_exists = check_s3_file_exists(url)
                if not file_exists:
                    break
            except Exception as e:
                print(f"Error checking file existence: {e}")
                break

        # Upload the file
        try:
            s3_client.upload_fileobj(file, S3_BUCKET_NAME, s3_key)
            file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            uploaded_file_links.append(file_url)
            print(f"Uploaded {file.name} to S3 bucket {S3_BUCKET_NAME}/{s3_key}")
        except NoCredentialsError:
            print("AWS credentials are incorrect or missing.")
        except Exception as e:
            print(f"Error uploading to S3: {e}")

    return uploaded_file_links

def check_s3_file_exists(url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error checking URL: {e}")
            return False

if __name__ == '__main__':
    # Example usage
    url = 'https://ssc-disrupt.s3.amazonaws.com/plan/polymers-feature.jpg.webp'
    file_exists = check_s3_file_exists(url)
    print(f"File exists: {file_exists}")

