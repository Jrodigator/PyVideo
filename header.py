from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip, concatenate_audioclips, concatenate_videoclips
from gtts import gTTS
import os
from rich.console import Console
from rich.progress import track


'''Full combined video (2 videos)'''
def create_combined_video(video1_path, video2_path, start_time1, end_time1, start_time2, end_time2, caption1="", caption2="", layout="side_by_side", output_resolution=(1280, 720)):
    # Load the video clips
    clip1 = VideoFileClip(video1_path).resize(width=output_resolution[0]//2)
    clip2 = VideoFileClip(video2_path).resize(width=output_resolution[0]//2)
    # .subclip(start_time1, end_time1)  .subclip(start_time2, end_time2)


    # Set resolution for each clip based on layout
    if layout == "side_by_side":
        clip1 = clip1.resize(width=output_resolution[0]//2)
        clip2 = clip2.resize(width=output_resolution[0]//2)
    elif layout == "top_bottom":
        clip1 = clip1.resize(height=output_resolution[1]//2)
        clip2 = clip2.resize(height=output_resolution[1]//2)

    # Add optional captions
    if caption1:
        txt_clip1 = TextClip(caption1, fontsize=24, color='white').set_position(('center', 'bottom')).set_duration(clip1.duration)
        clip1 = CompositeVideoClip([clip1, txt_clip1])

    if caption2:
        txt_clip2 = TextClip(caption2, fontsize=24, color='white').set_position(('center', 'bottom')).set_duration(clip2.duration)
        clip2 = CompositeVideoClip([clip2, txt_clip2])

    # Combine the clips based on layout
    if layout == "side_by_side":
        final_clip = CompositeVideoClip([clip1.set_position("left"), clip2.set_position("right")], size=output_resolution)
    elif layout == "top_bottom":
        final_clip = CompositeVideoClip([clip1.set_position("top"), clip2.set_position("bottom")], size=output_resolution)

    # Output the final video
    final_clip.write_videofile("videos/output.mp4", fps=24)

'''Speech generation using gTTS for testing'''
def generate_speech(text, lang='en', filename='audio.mp3'):
    myobj = gTTS(text=text, lang=lang, slow=False, tld='ca')
    myobj.save(filename)
    return filename

def split_text(text, delimiter='\n'):
    return text.split(delimiter)

def generate_audio_text(fulltext):
    audio_comp = []
    text_comp = []

    for idx, text in track(enumerate(fulltext), description='Synthesizing Audio...'):
        if text == "":
            continue
        audio_file = f"temp_assets/audio_{idx}.mp3"
        generate_speech(text.strip(), filename=audio_file)
        audio_duration = AudioFileClip(audio_file).duration
        text_clip = TextClip(text, fontsize=32, color="white",
                             align='center', method='caption', size=(660, None))
        text_clip = text_clip.set_duration(audio_duration)
        audio_comp.append(audio_file)
        text_comp.append(text_clip)
    return audio_comp, text_comp

def create_video_clip(video_file, outfile, image_file='', offset=0, duration=0, content='', include_sound=True):
    vid_clip = VideoFileClip(video_file).subclip(offset, offset + duration).resize((1980, 1280))
    vid_clip = vid_clip.crop(x_center=1980 / 2, y_center=1280 / 2, width=720, height=1280)

    if image_file != '':
        image_clip = ImageClip(image_file).set_duration(duration).set_position(("center", 'center')).resize(0.8)
        vid_clip = CompositeVideoClip([vid_clip, image_clip])

    if include_sound:
        audio_comp, text_comp = generate_audio_text(split_text(content))
        audio_comp_list = [AudioFileClip(audio) for audio in audio_comp]
        audio_comp_stitch = concatenate_audioclips(audio_comp_list)
        audio_duration = audio_comp_stitch.duration
        if duration == 0:
            duration = audio_duration
        audio_comp_stitch.write_audiofile('temp_audio.mp3', fps=44100)
        audio_comp_stitch.close()
        vid_clip = vid_clip.set_audio(AudioFileClip('temp_audio.mp3').subclip(0, duration))
    else:
        vid_clip = vid_clip.without_audio()

    vid_clip.write_videofile(outfile, fps=24)
    vid_clip.close()
