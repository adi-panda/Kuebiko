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

  export const executeScript = async () => {

    const resourcePath = await resolveResource("../../python_files");
    output.update((n) => n + "path + " + resourcePath + "\n");

    const command = new Command("run-python-script", [
      "run",
      "-n",
      "base",
      "--live-stream",
      "--no-capture-output",
      "python",
      resourcePath + `${sep}main.py`,
    ]);
    //const command = new Command("test-python-script", ["../test.py"]);
    command.on("close", (data) => {
      output.update((n) => (n += "command finished" + "\n"));
      console.log(
        `command finished with code ${data.code} and signal ${data.signal}`
      );
    });
    command.on("error", (error) => output.update((n) => (n += error + "\n")));

    command.stdout.on("data", (line) =>
      output.update((n) => (n += line + "\n"))
    );
    command.stderr.on("data", (line) =>
      output.update((n) => (n += line + "\n"))
    );
    const child = await command.spawn();
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
</script>

<h1>Kuebiko!</h1>
<div class="buttons">
  <button id="buildEnv" on:click={buildCondaEnv}> Build Environment! </button>
  <button id="executeScript" on:click={executeScript}> Execute Script! </button>
</div>
<h4>Output:</h4>

<div class="terminal">
  <pre>{$output}</pre>
</div>

<style lang="scss">
  .terminal {
    width: 100%;
    height: 30rem;
    padding: 1rem;
    background: #000;
    color: #0f0;
    border-radius: 10px;
    font-family: monospace;
    text-align: left;
    overflow-y: scroll;
  }
</style>
