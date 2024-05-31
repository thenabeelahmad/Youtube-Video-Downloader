from pytube import YouTube, Playlist
from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    if request.method == 'POST':
        url = request.POST.get('ytlink')
        if 'playlist' in url:
            # Handle playlist
            return handle_playlist(request, url)
        else:
            # Handle single video
            return handle_single_video(request, url)
    return render(request, 'index.html')

def handle_single_video(request, url):
    embedlink = url.replace("watch?v=", "embed/")
    try:
        yt = YouTube(url)
        # Get all available streams
        streams = yt.streams.filter(progressive=True).all()
        stream_options = []
        for stream in streams:
            stream_options.append({
                'resolution': stream.resolution,
                'mime_type': stream.mime_type,
                'url': stream.url
            })

        video_details = {
            'title': yt.title,
            'thumbnail_url': yt.thumbnail_url,
            'views': yt.views,
            'length': yt.length,
            'author': yt.author,
            'description': yt.description,
            'publish_date': yt.publish_date,
            'embedlink': embedlink,
            'streams': stream_options,
        }

        context = {
            'yobj': video_details,
            'embedlink': embedlink
        }
        return render(request, 'home.html', context)
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse(f"An error occurred: {e}")

def handle_playlist(request, url):
    try:
        pl = Playlist(url)
        videos = []
        for video in pl.videos:
            stream_options = []
            streams = video.streams.filter(progressive=True).all()
            for stream in streams:
                stream_options.append({
                    'resolution': stream.resolution,
                    'mime_type': stream.mime_type,
                    'url': stream.url
                })
            videos.append({
                'title': video.title,
                'thumbnail_url': video.thumbnail_url,
                'views': video.views,
                'length': video.length,
                'author': video.author,
                'description': video.description,
                'publish_date': video.publish_date,
                'streams': stream_options,
            })

        context = {
            'playlist_title': pl.title,
            'videos': videos,
        }
        return render(request, 'playlist.html', context)
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse(f"An error occurred: {e}")
