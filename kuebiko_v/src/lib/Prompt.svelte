<script context="module" lang = "ts">
import { exists, readTextFile, BaseDirectory, writeTextFile, readDir} from '@tauri-apps/api/fs';
import { prompt } from '../store';
import { get } from 'svelte/store';
import { sep } from '@tauri-apps/api/path';
export const loadPrompt = () => {
  
  const result = Promise.resolve(readTextFile(`KuebikoV2${sep}prompt_chat.txt`, { dir: BaseDirectory.Home}));
  console.log("test");
  result.then((value) => {
    prompt.update(n => value.toString());
  });
}

export const updatePrompt = () => {
  const result = Promise.resolve(writeTextFile(`KuebikoV2${sep}prompt_chat.txt`, get(prompt), { dir: BaseDirectory.Home}));
  result.then((value) => {
    console.log("updated prompt");
  });
}
</script>
<h1>Enter your prompt here!</h1>
<p>This is what the chatbot will use to guide it's responses.
</p>
<textarea bind:value = {$prompt}></textarea>
<button on:click={updatePrompt}>Update Prompt</button>

