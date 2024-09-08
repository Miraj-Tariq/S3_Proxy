
# FastAPI S3 Proxy Service

This is a FastAPI-based service that provides a proxy for uploading and downloading files from AWS S3.

## Setup

### 1. Install and Configure Poetry

#### **Windows:**
1. Open **PowerShell** as an administrator.
2. Run the following command to install Poetry:
   ```bash
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```
3. Add Poetry to the system `PATH`:
   - Open **Control Panel** > **System** > **Advanced system settings** > **Environment Variables**.
   - Under **User variables**, find and edit the `Path` variable.
   - Add the following path (replace `<YourUsername>` with your actual username):
     ```
     C:\Users\<YourUsername>\AppData\Roaming\Python\Scripts\
     ```
4. Verify installation:
   ```bash
   poetry --version
   ```

#### **MacOS:**
1. Install Poetry via the official installation script:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Add Poetry to your shell configuration by adding the following line to your `.bashrc`, `.zshrc`, or `.bash_profile`:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
3. Verify installation:
   ```bash
   poetry --version
   ```

#### **Linux:**
1. Install Poetry using the official script:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Add Poetry to your system `PATH`. Open your terminal and add the following line to your shell configuration file (`.bashrc`, `.zshrc`, or `.profile`):
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
3. Reload your shell and verify the installation:
   ```bash
   poetry --version
   ```

### 2. AWS IAM Setup for S3 Access

#### **Creating an AWS IAM User and Assigning S3 Policies:**
1. Log in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **IAM** (Identity and Access Management) from the services list.
3. Click on **Users** and then **Add User**.
4. Set a **username** and select **Programmatic access** for access type.
5. Click **Next: Permissions**.
6. Select **Attach policies directly** and search for `AmazonS3FullAccess`. Attach this policy to the user.
7. Complete the process to create the user and download the **Access Key ID** and **Secret Access Key**.

#### **Configure `.env` File:**
- Open the `.env` file (see the next section on how to create one).
- Add the following AWS credentials:
   ```ini 
  AWS_ACCESS_KEY_ID=access-key-id
  AWS_SECRET_ACCESS_KEY=secret-access-key
  AWS_REGION=aws-region
   ```

### 3. Configure `.env` File

1. **Rename** the `.env.example` file to `.env`:
   ```bash
   mv .env.example .env
   ```
2. **Edit the `.env` file** and provide the necessary AWS credentials and configurations:
   ```ini
   AWS_ACCESS_KEY_ID=access-key-id
   AWS_SECRET_ACCESS_KEY=secret-access-key
   AWS_REGION=aws-region
   FILE_DOWNLOAD_EXPIRY=time_in_seconds_like_3600
   ```

### 4. Install Dependencies
Once Poetry is installed, you can install the project dependencies by running:
```bash
poetry install
```

### 5. Running the Application
Start the FastAPI server with:
```bash
poetry run uvicorn main:app --reload
```

### 6. Access the API Documentation
After running the server, you can access the FastAPI documentation for your service by visiting the following URL:
```
http://127.0.0.1:8000/docs
```

## Available Endpoints

The following endpoints are already implemented in the project:

- **Upload a file to S3**: `POST /upload/`
- **Download a file from S3**: `GET /download/`

## Recommendations / TODO:

Here are some endpoints that can be added to enhance the functionality of the S3 proxy service:

1. List all S3 Buckets

2. List all Objects in One S3 Bucket

3. Update an Object against a Key

4. Delete an Object from S3 Bucket
