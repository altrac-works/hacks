#!/usr/bin/env bash
set -euf -o pipefail

FILES="$(cat rsm.txt | sort -R)"

echo > tried.txt
for FILE in $FILES; do
	echo "=== $FILE ==="
	if [ ! -f "rsm/$FILE.srt" ]; then
		echo "$FILE" >> tried.txt
		#CMD="time ./hear -i \"rsm/$FILE\" -S > \"rsm/$FILE.srt\""

		#HACK: We pass tdrz but we arent loading a tdrz model. For now.
		CMD="time ./build/bin/whisper-cli -m models/ggml-small.en.bin --output-srt --output-vtt --tinydiarize -f \"rsm/$FILE\""

		echo "Starting transcription. Hit return if you want me to stop after this file"
		echo "$CMD"

		bash -c "$CMD" #|| echo "Transcription failed; leaving empty output"

		if read -t 1; then
			echo "stopping because you typed something"
			exit 130
			sleep 420691337
		fi
		echo
	else
		echo "Already transcribed"
	fi
done
