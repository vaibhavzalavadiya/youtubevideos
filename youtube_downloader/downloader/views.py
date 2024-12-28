import os
import yt_dlp
from django.shortcuts import render
from django.http import FileResponse
from .forms import YouTubeDownloadForm
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)  # Replace invalid characters


def download_video(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            try:
                # Define the output path
                output_path = os.path.join(os.getcwd(), "downloads")
                if not os.path.exists(output_path):
                    os.makedirs(output_path)  # Create 'downloads' folder if it doesn't exist

                # yt-dlp options
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'format': 'best',
                    'noplaylist': True,  # Ensure only a single video is downloaded
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    video_path = ydl.prepare_filename(info)

                # Serve the file for download
                with open(video_path, 'rb') as f:
                    response = FileResponse(f, as_attachment=True)
                    return response

            except yt_dlp.utils.DownloadError as e:
                return render(request, 'downloader/index.html', {'form': form, 'error': f"Download Error: {str(e)}"})
            except Exception as e:
                return render(request, 'downloader/index.html', {'form': form, 'error': f"Server Error: {str(e)}"})
    else:
        form = YouTubeDownloadForm()

    return render(request, 'downloader/index.html', {'form': form})
