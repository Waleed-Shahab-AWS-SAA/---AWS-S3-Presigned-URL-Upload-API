# 🗂️ AWS S3 Presigned URL Upload API  

A **serverless image upload API** built with **AWS Lambda**, **API Gateway**, and **Amazon S3**.  
It securely generates presigned URLs so users can upload images directly to S3 — no backend storage or credentials needed.  

> ⚡ After 2 days of continuous debugging and countless “SignatureDoesNotMatch” errors, I finally made this work — and it feels *amazing!* 😄  

---

## 🧩 Architecture  

Client → API Gateway → Lambda → S3


**Flow:**  
1. API Gateway receives a `POST /presign` request  
2. Lambda generates a presigned S3 URL  
3. The client uploads the file directly to S3 using that URL  

🪄 *Fully serverless, scalable, and secure!*  

---

## 🧠 Tech Stack  

| Service | Purpose |
|----------|----------|
| 🧱 **AWS Lambda** | Generates the presigned upload URL |
| 🌐 **API Gateway** | Exposes the `/presign` endpoint |
| ☁️ **Amazon S3** | Stores uploaded images |
| 🐍 **Python (boto3)** | AWS SDK used for URL generation |

---

## 🚀 Example Request  

**Endpoint:**  

POST https://<your-api-id>.execute-api.us-east-1.amazonaws.com/presign


**Body:**  
```json
{
  "fileName": "sample.jpg",
  "contentType": "image/jpeg"
}

{
  "uploadUrl": "<presigned_s3_url>",
  "key": "uploads/sample.jpg"
}

Then, simply upload your image using a PUT request to the uploadUrl.
If you see HTTP 200 OK, the file is successfully stored in your S3 bucket 🎉

🧩 Key Highlights

✅ Secure presigned URL generation

✅ Proper CORS setup for API Gateway

✅ Correct MIME type handling (image/jpeg)

✅ Successfully validated S3 uploads

🧪 Example Use Case

You can integrate this backend with a React or Next.js frontend to upload images securely without exposing AWS credentials.
It’s ideal for:

Profile photo uploads

Portfolio or document management systems

Internal image pipelines

💪 My Journey

This project tested my patience, problem-solving, and AWS debugging skills.
I spent two full days tackling issues like invalid signatures, CORS mismatches, and broken file uploads.

But in the end, seeing a clean 200 OK response and a valid JPEG in my S3 bucket was worth every minute 😎

Lesson learned: When AWS says “SignatureDoesNotMatch,” don’t panic — it’s just testing your persistence 💜

📚 Future Improvements

🔒 Add authentication with AWS Cognito

🗃️ Store metadata in DynamoDB (timestamp, file name, uploader)

🖥️ Build a small React upload UI using this API

🏷️ Tags

AWS Serverless Lambda API Gateway S3 Python Presigned URL Cloud Projects

⭐ If this project helped you, consider giving it a star!
Built with ☁️ AWS, 💜 persistence, and a lot of debugging coffee ☕

