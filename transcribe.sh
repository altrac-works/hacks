#!/usr/bin/env bash
set -euf -o pipefail

JOB_ID="$(date +%s)"
FILE_OG="$1"

echo "Extracting audio."
FILE_AUDIO="${FILE_OG%.mp4}.m4a"
ffmpeg -i "$FILE_OG" -c:a copy -vn "$FILE_AUDIO"

echo "Copying into S3, with JOB_ID=$JOB_ID"
FILE_AUDIO_S3="s3://hfuller-transcribe/$JOB_ID.m4a"
aws s3 cp "$FILE_AUDIO" "$FILE_AUDIO_S3"

echo "Starting transcription."
aws transcribe start-transcription-job --transcription-job-name "$JOB_ID" --language-code en-US --media "MediaFileUri=$FILE_AUDIO_S3" --output-bucket-name hfuller-transcribe --settings "ShowSpeakerLabels=true,MaxSpeakerLabels=10,ShowAlternatives=true,MaxAlternatives=10" --subtitles "Formats=vtt,srt,OutputStartIndex=1"

echo "Monitoring status."
JOB_STATUS=""
while (!(echo "$JOB_STATUS" | grep "COMPLETED")); do 
	sleep 60
	JOB_STATUS="$(aws transcribe get-transcription-job --transcription-job-name "$JOB_ID")"
	echo -n "$(date): "
	echo "$JOB_STATUS" | grep -i status
done

echo "Downloading subs"
FILE_SRT="${FILE_OG%.mp4}.srt"
FILE_SRT_S3="s3://hfuller-transcribe/$JOB_ID.srt"
FILE_VTT="${FILE_OG%.mp4}.vtt"
FILE_VTT_S3="s3://hfuller-transcribe/$JOB_ID.vtt"
aws s3 cp "$FILE_SRT_S3" "$FILE_SRT"
aws s3 cp "$FILE_VTT_S3" "$FILE_VTT"

echo "Creating subtitled QuickTime mpeg-4 file."
FILE_SUBBED="${FILE_OG%.mp4} - Subtitled.mp4"
ffmpeg -i "$FILE_OG" -i "$FILE_SRT" -codec:v copy -codec:a copy -codec:s mov_text -metadata:s:s:0 'language=eng' -movflags '+faststart' "$FILE_SUBBED"


