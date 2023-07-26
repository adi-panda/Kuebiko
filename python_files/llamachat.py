from llama_cpp import Llama
import copy
import json
import os

llm = Llama(
    use_mlock=False,
    n_threads=12,
    model_path=os.path.dirname(__file__)
    + "/models/Wizard-Vicuna-13B-Uncensored.ggmlv3.q4_K_S.bin",
    verbose=False,
)
print("Model loaded")


def llama_completion(
    prompt,
    repeat_penalty=2.0,
    presence_penalty=2.0,
    temperature=0.9,
    max_tokens=100,
    stop=["DOGGIEBRO:", "CHATTER:", "\n"],
    stream=False,
):
    print("running llama_completion")
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    response = llm(
        prompt,
        repeat_penalty=repeat_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        stream=stream,
    )
    text = response["choices"][0]["text"].strip()
    return text
