import os
import subprocess
import urllib.request

os.makedirs("output_videos", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

print("[INFO] Starting the CPA Video Factory...")

# تجاوز حظر المواقع
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(opener)

# جلب الصوت
audio_path = "downloads/viral_beat.mp3"
if not os.path.exists(audio_path):
    print("[INFO] Downloading default audio track...")
    try:
        urllib.request.urlretrieve("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", audio_path)
    except Exception as e:
        print(f"[WARNING] Could not download audio: {e}")

# جلب الصور
images_list = [img for img in os.listdir("downloads") if img.endswith((".jpg", ".png"))]
if not images_list:
    print("[INFO] No images found! Downloading test images...")
    try:
        urllib.request.urlretrieve("https://placehold.co/1080x1920/png", "downloads/test_img_1.png")
        images_list.append("test_img_1.png")
    except Exception as e:
        print(f"[ERROR] Failed to download images: {e}")

# صناعة الفيديوهات
if images_list:
    for img in images_list:
        input_img = f"downloads/{img}"
        output_vid = f"output_videos/reel_{img.split('.')[0]}.mp4"
        print(f"[PROCESS] Generating 9:16 video for {img}...")
        
        if os.path.exists(audio_path):
            cmd = f'ffmpeg -loop 1 -framerate 30 -i "{input_img}" -i "{audio_path}" -c:v libx264 -preset ultrafast -tune stillimage -c:a aac -b:a 128k -pix_fmt yuv420p -t 8 -shortest -y "{output_vid}"'
        else:
            cmd = f'ffmpeg -loop 1 -framerate 30 -i "{input_img}" -c:v libx264 -preset ultrafast -tune stillimage -pix_fmt yuv420p -t 8 -y "{output_vid}"'
            
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"[SUCCESS] Created successfully: {output_vid}")
        except Exception as e:
            print(f"[ERROR] Error creating video for {img}: {e}")
else:
    print("[WARNING] No images found to process.")

print("[INFO] Process completed!")
