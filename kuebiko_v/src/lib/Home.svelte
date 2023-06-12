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
  import { sep } from "@tauri-apps/api/path";

  export const executeScript = async () => {
    const test = await new Command("list-cwd", ["-l", "../"]).execute();
    // document.getElementById("OutPut").innerHTML += (test.stdout + "<br>");
    //output.update(n => n + test.stdout + "\n");
    output.update((n) => n + test.stdout + "\n");

    const entries = await readDir("", { dir: BaseDirectory.Home });
    output.update((n) => n + "test" + "\n");
    var file_path = "";
    var found_file = false;
    for (const entry of entries) {
      console.log("entry: " + entry.name);
      if (entry.name == "Kuebiko") {
        file_path = entry.path;
        found_file = true;
      }
    }
    if (!found_file) {
      // document.getElementById("OutPut").innerHTML += ("Kuebiko not found in home directory" + "<br>");
      return;
    }
    output.update((n) => n + file_path + "\n");

    const command = new Command("run-python-script", [
      "run",
      "-n",
      "base",
      "--live-stream",
      "--no-capture-output",
      "python",
      file_path + `${sep}main.py`,
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
    height: 500px;
    padding: 10px;
    background: #000;
    color: #0f0;
    border-radius: 10px;
    font-family: monospace;
    text-align: left;
  }

  .terminal pre {
    margin: 10px;
    padding: 10px;
    overflow-y: scroll;
  }
</style>
