import os
import pysrt
import unidecode
import requests
from random import randint
from subtitle_scraper import *
from tqdm import tqdm
import youtube_dl

api_key = "dc6zaTOxFJmzC"

def download_meme_gif(idx, query):
    params = {'q': query, 'api_key': api_key, 'limit': 3,'rating': 'pg'}
    r = requests.get("http://api.giphy.com/v1/gifs/search", params=params)
    data = r.json()['data']
    try:
        gif_url = data[randint(0,len(data)-1)]["images"]['original_mp4']['mp4']
    except:
        gif_url = data[randint(0,len(data)-1)]["images"]["images"]['downsized_small']['mp4']
    r = requests.get(gif_url)
    st = "./memes/"+str(idx)+".mp4"
    with open(st, 'wb') as f:
        f.write(r.content)


def get_file_by_extension(project_dir, extension):
    for filename in os.listdir(project_dir):
        if filename.endswith(extension):
            return filename


def generate_video(project_name, project_dir):
    from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

    os.chdir(project_dir)
    try:
        os.mkdir("memes")
    except:
        pass

    subtitles = pysrt.open(get_file_by_extension(project_dir, 'srt'))

    texts = [s.text for s in subtitles]
    
    durations = []
    for x in range(len(subtitles)):
        try:
            duration = subtitles[x+1].start - subtitles[x].start
        except:
            duration = subtitles[x].duration
        d = round((duration.seconds*1000 + duration.milliseconds)/1000,3)
        durations.append(d)

    print("Fetching {len(subtitles)} memes.")
    for idx, text in tqdm(enumerate(texts), total=len(subtitles)):
        try:
            query = unidecode.unidecode(text).replace('*****', 'k')
            print(idx, query)
            download_meme_gif(idx, query)
        except:
            query = "imagination spongebob"
            download_meme_gif(idx, query)


    print("Joining clips.")
    clips = []

    for x in range(len(texts)):
        st = "./memes/"+str(x)+".mp4"
        clip = VideoFileClip(st)
        lclip = clip.resize((400,400)).loop(duration=durations[x])
        clips.append(lclip)

    aclip = AudioFileClip(get_file_by_extension(project_dir, 'mp3'))
    audio_start = round((subtitles[0].start.minutes*60*1000 + subtitles[0].start.seconds*1000 + subtitles[0].start.milliseconds)/1000,3)
    aclip = aclip.subclip(t_start=audio_start)

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(aclip)
    print("Writing your awesome music video!")
    ss = project_name+".mp4"
    final_clip.write_videofile(ss)


if __name__ == '__main__':
    url = input("Enter URL of YouTube video: ") 

    # fetch video info and downnload audio
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        result = ydl.extract_info(url, download=False)

    # get project title/name
    query = result['title']
    print("Creating your project.")
    try:
        os.mkdir(query.replace(' ', '-'))
    except:
        pass
    os.chdir(os.getcwd()+'/'+query.replace(' ', '-'))
    project_dir = os.getcwd()
    project_name = query.replace(' ', '_')

    # download audio
    print("Downloading audio.")
    st = "youtube-dl --extract-audio --audio-format mp3 " + url
    call(st, shell=True)

    # find subtitles
    print("Finding subtitles for", query)
    browser = start_browser(project_dir)
    subs = get_available_subs(query, browser)
    print("Following subtitles were found:")
    for idx,sub in enumerate(subs):
        print(idx+1, sub['name'])
    choice = int(input("Select the subtitle no. to download: "))-1
    
    # download subtitle
    download_sub(subs[choice], browser)
    print("Successfully downloaded subtitle.")

    # generate video
    print("Generating video.")
    generate_video(project_name, project_dir)