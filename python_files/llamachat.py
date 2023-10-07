from llama_cpp import Llama
import copy
import json
import sys
import os

model_path = os.path.dirname(__file__) + "/models/llama-2-7b.Q4_K_M.gguf"
print(model_path)
llm = Llama(
    model_path=model_path,
    verbose=False,
)
print("Model loaded")


def llama_completion(
    prompt,
    repeat_penalty=2.0,
    presence_penalty=1.0,
    temperature=0.2,
    stop=["DOGGIEBRO:", "CHATTER:", "\n"],
    max_tokens=32,
):
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    response = llm(
        prompt,
        repeat_penalty=repeat_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        stop=stop,
        max_tokens=max_tokens,
    )
    text = response["choices"][0]["text"].strip()
    return text
