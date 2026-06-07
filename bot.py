import os
import subprocess
import urllib.request

# 1. إعداد المجلدات لي غنحتاجو
os.makedirs("output_videos", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

print(" Starting the CPA Video Factory...")

# 2. التأكد من وجود ملف صوتي (إلى مالقاهش غيحمل موسيقى بدون حقوق للتجربة)
audio_path = "downloads/viral_beat.mp3"
if not os.path.exists(audio_path):
    print(" Downloading default audio track...")
    try:
        urllib.request.urlretrieve("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3", audio_path)
    except Exception as e:
        print(f" Could not download audio: {e}")

# 3. جلب الصور (إلى كان مجلد التحميل خاوي، غيحمل جوج صور ذكاء اصطناعي للتجربة)
images_list = [img for img in os.listdir("downloads") if img.endswith((".jpg", ".png"))]

if not images_list:
    print(" No images found! Downloading test AI images...")
    dummy_urls = [
        "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=1080",
        "https://images.unsplash.com/photo-1682687982501-1e58f813f228?w=1080"
    ]
    for i, url in enumerate(dummy_urls):
        img_path = f"downloads/test_img_{i}.jpg"
        urllib.request.urlretrieve(url, img_path)
        images_list.append(f"test_img_{i}.jpg")

# 4. ماكينة المونتاج الأوتوماتيكي بـ FFmpeg
for img in images_list:
    input_img = f"downloads/{img}"
    output_vid = f"output_videos/reel_{img.split('.')[0]}.mp4"
    
    print(f" Generating 9:16 video for {img}...")
    
    # الكود السحري: خلفية ضبابية + مدة 8 ثواني (المدة المثالية للريلز) + معالجة سريعة (ultrafast)
    cmd = f'ffmpeg -loop 1 -framerate 30 -i "{input_img}" -i "{audio_path}" -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:20[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -preset ultrafast -tune stillimage -c:a aac -b:a 128k -pix_fmt yuv420p -t 8 -shortest -y "{output_vid}"'
    
    try:
        # تشغيل الأمر
        subprocess.run(cmd, shell=True, check=True)
        print(f" Created successfully: {output_vid}")
    except Exception as e:
        print(f" Error creating video for {img}")

print(" All videos generated! Passing them to Rclone for Google Drive upload...")
