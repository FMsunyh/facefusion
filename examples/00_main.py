# 展示多个视频

import gradio as gr
import glob
import os
directory = '/work/facefusion/.assets/examples/'

def get_mp4_files_glob(directory):
    pattern = os.path.join(directory, '**', '*.mp4')
    mp4_files = glob.glob(pattern, recursive=True)
    mp4_files.sort(key=lambda x: os.path.basename(x))
    return mp4_files

def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            num_1 = gr.Number(value=4)
            operation = gr.Radio(["add", "subtract", "multiply", "divide"])
            num_2 = gr.Number(value=0)
            submit_btn = gr.Button(value="Calculate")
        with gr.Column():
            result = gr.Number()

    submit_btn.click(
        calculator, inputs=[num_1, operation, num_2], outputs=[result], api_name=False
    )
    examples = gr.Examples(
        examples=[
            [5, "add", 3],
            [4, "divide", 2],
            [-4, "multiply", 2.5],
            [0, "subtract", 1.2],
        ],
        inputs=[num_1, operation, num_2],
    )
    
    with gr.Row():
        with gr.Column():
            gr_video = gr.Video(label="Target", sources='upload', type="filepath", scale=0.5, value='/work/facefusion/.assets/examples/target-240p.mp4')
            video_paths = get_mp4_files_glob(directory)
            example = gr.Examples(
                label="Targets",
                inputs=gr_video,
                examples_per_page=12,
                examples=video_paths)

if __name__ == "__main__":
    demo.launch(show_api=False)