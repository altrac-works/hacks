#!/usr/bin/env bash
set -euf -o pipefail

FILES="$(cat rsm.txt | sort -R)"
for FILE in $FILES; do
	echo "=== $FILE ==="
	if [ ! -f "rsm/$FILE.srt" ]; then
		CMD="time ./hear -i \"rsm/$FILE\" -S > \"rsm/$FILE.srt\""

		echo "Starting transcription. Hit return if you want me to stop after this file"
		echo "$CMD"

		bash -c "$CMD" || echo "Transcription failed; leaving empty output"

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
