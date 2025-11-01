import json
import os
import boto3
import uuid
import io
from datetime import datetime
from PIL import Image

s3 = boto3.client('s3')
rek = boto3.client('rekognition')
ddb = boto3.resource('dynamodb')

# Environment variables
TABLE_NAME = os.environ['DDB_TABLE']
THUMB_BUCKET = os.environ['THUMB_BUCKET']
THUMB_WIDTH = int(os.environ.get('THUMB_WIDTH', '300'))

table = ddb.Table(TABLE_NAME)

def generate_thumbnail(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail((THUMB_WIDTH, THUMB_WIDTH))
    out_buf = io.BytesIO()
    img.save(out_buf, format='JPEG')
    out_buf.seek(0)
    return out_buf

def lambda_handler(event, context):
    for rec in event.get('Records', []):
        s3bucket = rec['s3']['bucket']['name']
        key = rec['s3']['object']['key']
        media_id = str(uuid.uuid4())
        
        try:
            resp = s3.get_object(Bucket=s3bucket, Key=key)
            content_type = resp['ContentType']
            body = resp['Body'].read()

            # Skip if it's already a thumbnail
            if key.lower().startswith("thumbs/"):
                print(f"Skipping thumbnail file: {key}")
                continue

            # Generate thumbnail
            thumb_key = None
            if content_type.startswith('image/'):
                thumb_buf = generate_thumbnail(body)
                thumb_key = f"thumbs/{media_id}.jpg"
                s3.put_object(
                    Bucket=THUMB_BUCKET,
                    Key=thumb_key,
                    Body=thumb_buf,
                    ContentType='image/jpeg'
                )

            # Detect labels
            rek_resp = rek.detect_labels(
                Image={'Bytes': body},
                MaxLabels=10,
                MinConfidence=70.0
            )
            labels = [{'Name': l['Name'], 'Confidence': round(l['Confidence'], 2)} for l in rek_resp.get('Labels', [])]

            # Save metadata to DynamoDB
            table.put_item(Item={
                'mediaId': media_id,
                's3Bucket': s3bucket,
                's3Key': key,
                'thumbKey': thumb_key,
                'contentType': content_type,
                'labels': labels,
                'createdAt': datetime.utcnow().isoformat()
            })

            print(f"Processed: {key} → {thumb_key}")

        except Exception as e:
            print("Error processing", key, str(e))
            raise e

    return {"statusCode": 200, "body": json.dumps("Processing complete")}
