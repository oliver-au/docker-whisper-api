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
# Check if the transcription file already exists
if (Test-Path -Path $outputFilePath) {
    Write-Host "Skipping '$($file.Name)': Transcription already exists."
    continue
}

Write-Host "Processing file: $($file.Name)"
Write-Host "Saving transcription to: $outputFilePath"

try {
    # Call the transcription API using curl.exe
    $transcription = curl.exe --location "http://localhost:5001/transcribe" `
        --form "audio=@`"$inputFilePath`"" `
        --silent

    # Validate the response (optional)
    if (-not [string]::IsNullOrWhiteSpace($transcription)) {
        # Save the transcription string to a .txt file
        $transcription | Out-File -FilePath $outputFilePath -Encoding UTF8
        Write-Host "Transcription saved successfully for: $baseName`n"
    }
    else {
        Write-Warning "Received empty transcription for '$($file.Name)'. Skipping save."
    }
}
catch {
    Write-Error "Failed to process '$($file.Name)'. Error: $_"
}
```

