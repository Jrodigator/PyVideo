from header import create_combined_video, create_video_clip
import os, random

# Example usage
# create_combined_video(
#     video1_path="videos/gameplay.mp4",
#     video2_path="videos/advertisement.mp4",
#     start_time1=0,  # start time for video 1 in seconds
#     end_time1=10,   # end time for video 1 in seconds
#     start_time2=0,  # start time for video 2 in seconds
#     end_time2=10,   # end time for video 2 in seconds
#     caption1="Gameplay Footage",
#     caption2="Advertisement",
#     layout="top_bottom",  # layout of the combined video (side_by_side or top_bottom)
#     output_resolution=(1280, 720)  # Resolution of the final video
# )

if not os.path.exists("temp_assets"):
    os.mkdir("temp_assets")

# For Video 1
video_background_file = "videos/gameplay.mp4"
video_background_offset = 0  # Start from the beginning
image_banner_file = "videos/banner.png"
output_file1 = "videos/output_video1.mp4"
content1 = "Hello, welcome to our first video. \n This is an example of synthesized speech."

# For Video 2
video_background_file2 = "videos/advertisement.mp4"
video_background_offset2 = 0  # Start from the beginning
image_banner_file2 = "videos/banner.png"
output_file2 = "videos/output_video2.mp4"
content2 = "And here is our second video. \n We hope you find this demonstration useful."

create_video_clip(video_file=video_background_file, outfile=output_file1, image_file=image_banner_file, 
                  offset=video_background_offset, content=content1, include_sound=True)

create_video_clip(video_file=video_background_file2, outfile=output_file2, image_file=image_banner_file2, 
                  offset=video_background_offset2, content=content2, include_sound=False)

create_combined_video(
    video1_path=output_file1, 
    video2_path=output_file2, 
    start_time1=0,
    end_time1=10,
    start_time2=0,
    end_time2=10,
    layout="top_bottom", 
    output_resolution=(1280, 720)
    )