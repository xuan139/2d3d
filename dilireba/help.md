<!-- ffmpeg helper -->
#  ffmpeg -i dilireb.mp4 -r 30 -vf scale=1964:1080 -pix_fmt rgba frames/frame_%04d.png
#  convert mp4 into png with size
#  ffmpeg -r 30 -f image2 -s 2478*1125 -i ./sbs/frame_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p result.mp4
#  -r 24 fps 
# ffmpeg -i input.mp4 -ss 00:00:00 -to 00:00:30 -c copy output.mp4  
# 按秒数0-30秒
# ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:30:00 -f segment -reset_timestamps 1 output%03d.mp4 
# 按秒数
# extra mp3 from mp4
# ffmpeg -i zhz.mp4 -vn -ar 44100 -ac 2 -ab 192k -f mp3 zhz.mp3
# combine mp3 to mp4
# ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4

#  scp zhz1.mp4 ubuntu@139.155.179.142:/home/ubuntu/superbrain/bletest/public
# 启动django
# python manage.py runserver 192.168.1.3:8000

# scp zhz1.mp4 ubuntu@139.155.179.142:/var/www/html
# /var/www/html
# 在链接的http://github.com后面加入.cnpmjs.org
# EX:git clone https://github.com/ros/rosdistro.git
# 改为git clone https://github.com.cnpmjs.org/ros/rosdistro.git

# nginx 安装

<!-- https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04 -->