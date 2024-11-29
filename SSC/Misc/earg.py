import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials
AWS_ACCESS_KEY_ID = 'AKIAT7JJU2JBBCLMP4NJ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_BUCKET_NAME = 'ssc-disrupt'

# File to upload
file_path = r'C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Clients\Square Second Consultancy\SSC\SSC\media\property\head_GIbgU6f.jpg'  # Replace with the path of the file you want to upload
s3_file_name = 'property/your-uploaded-file.jpg'  # The name of the file in S3 after upload

# Initialize a session using your AWS credentials
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

try:
    # Upload the file
    s3.upload_file(file_path, AWS_S3_BUCKET_NAME, s3_file_name)
    print(f"File '{file_path}' has been uploaded to '{AWS_S3_BUCKET_NAME}/{s3_file_name}'")
except FileNotFoundError:
    print(f"File '{file_path}' not found")
except NoCredentialsError:
    print("Credentials not available")
except Exception as e:
    print(f"An error occurred: {e}")
