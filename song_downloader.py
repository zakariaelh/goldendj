from moviepy.editor import *
from typing import Type
from vocode.streaming.action.base_action import BaseAction, ActionOutput, ActionType, ActionInput, ActionConfig
from pydantic import BaseModel, Field

import googleapiclient.discovery
import googleapiclient.errors
from moviepy.editor import *

from pytube import YouTube
import subprocess

def youtube_to_mp3(url):
    # Define the relative output path
    output_path = "audios"
    
    # Make sure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Download the video from YouTube
    yt = YouTube(url)

    # Select the audio stream
    video = yt.streams.filter(only_audio=True).first()

    # Download the audio stream, specifying only the output path and not the filename
    out_file = video.download(output_path=output_path)

    # Extract the filename without extension and add '.mp3' for the new filename
    base = os.path.basename(out_file)
    base_name = os.path.splitext(base)[0]
    # mp3_filename = base_name + '.mp3'
    mp3_filename = 'song.mp3'
    mp3_file = os.path.join(output_path, mp3_filename)

    # Convert the file to MP3
    audioclip = AudioFileClip(out_file)
    audioclip.write_audiofile(mp3_file)

    # Remove the original download
    os.remove(out_file)

    # convert to meet twilio requirements
    twilio_filename = 'twilio-song.wav'
    output_path = os.path.join(output_path, twilio_filename)
    # convert_mp3_to_mulaw(
    #     input_file=mp3_file,
    #     output_file=output_path
    # )

    # Return the relative path to the MP3 file
    return base_name

def convert_mp3_to_mulaw(input_file: str, output_file: str) -> None:
    """
    Convert an MP3 file to a WAV file with μ-law encoding, 8000 Hz sample rate, and mono channel.

    Parameters:
    input_file (str): Path to the input MP3 file.
    output_file (str): Path to the output WAV file.
    """
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-ar", "8000",
        "-ac", "1",
        "-f", "mulaw",
        "-acodec", "pcm_mulaw",
        output_file
    ]
    subprocess.run(command, check=True)


def download_song(song_name, artist_name):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey='AIzaSyAdN7Ci2z3_MiiK_Xya8dA6yPqqpi4HagU')

    request = youtube.search().list(
        part="snippet",
        maxResults=3,
        q=f'{song_name} by {artist_name}',
        topicId="/m/04rlf"
    )
    response = request.execute()

    top_result = response['items'][0]
    result_data = {'url':f"https://www.youtube.com/watch?v={top_result['id']['videoId']}", 'title':top_result['snippet']['title'], 'description':top_result['snippet']['description']}

    out_file = youtube_to_mp3(result_data['url'])

    return out_file

class SongDownloaderActionResponse(BaseModel):
    result: str
    song_downloaded: str

class SongDownloaderActionConfig(ActionConfig, type="song_download_action"):
    pass

class SongDownloaderActionParams(BaseModel):
    song_name: str = Field(..., description="The name of the song")
    artist_name: str = Field(..., description="The name of the artist of the song")

class SongDownloaderAction(BaseAction[
    SongDownloaderActionConfig,
    SongDownloaderActionParams,
    SongDownloaderActionResponse
]):
    description: str = "This functions allows the agent to download a song directly. The agent will then play it."
    parameters_type: Type[SongDownloaderActionParams] = SongDownloaderActionParams
    response_type: Type[SongDownloaderActionResponse] = SongDownloaderActionResponse
    async def run(self, action_input: ActionInput[SongDownloaderActionParams]) -> int:
        song_name = action_input.params.song_name
        artist_name = action_input.params.artist_name
        result = download_song(song_name=song_name, artist_name=artist_name)

        # Generate and return the random number.
        return ActionOutput(
            action_type=self.action_config.type,
            response=SongDownloaderActionResponse(
                result=result,
                song_downloaded=f'{song_name} by {artist_name}'
            ))

