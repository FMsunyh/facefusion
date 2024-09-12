# 加载显示视频文件

# import gradio as gr
# import os

# # 获取指定目录下的所有视频文件
# def load_videos(directory):
#     video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv']  # 可根据需求增加扩展名
#     videos = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
#     return [[video] for video in videos]  # 返回列表，用于在表格中显示

# # 创建Gradio接口
# with gr.Blocks() as demo:
#     with gr.Row():
#         directory = gr.Textbox(label="输入目录路径", placeholder="请输入视频文件目录路径")
#         load_button = gr.Button("加载视频文件")
    
#     video_table = gr.Dataframe(headers=["视频文件"], datatype="str", interactive=False)

#     load_button.click(fn=load_videos, inputs=directory, outputs=video_table)

# # 启动Gradio应用
# demo.launch()


import gradio as gr
import os

# 获取指定目录下的所有视频文件
def load_videos(directory):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv']  # 可根据需求增加扩展名
    videos = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
    video_paths = [os.path.join(directory, video) for video in videos]  # 完整路径
    return [[video] for video in videos], video_paths  # 返回视频文件名和路径

# 显示视频预览
def preview_video(video_file, video_paths):
    index = video_file[0]  # 从传入的数据中获取选中视频的索引
    return video_paths[index]  # 返回选中的视频路径进行播放

# 创建Gradio接口
with gr.Blocks() as demo:
    with gr.Row():
        directory = gr.Textbox(label="输入目录路径", placeholder="请输入视频文件目录路径")
        load_button = gr.Button("加载视频文件")
    
    video_table = gr.Dataframe(headers=["视频文件"], datatype="str", interactive=True)
    video_preview = gr.Video(label="视频预览")

    video_paths = gr.State([])  # 存储视频路径

    # 加载按钮点击时加载视频
    load_button.click(fn=load_videos, inputs=directory, outputs=[video_table, video_paths])

    # 点击表格中的视频文件进行预览
    video_table.select(fn=preview_video, inputs=[video_table, video_paths], outputs=video_preview)

# 启动Gradio应用
demo.launch()
