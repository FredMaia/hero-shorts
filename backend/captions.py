from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import whisper_timestamped as whisper

from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})


filename = "./short.mp4"

screen_width = 1080
screen_height = 1920

def get_transcribed_text(filename):
    audio = whisper.load_audio(filename)
    model = whisper.load_model("small", device="cpu")
    results = whisper.transcribe(model, audio, language="en")

    return results["segments"]

def get_text_clips(text, fontsize):
    text_clips = []
    for segment in text:
        for word in segment["words"]:
            text_clips.append(
                TextClip(word["text"],
                    fontsize=fontsize,
                    method='caption',
                    stroke_width=5, 
                    stroke_color="white", 
                    font="Arial-Bold",
                      color="white")
                .set_start(word["start"])
                .set_end(word["end"])   
                .set_position("center")
            )
    return text_clips

# Loading the video as a VideoFileClip
original_clip = VideoFileClip(filename)

# Load the audio in the video to transcribe it and get transcribed text
transcribed_text = get_transcribed_text(filename)
# Generate text elements for video using transcribed text
text_clip_list = get_text_clips(text=transcribed_text, fontsize=90)
# Create a CompositeVideoClip that we write to a file
final_clip = CompositeVideoClip([original_clip] + text_clip_list)

final_clip.write_videofile("final.mp4", codec="libx264")