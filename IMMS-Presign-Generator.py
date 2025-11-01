import os
import boto3
import json
import uuid

s3 = boto3.client('s3')
BUCKET = os.environ.get('UPLOAD_BUCKET', 'imms-project-uploads')

def lambda_handler(event, context):
    # Parse the incoming request body
    body = json.loads(event.get('body') or '{}')
    
    # Generate a unique file name if not provided
    file_name = body.get('fileName') or f"{uuid.uuid4()}"
    
    # ✅ Default content type set to image/jpeg
    content_type = body.get('contentType', 'image/jpeg')
    
    # Define the S3 key (path inside bucket)
    key = f"uploads/{file_name}"
    
    # Generate the presigned URL for uploading
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': BUCKET,
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=900  # URL valid for 15 minutes
    )
    
    # Return the upload URL and object key
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # ✅ CORS enabled
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({
            "uploadUrl": url,
            "key": key
        })
    }
