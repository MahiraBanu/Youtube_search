import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect


search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'



def index(request):
    videos = []
    
    search_params = {
        'part' : 'snippet',
        'q' : request.POST.get('search'),
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 9,
        'type' : 'video',
    }
    
    
    r = requests.get(search_url, params=search_params)
    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    
    if request.POST.get('submit') == 'lucky':
        return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet, contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 9,
        
    }


    r = requests.get(video_url, params=video_params)
    results = r.json()['items']


    
    for result in results:

        video_data = {
            'result' : results,
            'key_words' : result['snippet'],
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : parse_duration(result['contentDetails']['duration']),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']

        }

        videos.append(video_data)

    front_end = {
        'search_params' : search_params,
        'videos' : videos,
        
    }            

    return render(request, 'my_app/index.html', front_end)

