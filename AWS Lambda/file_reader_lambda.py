import json
import boto3
import io
from chunking import split_and_reduce_chunks  # Import the updated function
from PyPDF2 import PdfReader
from urllib.parse import unquote_plus

# Initialize the S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract the bucket name and raw file name from the event (triggered by S3)
        s3_bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        s3_raw_file_name = event["Records"][0]["s3"]["object"]["key"]  # Raw key (possibly URL encoded)
        s3_file_name = unquote_plus(s3_raw_file_name)  # Decode the key to handle special characters

        # Fetch the PDF file from S3 using the decoded key
        s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_file_name)
        pdf_content = s3_object['Body'].read()

        # Read the PDF using PyPDF2
        reader = PdfReader(io.BytesIO(pdf_content))
        pdf_text = ""

        # Extract text from each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()

        # Use the split_and_reduce_chunks function from chunking.py
        chunks = split_and_reduce_chunks(pdf_text)
        number_of_chunks = len(chunks)

        # Return the number of chunks
        return {
            'statusCode': 200,
            'body': json.dumps('PDF text processed successfully!'),
            'number_of_chunks': number_of_chunks,
            # Optionally, include the chunks themselves
            # 'chunks': chunks
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }
