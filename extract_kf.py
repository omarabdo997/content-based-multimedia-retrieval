import cv2
import os
import subprocess

videourl = "./videos/lava1.mp4"


def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def save_i_keyframes(video_fn):
    frame_types = get_frame_types(video_fn)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    frames = []
    if i_frames:

        cap = cv2.VideoCapture(video_fn)
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            frames.append(frame)
        cap.release()

    return frames

def extract_images(video_url):
        images = save_i_keyframes(video_url)
    basename = "videos/" + os.path.splitext(os.path.basename(video_url))[
        0]+'/'
    if not os.path.exists(basename):
        os.mkdir(path=basename)

    for i, image in enumerate(images):
        print(i)
        outname = basename+'_i_frame_'+str(i)+'.jpg'
        cv2.imwrite(outname, image)
        
if __name__ == "__main__":
    extract_images(videourl)

