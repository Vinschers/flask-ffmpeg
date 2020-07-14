# flask-ffmpeg
Flask script that does ffmpeg operations without saving them to disk storage and yields response chunks in real time
# Usage
Simply send the input video file to the /upload route and the server will return the file generated in various chunks.
# Customization
Just change the custom_process function using whatever ffmpeg commands you need and sending a subprocess.Popen object to the `_execute_command` function.
