from typing import Tuple, Optional
import gradio
import os

import facefusion.globals
from facefusion import wording
from facefusion.face_store import clear_static_faces, clear_reference_faces
from facefusion.uis.typing import File
from facefusion.filesystem import get_file_size, is_image, is_video
from facefusion.uis.core import register_ui_component
from facefusion.vision import get_video_frame, normalize_frame_color

FILE_SIZE_LIMIT = 512 * 1024 * 1024

TARGET_DIRECTORY : Optional[gradio.Textbox] = None
TARGET_LOAD : Optional[gradio.Button] = None
TARGET_VIDEO_TABLE : Optional[gradio.Dataframe] = None

def render() -> None:
	global TARGET_LOAD
	global TARGET_DIRECTORY
	global TARGET_VIDEO_TABLE
 
	with gradio.Row():
		TARGET_DIRECTORY = gradio.Textbox(label="输入目录路径", placeholder="请输入视频文件目录路径")
		TARGET_LOAD = gradio.Button("加载视频文件", variant = 'primary',)

	TARGET_VIDEO_TABLE = gradio.Dataframe(headers=["视频文件"], datatype="str", interactive=False)


def listen() -> None:
	TARGET_LOAD.click(fn=load_videos, inputs=TARGET_DIRECTORY, outputs=TARGET_VIDEO_TABLE)

def load_videos(directory):
	clear_reference_faces()
	clear_static_faces()

	video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv']  # 可根据需求增加扩展名
	videos = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
	facefusion.globals.target_paths = [os.path.join(directory, video) for video in videos]  # 完整路径

	return [[video] for video in videos]  # 返回列表，用于在表格中显示
 
