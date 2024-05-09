import gradio as gr
from gradio_client import Client

def get_speech(text, voice):
    client = Client("https://collabora-whisperspeech.hf.space/")
    result = client.predict(
    		text,	# str  in 'Enter multilingual text💬📝' Textbox component
    		voice,	# filepath  in 'Upload or Record Speaker Audio (optional)🌬️💬' Audio component
    		"",	# str  in 'alternatively, you can paste in an audio file URL:' Textbox component
    		14,	# float (numeric value between 10 and 15) in 'Tempo (in characters per second)' Slider component
    		api_name="/whisper_speech_demo"
    )
    print(result)
    return result

def get_dreamtalk(image_in, speech):
    client = Client("https://fffiloni-dreamtalk.hf.space/")
    result = client.predict(
    		speech,	# filepath  in 'Audio 👉' Audio component
    		image_in,	# filepath  in 'Image' Image component
    		"M030_front_neutral_level1_001.mat",	# Literal['M030_front_angry_level3_001.mat', 'M030_front_contempt_level3_001.mat', 'M030_front_disgusted_level3_001.mat', 'M030_front_fear_level3_001.mat', 'M030_front_happy_level3_001.mat', 'M030_front_neutral_level1_001.mat', 'M030_front_sad_level3_001.mat', 'M030_front_surprised_level3_001.mat', 'W009_front_angry_level3_001.mat', 'W009_front_contempt_level3_001.mat', 'W009_front_disgusted_level3_001.mat', 'W009_front_fear_level3_001.mat', 'W009_front_happy_level3_001.mat', 'W009_front_neutral_level1_001.mat', 'W009_front_sad_level3_001.mat', 'W009_front_surprised_level3_001.mat', 'W011_front_angry_level3_001.mat', 'W011_front_contempt_level3_001.mat', 'W011_front_disgusted_level3_001.mat', 'W011_front_fear_level3_001.mat', 'W011_front_happy_level3_001.mat', 'W011_front_neutral_level1_001.mat', 'W011_front_sad_level3_001.mat', 'W011_front_surprised_level3_001.mat']  in 'emotional style' Dropdown component
    		api_name="/infer"
    )
    print(result)
    return result['video']

def pipe (text, voice, image_in):

    speech = get_speech(text, voice)
    
    try:
        video = get_dreamtalk(image_in, speech)
    except:
       
        raise gr.Error('An error occurred while loading: Image may not contain any face - try again')

    return video

with gr.Blocks() as demo:
    with gr.Column():
        gr.HTML("""
         <h1 style="text-align: center;">
        Picture Speaks
        </h1>
        <p style="text-align: center;"></p>
        
        <h3 style="text-align: center;">
         i-Talk, you-Talk, we-Talk
        </h3>
        <p style="text-align: center;"></p>
        """)
        with gr.Row():
            with gr.Column():
                image_in = gr.Image(label="Portrait IN", type="filepath", value="./talk.jpg")
            with gr.Column():
                voice = gr.Audio(type="filepath", label="Upload or Record Speaker audio (Optional voice cloning)")
                text = gr.Textbox(label="text")
                submit_btn = gr.Button('Submit')
            with gr.Column():
                video_o = gr.Video(label="Video result")
    submit_btn.click(
        fn = pipe,
        inputs = [
            text, voice, image_in
        ],
        outputs = [
            video_o
        ],
        concurrency_limit = 3
    )
demo.queue(max_size=10).launch(show_error=True, show_api=False)