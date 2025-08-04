#!/usr/bin/env python3
"""
Teams Transcript Summariser (TXT version)

This script takes a .txt transcript file, sends the content to AWS Bedrock
for summarization, and saves the results to a new .txt file.
"""

import boto3
import argparse
import sys
import os
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError
import json
import datetime


class TranscriptSummariser:
    """Initializes the summariser with AWS Bedrock client."""
    def __init__(self):
        try:
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name='us-east-1'
            )
            print(f"Successfully connected to AWS Bedrock")
        except NoCredentialsError:
            print("AWS credentials not found. Please configure your AWS credentials.")
            print("   You can use: aws configure")
            sys.exit(1)
        except Exception as e:
            print(f"Error connecting to AWS Bedrock: {e}")
            sys.exit(1)

    def read_txt_file(self, file_path):
        """
        Read text content from a .txt file.
        Args:
            file_path (str): Path to the .txt file
        Returns:
            str: Extracted text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            if not text_content.strip():
                print("Error: No text content found in the document")
                sys.exit(1)
            return text_content
        except Exception as e:
            print(f"Error reading .txt file: {e}")
            sys.exit(1)

    def summarize_with_bedrock(self, text_content, max_tokens=1000):
        """
        Send text content to AWS Bedrock for summarization.
        Args:
            text_content (str): Text to summarize
            max_tokens (int): Maximum tokens for the summary
        Returns:
            str: Summarized content
        """
        prompt = f"""Please provide a comprehensive summary of the following Teams transcript. \
                    Focus on the key points from each participant, main topics discussed, and important decisions or follow-up actions mentioned.\n\nTranscript:\n{text_content}\n\nSummary:"""

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            print("Sending content to AWS Bedrock for summarization...")
            response = self.bedrock_client.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(request_body)
            )
            response_body = json.loads(response['body'].read())
            summary = response_body['content'][0]['text']
            print(summary)
            print("Summarization completed successfully!")
            return summary
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                print("Access denied. Please check your AWS permissions for Bedrock.")
            elif error_code == 'ModelInvocationException':
                print("Model invocation failed. Please check the input format.")
            else:
                print(f"AWS Bedrock error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error during summarization: {e}")
            sys.exit(1)

    def save_summary_to_txt(self, summary, output_path):
        """
        Save the summarized content to a new .txt file.
        Args:
            summary (str): Summarized content to save
            output_path (str): Path for the output .txt file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Transcript Summary\n\n")
                f.write(summary.strip() + "\n")
            print(f"Summary saved to: {output_path}")
        except Exception as e:
            print(f"Error saving summary to .txt: {e}")
            sys.exit(1)

    def process_transcript(self, input_file, output_file=None):
        """
        Main method to process the transcript file.
        Args:
            input_file (str): Path to input .txt file
            output_file (str): Path to output .txt file (optional)
        """
        # Validate input file
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            sys.exit(1)
        if not input_file.lower().endswith('.txt'):
            print("Error: Input file must be a .txt file")
            sys.exit(1)
        # Generate timestamp for versioning
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        # Generate output filename if not provided
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_summary_{timestamp}.txt"
        else:
            output_path = Path(output_file)
            if output_path.suffix == '.txt':
                output_file = output_path.with_stem(f"{output_path.stem}_{timestamp}")
            else:
                output_file = output_path.parent / f"{output_path.name}_{timestamp}.txt"
        print(f"Reading transcript from: {input_file}")
        text_content = self.read_txt_file(input_file)
        print(f"Extracted {len(text_content)} characters of text")
        summary = self.summarize_with_bedrock(text_content)
        self.save_summary_to_txt(summary, output_file)
        print(f"Process completed successfully!")
        print(f"   Input: {input_file}")
        print(f"   Output: {output_file}")


def main():
    """Main function to handle command line arguments and run the summariser."""
    parser = argparse.ArgumentParser(
        description="Summarize Teams transcript (.txt) using AWS Bedrock",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python summariser.py transcript.txt
  python summariser.py transcript.txt -o summary.txt
        """
    )
    parser.add_argument(
        'input_file',
        help='Path to the input .txt transcript file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Path for the output .txt file (default: input_summary.txt)'
    )
    args = parser.parse_args()
    summariser = TranscriptSummariser()
    summariser.process_transcript(args.input_file, args.output)


if __name__ == "__main__":
    main()
