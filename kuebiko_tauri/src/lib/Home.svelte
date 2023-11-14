<script lang="ts">
  import {
    openAPI,
    twitchToken,
    twitchUser,
    googleCloud,
    output,
  } from "../store";
  import {
    exists,
    readTextFile,
    BaseDirectory,
    writeTextFile,
    readDir,
  } from "@tauri-apps/api/fs";
  import { Command } from "@tauri-apps/api/shell";
  import { sep, resolveResource } from "@tauri-apps/api/path";

  let runningBot = false;
  let child = null;

  export const executeScript = async () => {
    if (runningBot) return;
    runningBot = true;
    const resourcePath = await resolveResource("../../python_files" );
    output.update((n) => n + "path + " + resourcePath + "\n");

    let currentBot = new Command("run-python-script", [
      "run",
      "-n",
      "base",
      "--live-stream",
      "--no-capture-output",
      "python",
      resourcePath + `${sep}main.py`,
    ]);
    //const command = new Command("test-python-script", ["../test.py"]);
    currentBot.on("close", (data) => {
      output.update((n) => (n += "command finished" + "\n"));
      console.log(
        `command finished with code ${data.code} and signal ${data.signal}`
      );
    });
    currentBot.on("error", (error) => {
      output.update((n) => (n += error + "\n"));
      runningBot = false;
    });

    currentBot.stdout.on("data", (line) =>
      output.update((n) => (n += line + "\n"))
    );
    currentBot.stderr.on("data", (line) =>
      output.update((n) => (n += line + "\n"))
    );
    child = await currentBot.spawn();
    output.update((n) => (n += "pid: " + child.pid + "\n"));
    console.log("pid:", child.pid);
  };

  export const buildCondaEnv = async () => {
    const result = new Command("build-conda-env", [
      "env",
      "create",
      "--name",
      "kuebiko",
      "--f",
      `${sep}environment.yml`,
    ]).execute();
  };

  export const stopScript = async () => {
    if (child) {
      await child.kill();
      child = null;
      runningBot = false;
      output.update((n) => (n += "Script stopped by user\n"));
    }
  };
</script>

<div class="buttons">
  <button id="buildEnv" on:click={buildCondaEnv}> Build Environment! </button>
  <button id="executeScript" on:click={executeScript}> Execute Script! </button>
  <button
    class:grey-button={!runningBot}
    id="stopScript"
    on:click={() => {
      stopScript();
    }}
  >
    Stop Script!
  </button>
  <button
    on:click={() => {
      $output = "";
    }}
  >
    Clear</button
  >
</div>
<h4>Output:</h4>

<div class="terminal">
  <pre>{$output}</pre>
</div>

<style lang="scss">
  .grey-button {
    border-color: #989898;
    color: #989898;
  }
  .grey-button:hover {
    background-color: #98989800;
    transform: none;
  }
  .terminal {
    width: 100%;
    height: 100%;
    padding: 1rem;
    background: #000;
    color: #0f0;
    border-radius: 10px;
    font-family: monospace;
    text-align: left;
    overflow-y: scroll;
  }
</style>
