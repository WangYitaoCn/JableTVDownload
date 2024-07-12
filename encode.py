import os
import subprocess
import traceback


def ffmpegEncode(folder_path, file_name, action):
    if action == 0:  #不轉檔
        return
    elif action == 1:  #快速無損轉檔
        os.chdir(folder_path)
        try:
            subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4',
                             '-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-movflags', '+faststart',
                             f'f_{file_name}.mp4'])
            os.remove(os.path.join(folder_path, f'{file_name}.mp4'))
            os.rename(os.path.join(folder_path, f'f_{file_name}.mp4'), os.path.join(folder_path, f'{file_name}.mp4'))
            print("快速無損轉檔,轉檔成功")

        except Exception as e:
            print("快速無損轉檔,轉檔失敗!")
            print(f"错误信息: {str(e)}")
            traceback.print_exc()

    elif action == 2:  #GPU轉檔
        os.chdir(folder_path)
        try:
            subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4', '-c:v', 'h264_nvenc', '-b:v', '10000K',
                             '-threads', '5', f'f_{file_name}.mp4'])
            os.remove(os.path.join(folder_path, f'{file_name}.mp4'))
            os.rename(os.path.join(folder_path, f'f_{file_name}.mp4'), os.path.join(folder_path, f'{file_name}.mp4'))
            print("GPU轉檔,轉檔成功!")

        except:
            print("GPU轉檔,轉檔失敗")
    elif action == 3:  #CPU轉檔
        os.chdir(folder_path)
        try:
            subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4', '-c:v', 'libx264', '-b:v', '3M',
                             '-threads', '5', '-preset', 'superfast', f'f_{file_name}.mp4'])
            os.remove(os.path.join(folder_path, f'{file_name}.mp4'))
            os.rename(os.path.join(folder_path, f'f_{file_name}.mp4'), os.path.join(folder_path, f'{file_name}.mp4'))
            print("CPU轉檔,轉檔成功!")

        except:

            print("CPU轉檔,轉檔失敗!")
    else:
        return
