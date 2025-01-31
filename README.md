# Whisper Transcription Service

This project provides a transcription service using OpenAI's Whisper model. It allows you to upload audio or video files and returns the transcribed text.

## Prerequisites

- Docker

## Building and Running the Docker Container

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build the Docker image:**
    ```sh
    docker build -t whisper-transcription-service .
    ```

3. **Run the Docker container:**
    ```sh
    docker run --gpus all -d -p 5001:5001 --name whisper-transcription whisper-transcription-service
    ```

## Using the API

Once the container is running, you can use the `/transcribe` endpoint to transcribe audio or video files.

### Endpoint

- **POST** `/transcribe`

### Request

- **Form Data**: `audio` - The audio or video file to be transcribed.

### Example using `curl`

```sh
curl -X POST http://localhost:5001/transcribe -F "audio=@/path/to/your/file.mp3"
```

### Example using PowerShell

```powershell
# Define the transcription API endpoint
$apiEndpoint = "http://localhost:5001/transcribe"

# Define the video file extensions to process (add more if needed)
$videoExtensions = @("*.mkv", "*.mp4", "*.avi", "*.mov")  # Add other extensions as required

# Retrieve all video files in the current directory and subdirectories
$videoFiles = Get-ChildItem -Path . -Recurse -Include $videoExtensions -File

# Check if any video files were found
if ($videoFiles.Count -eq 0) {
    Write-Host "No video files found in the current directory or its subdirectories."
    exit 0
}

# Iterate over each video file
foreach ($file in $videoFiles) {
    $filePath      = $file.FullName
    $fileDirectory = $file.DirectoryName
    $baseName      = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)

    # Define the transcriptions folder path within the file's directory
    $transcriptionsFolder = Join-Path $fileDirectory "transcriptions"

    # Create the 'transcriptions' folder if it doesn't exist
    if (-Not (Test-Path -Path $transcriptionsFolder)) {
        try {
            New-Item -ItemType Directory -Path $transcriptionsFolder -Force | Out-Null
            Write-Host "Created folder: $transcriptionsFolder"
        }
        catch {
            Write-Error "Failed to create folder '$transcriptionsFolder'. Error: $_"
            continue  # Skip to the next file
        }
    }

    # Define the output transcription file path
    $outputFilePath = Join-Path $transcriptionsFolder "$baseName.txt"

    # Check if the transcription file already exists
    if (Test-Path -Path $outputFilePath) {
        Write-Host "Skipping '$filePath': Transcription already exists."
        continue  # Skip to the next file
    }

    Write-Host "Processing file: $filePath"
    Write-Host "Saving transcription to: $outputFilePath"

    try {
        # Call the transcription API using curl.exe
        $transcription = curl.exe --location $apiEndpoint `
            --form "audio=@`"$filePath`"" `
            --silent

        # Validate the response
        if (-not [string]::IsNullOrWhiteSpace($transcription)) {
            # Save the transcription string to a .txt file
            $transcription | Out-File -FilePath $outputFilePath -Encoding UTF8
            Write-Host "Transcription saved successfully for: $baseName`n"
        }
        else {
            Write-Warning "Received empty transcription for '$filePath'. Skipping save."
        }
    }
    catch {
        Write-Error "Failed to process '$filePath'. Error: $_"
    }
}

```

