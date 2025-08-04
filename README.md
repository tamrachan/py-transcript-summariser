# Teams Transcript Summariser (TXT version)

A Python script that takes a `.txt` transcript file, sends the content to AWS Bedrock for summarization, and saves the results to a new `.txt` file.

## Features

- Reads plain `.txt` transcript files
- Uses AWS Bedrock (Claude 3 Sonnet) for intelligent summarization
- Saves summarized content to a new `.txt` file
- AWS region set to us-east-1
- Comprehensive error handling and validation
- Simple, fast, and robust (no dependency on Microsoft Word or docx files)

## Prerequisites

1. **Python 3.7+** installed on your system
2. **AWS Account** with access to Bedrock service
3. **AWS Credentials** configured locally

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## AWS Setup

### 1. Configure AWS Credentials

You need to configure your AWS credentials. You can do this in several ways:

**Option A: Using AWS CLI**
```bash
aws configure
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option C: AWS Credentials File**
Create `~/.aws/credentials` (Linux/Mac) or `%UserProfile%\.aws\credentials` (Windows):
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```

### 2. Enable Bedrock Access

Ensure your AWS account has access to the Bedrock service in the us-east-1 region.

## Usage

### Basic Usage

```bash
python summariser.py transcript.txt
```

This will:
- Read `transcript.txt`
- Send content to AWS Bedrock for summarization
- Save the summary as `transcript_summary.txt`

### Advanced Usage

**Specify output file:**
```bash
python summariser.py transcript.txt -o my_summary.txt
```

### Command Line Options

- `input_file`: Path to the input `.txt` transcript file (required)
- `-o, --output`: Path for the output `.txt` file (optional, default: input_summary.txt)

## Example Workflow

1. **Prepare your transcript**: Save your Teams meeting transcript as a `.txt` file
2. **Run the script**: `python summariser.py meeting_transcript.txt`
3. **Get your summary**: The script will create `meeting_transcript_summary.txt`

## Output Format

The generated summary document includes:
- A title: "Transcript Summary"
- The AI-generated summary content

## Error Handling

The script includes comprehensive error handling for:
- Missing AWS credentials
- Invalid file paths
- Non-`.txt` input files
- AWS Bedrock access issues
- File read/write errors

## Troubleshooting

### Common Issues

**"AWS credentials not found"**
- Run `aws configure` to set up your credentials
- Or set environment variables as shown above

**"Access denied"**
- Check that your AWS account has Bedrock permissions
- Verify you're using the correct region

**"Input file not found"**
- Check the file path is correct
- Ensure the file exists and is readable

**"No text content found"**
- Verify the `.txt` file contains text content
- Check that the file isn't corrupted

### Getting Help

Run the script with `-h` for help:
```bash
python summariser.py -h
```

## Technical Details

- **AWS Service**: Bedrock Runtime API
- **Model**: Claude 3 Sonnet (anthropic.claude-3-sonnet-20240229-v1:0)
- **Input Format**: Plain text from `.txt` file
- **Output Format**: Plain text `.txt` with title and content
- **Max Tokens**: 1000 (configurable in code)

## Dependencies

- `boto3`: AWS SDK for Python
- `botocore`: AWS core functionality

## License

This project is provided as-is for educational and personal use.