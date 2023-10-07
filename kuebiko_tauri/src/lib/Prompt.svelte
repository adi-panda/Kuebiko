<script context="module" lang="ts">
  import {
    exists,
    readTextFile,
    BaseDirectory,
    writeTextFile,
    readDir,
  } from "@tauri-apps/api/fs";
  import { state } from "../store";
  import { get } from "svelte/store";
  import { sep, resolveResource } from "@tauri-apps/api/path";
  import { saveState } from "../prefs";
</script>

<h1>Enter your prompt here!</h1>
<p>This is what the chatbot will use to guide it's responses.</p>
<textarea bind:value={$state.PROMPT} />
<button on:click={() => saveState($state, false)}>Update Prompt</button>

<style>
  button {
    margin: 1rem 1rem 1rem 0;
    width: 10rem;
  }
</style>
