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
# Define the base transcription API endpoint
$baseApiEndpoint = "http://localhost:5001/transcribe"
$baseApiEndpointVtt = "http://localhost:5001/transcribe?format=vtt"
$baseApiEndpointText = "http://localhost:5001/transcribe?format=text"

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

    # Define the transcriptions folder paths within the file's directory
    $vttFolder = Join-Path $fileDirectory "transcriptions-vtt"
    $textFolder = Join-Path $fileDirectory "transcriptions-text"

    # Create the folders if they don't exist
    foreach ($folder in @($vttFolder, $textFolder)) {
        if (-Not (Test-Path -Path $folder)) {
            try {
                New-Item -ItemType Directory -Path $folder -Force | Out-Null
                Write-Host "Created folder: $folder"
            }
            catch {
                Write-Error "Failed to create folder '$folder'. Error: $_"
                # Decide if you want to continue with the file or skip entirely
                # continue 2 # Uncomment to skip this file entirely if folder creation fails
            }
        }
    }

    # --- Process VTT Format ---
    $vttOutputFilePath = Join-Path $vttFolder "$baseName.vtt"
    if (Test-Path -Path $vttOutputFilePath) {
        Write-Host "Skipping VTT for '$filePath': Transcription already exists."
    } else {
        Write-Host "Processing VTT for file: $filePath"
        Write-Host "Saving VTT transcription to: $vttOutputFilePath"
        try {
            $vttApiEndpoint = $baseApiEndpointVtt
            $vttTranscription = curl.exe --location $vttApiEndpoint `
                --form "audio=@`"$filePath`"" `
                --silent

            if (-not [string]::IsNullOrWhiteSpace($vttTranscription)) {
                $vttTranscription | Out-File -FilePath $vttOutputFilePath -Encoding UTF8
                Write-Host "VTT Transcription saved successfully for: $baseName"
            } else {
                Write-Warning "Received empty VTT transcription for '$filePath'. Skipping save."
            }
        } catch {
            Write-Error "Failed to process VTT for '$filePath'. Error: $_"
        }
    }

    # --- Process Text Format ---
    $textOutputFilePath = Join-Path $textFolder "$baseName.txt"
    if (Test-Path -Path $textOutputFilePath) {
        Write-Host "Skipping Text for '$filePath': Transcription already exists."
    } else {
        Write-Host "Processing Text for file: $filePath"
        Write-Host "Saving Text transcription to: $textOutputFilePath"
        try {
            $textApiEndpoint = $baseApiEndpointText
            $textTranscription = curl.exe --location $textApiEndpoint `
                --form "audio=@`"$filePath`"" `
                --silent

            if (-not [string]::IsNullOrWhiteSpace($textTranscription)) {
                $textTranscription | Out-File -FilePath $textOutputFilePath -Encoding UTF8
                Write-Host "Text Transcription saved successfully for: $baseName"
            } else {
                Write-Warning "Received empty Text transcription for '$filePath'. Skipping save."
            }
        } catch {
            Write-Error "Failed to process Text for '$filePath'. Error: $_"
        }
    }
    Write-Host "" # Add a newline for better readability between files
}
```

