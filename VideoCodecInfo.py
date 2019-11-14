from pymediainfo import MediaInfo
from pathlib import Path
import colorama
import glob

colorama.init()

p = 'Z:\\Movies'

ignore_files = [
    ".srt",
    ".sub",
    ".nfo"
]

accepted_containers = [
    "avi",
    "m2ts",
    "m4v", # i.e. mpeg4
    "mkv",
    "mov",
    "mp4",
    "ts",
    "wmv"
]

accepted_video_codecs = [
    "avc",
    "hevc",
    "mjpeg",
    "mpeg2video",
    "mpeg video", # i.e. mp2
    "mpeg4",
    "mpeg-4 visual",
    "vc1",
    "vc-1",
    "vp9",
    "wmv3"
]

accepted_audio_codecs = [
    "aac",
    "ac3",
    "ac-3",
    "dts",
    "mp2",
    "mp3",
    "mpeg audio", # i.e. MP3
    "pcm",
    "vorbis",
    "wma",
    "wmapro",
    "wmav2"
]

direct_play = []
direct_stream = []
transcode = []

for file in glob.iglob(p + '**/*.*', recursive=True):
    movie_info = MediaInfo.parse(file)

    container_ok = True
    tracks_ok = True
    num_audio_tracks = 0
    blame_tracks = {}
    
    for track in movie_info.tracks:
        if track.track_type.lower() == "general":
            if track.file_extension not in accepted_containers:
                container_ok = False
                blame_tracks['Container'] = track.file_extension
            
        if track.track_type.lower() == "video":
            if str(track.format).lower() not in accepted_video_codecs:
                tracks_ok = False
                blame_tracks['Video'] = track.format

        if track.track_type.lower() == "audio":
            num_audio_tracks += 1
            if str(track.format).lower() not in accepted_audio_codecs:
                tracks_ok = False
                blame_tracks['Audio'] = track.format

    if container_ok and tracks_ok:
        direct_play.append(file.name)
    elif not container_ok and tracks_ok:
        direct_stream.append(f"{file.name} | {blame_tracks}")
    elif not tracks_ok:
        transcode.append(f"{file.name} | Number audio tracks: {num_audio_tracks} | {blame_tracks}")
    else:
        print("How the fuck?")

print(f"{colorama.Fore.GREEN}Direct Play count: {len(direct_play)}")
print(f"{colorama.Fore.YELLOW}Direct Stream count: {len(direct_stream)}")
print(f"--------------------")
for stream in direct_stream:
    print(stream)
print(f"{colorama.Fore.RED}Transcode count: {len(transcode)}")
print(f"--------------------")
for trans in transcode:
    print(trans)