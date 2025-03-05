import gradio as gr
from gradio.flagging import FlaggingCallback

# Define a no-op flagging callback that does nothing
class NoOpFlaggingCallback(FlaggingCallback):
    def setup(self, components, directory):
        pass
    def flag(self, *args, **kwargs):
        pass

def greet(name):
    return f"Hello, {name}!"

# Use the custom no-op flagging callback to disable flagging
demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text",
    flagging_callback=NoOpFlaggingCallback(),  # disable flagging functionality
    flagging_mode="never"  # also indicate that flagging should be disabled
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)
