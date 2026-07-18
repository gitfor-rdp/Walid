import os
import subprocess
import glob

os.makedirs("output_videos", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

print("[INFO] Starting the Advanced CPA Video Factory...")

audio_files = glob.glob("downloads/*.mp3")
audio_path = audio_files[0] if audio_files else None

images_list = [img for img in os.listdir("downloads") if img.lower().endswith((".jpg", ".jpeg", ".png"))]

if not images_list:
    print("[ERROR] No images found in 'downloads' folder.")
else:
    for img in images_list:
        input_img = f"downloads/{img}"
        output_vid = f"output_videos/reel_{img.split('.')[0]}.mp4"
        print(f"[PROCESS] Creating advanced video for {img}...")
        
        filter_complex = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:20[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[outv]"
        
        if audio_path:
            print(f"[INFO] Using audio file: {audio_path}")
            cmd = f'ffmpeg -loop 1 -framerate 30 -i "{input_img}" -i "{audio_path}" -filter_complex "{filter_complex}" -map "[outv]" -map 1:a -c:v libx264 -preset fast -c:a aac -b:a 128k -t 8 -shortest -y "{output_vid}"'
        else:
            print("[WARNING] No audio found. Creating silent video.")
            cmd = f'ffmpeg -loop 1 -framerate 30 -i "{input_img}" -filter_complex "{filter_complex}" -map "[outv]" -c:v libx264 -preset fast -t 8 -y "{output_vid}"'
            
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"[SUCCESS] Video created perfectly: {output_vid}")
        except Exception as e:
            print(f"[ERROR] Failed to create video for {img}. Error: {e}")

print("[INFO] Process completed!")
