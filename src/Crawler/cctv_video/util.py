import os
import shutil


file_list = os.listdir('ts_videos')
for f in file_list:
	path = os.path.join('ts_videos', f)
	if not os.listdir(path):
		shutil.rmtree(path)