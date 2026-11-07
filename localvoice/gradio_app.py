from .audio import decode_audio
from .inference import transcribe
from .core import score, EXPERIMENTS


def create_app():
    import gradio as gr

    def run(path, experiment, reference):
        if not path:
            raise gr.Error("Record or upload audio first.")
        result = transcribe(decode_audio(path), experiment)
        if reference.strip():
            result["metrics"] = score([reference], [result["transcript"]])
        return result["transcript"], result

    with gr.Blocks(title="LocalVoice · Speech lab", analytics_enabled=False) as demo:
        gr.Markdown("# LocalVoice\nSpanish speech recognition · measured model comparisons")
        audio = gr.Audio(sources=["upload", "microphone"], type="filepath", format="wav", label="Speech (up to 30 seconds)")
        experiment = gr.Dropdown([e["id"] for e in EXPERIMENTS], value="E0", label="Experiment")
        reference = gr.Textbox(label="Optional reference transcript")
        run_button = gr.Button("Transcribe")
        transcript, details = gr.Textbox(label="Transcript"), gr.JSON(label="Measured details")
        run_button.click(run, [audio, experiment, reference], [transcript, details])
    return demo


def launch():
    create_app().launch(server_name="127.0.0.1", share=False)
