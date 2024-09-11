from typing import Any, Optional, List, Dict, Generator
from time import sleep, perf_counter
import tempfile
import statistics
import gradio

import facefusion.globals
from facefusion import process_manager, wording
from facefusion.face_store import clear_static_faces
from facefusion.processors.frame.core import get_frame_processors_modules
from facefusion.vision import count_video_frame_total, detect_video_resolution, detect_video_fps, pack_resolution
from facefusion.core import conditional_process
from facefusion.memory import limit_system_memory
from facefusion.filesystem import clear_temp
from facefusion.uis.core import get_ui_component

import glob
import os
directory = '/work/facefusion/data/2024-09-11'

def get_mp4_files_glob(directory):
    pattern = os.path.join(directory, '**', '*.mp4')
    mp4_files = glob.glob(pattern, recursive=True)
    mp4_files.sort(key=lambda x: os.path.basename(x))
    return mp4_files

BENCHMARK_RESULTS_DATAFRAME : Optional[gradio.Dataframe] = None
BENCHMARK_START_BUTTON : Optional[gradio.Button] = None
BENCHMARK_CLEAR_BUTTON : Optional[gradio.Button] = None
BENCHMARKS : Dict[str, str] =\
{
	'240p': '.assets/examples/target-240p.mp4',
	'360p': '.assets/examples/target-360p.mp4',
	'540p': '.assets/examples/target-540p.mp4',
	'720p': '.assets/examples/target-720p.mp4',
	'1080p': '.assets/examples/target-1080p.mp4',
	'1440p': '.assets/examples/target-1440p.mp4',
	'2160p': '.assets/examples/target-2160p.mp4'
}


def render() -> None:
	global BENCHMARK_RESULTS_DATAFRAME
	global BENCHMARK_START_BUTTON
	global BENCHMARK_CLEAR_BUTTON

	BENCHMARK_RESULTS_DATAFRAME = gradio.Dataframe(
		label = wording.get('uis.benchmark_results_dataframe'),
		headers =
		[
			'target_path',
			'process_time',
			'video_frame_total',
		],
		datatype =
		[
			'str',
			'number',
			'number'
		]
	)
	BENCHMARK_START_BUTTON = gradio.Button(
		value = wording.get('uis.start_button'),
		variant = 'primary',
		size = 'sm'
	)
	BENCHMARK_CLEAR_BUTTON = gradio.Button(
		value = wording.get('uis.clear_button'),
		size = 'sm'
	)


def listen() -> None:
	BENCHMARK_START_BUTTON.click(start,  outputs = BENCHMARK_RESULTS_DATAFRAME)
	BENCHMARK_CLEAR_BUTTON.click(clear, outputs = BENCHMARK_RESULTS_DATAFRAME)


def start() -> Generator[List[Any], None, None]:
	print("11")
	# facefusion.globals.output_path = '/work/facefusion/output'
	facefusion.globals.face_landmarker_score = 0
	facefusion.globals.temp_frame_format = 'jpg'
	facefusion.globals.output_video_preset = 'ultrafast'
	benchmark_results = []
	target_paths = get_mp4_files_glob(directory)

	if target_paths:
		pre_process()
		for target_path in target_paths:
			facefusion.globals.target_path = target_path
			benchmark_results.append(benchmark())
			yield benchmark_results
		post_process()


def pre_process() -> None:
	if facefusion.globals.system_memory_limit > 0:
		limit_system_memory(facefusion.globals.system_memory_limit)
	for frame_processor_module in get_frame_processors_modules(facefusion.globals.frame_processors):
		frame_processor_module.get_frame_processor()


def post_process() -> None:
	clear_static_faces()


def benchmark() -> List[Any]:
	video_frame_total = count_video_frame_total(facefusion.globals.target_path)
	output_video_resolution = detect_video_resolution(facefusion.globals.target_path)
	facefusion.globals.output_video_resolution = pack_resolution(output_video_resolution)
	facefusion.globals.output_video_fps = detect_video_fps(facefusion.globals.target_path)

	facefusion.globals.output_image_quality = 100
	facefusion.globals.output_video_quality = 100
	facefusion.globals.output_video_encoder = 'h264_nvenc'
	facefusion.globals.output_video_preset = 'veryslow'

	start_time = perf_counter()
	conditional_process()
	end_time = perf_counter()
	process_time = end_time - start_time

	return\
	[
		facefusion.globals.target_path,
		process_time,
  		video_frame_total
	]


def clear() -> gradio.Dataframe:
	while process_manager.is_processing():
		sleep(0.5)
	if facefusion.globals.target_path:
		clear_temp(facefusion.globals.target_path)
	return gradio.Dataframe(value = None)
