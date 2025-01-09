import cv2
import numpy as np

video_path = 'pickcube.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频文件")
    exit()

frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("视频读取完毕或读取出错")
        break
    
    print(frame.shape)
    large_frame = np.zeros((600, 1536, 3), dtype=np.uint8)
    large_frame[88:, :, :] = frame
    
    text_positions = [(190, 40), (215+512, 40), (210+1024, 40)]
    text_labels = ["Ours", "BC", "PPO"]
    colors = [(255, 255, 255), (144, 238, 144), (230, 216, 173)]
    for pos, label, color in zip(text_positions, text_labels, colors):
        cv2.putText(large_frame, label, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2, cv2.LINE_AA)
    
    frames.append(large_frame)


cap.release()
cv2.destroyAllWindows()

output_file = 'pickcube_anno.mp4'
frame_height, frame_width, _ = frames[0].shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

for frame in frames:
    video_writer.write(frame)

video_writer.release()
