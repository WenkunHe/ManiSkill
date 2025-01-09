import cv2
import numpy as np

video_path = 'pickcube_ours.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频文件")
    exit()

bins = [[], [], []]
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("视频读取完毕或读取出错")
        break
    
    bins[0].append(frame[0:512, 0:512, :])
    frame_count += 1
    print(f"正在处理第 {frame_count} 帧")

cap.release()
cv2.destroyAllWindows()

video_path = 'pickcube_bc.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频文件")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("视频读取完毕或读取出错")
        break
    
    bins[1].append(frame[0:512, 0:512, :])
    frame_count += 1
    print(f"正在处理第 {frame_count} 帧")

cap.release()
cv2.destroyAllWindows()

video_path = 'pickcube_ppo.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频文件")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("视频读取完毕或读取出错")
        break
    
    bins[2].append(frame[0:512, 0:512, :])
    frame_count += 1
    print(f"正在处理第 {frame_count} 帧")

cap.release()
cv2.destroyAllWindows()

frame_counts = [len(bin) for bin in bins]
print(frame_counts)
if len(set(frame_counts)) != 1:
    raise ValueError("每个 bin 中的帧数量不一致，无法拼接视频")

# 获取帧大小信息
frame_height, frame_width, frame_channels = bins[0][0].shape
output_height = frame_height * 1  # 拼接后高度为 2 倍单帧高度
output_width = frame_width * 3   # 拼接后宽度为 4 倍单帧宽度

# 初始化视频写入器
output_path = "pickcube.mp4"
fps = 30  # 设置帧率
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 输出格式
out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

# 按帧拼接
for i in range(frame_counts[0]):
    # 从每个 bin 中取出对应帧
    frame_0 = bins[0][i]
    frame_1 = bins[1][i]
    frame_2 = bins[2][i]
    #frame_3 = bins[3][i]
    #frame_4 = bins[4][i]
    #frame_5 = bins[5][i]
    #frame_6 = bins[6][i]
    #frame_7 = bins[7][i]
    
    # 横向拼接成 1x4 布局
    top_row = np.hstack((frame_0, frame_1, frame_2))
    #bottom_row = np.hstack((frame_4, frame_5, frame_6, frame_7))
    
    # 纵向拼接成 2x4 布局
    #full_frame = np.vstack((top_row, bottom_row))
    
    # 写入视频
    out.write(top_row)

# 释放视频写入器
out.release()
print(f"视频保存到 {output_path}")