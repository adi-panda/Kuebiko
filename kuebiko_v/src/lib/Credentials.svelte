<script lang="ts" context="module">
  import { get } from "svelte/store";
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

  let openAPIValue = "";
  let twitchTokenValue = "";
  let twitchUserValue = "";
  let googleCloudValue = "";
  let textType = "password";

  export function loadCredentials() {
    // console.log(BaseDirectory.AppConfig);

    console.log("test");
    var doesExist = false;
    const result1 = Promise.resolve(
      exists(".kuebikoInfo.json", { dir: BaseDirectory.Home })
    );
    result1.then((value) => {
      console.log(value);
      if (value) {
        readCredentials();
      } else {
        updateCredentials();
      }
    });
    //const credentialsFile = JSON.parse(result);
  }

  export const readCredentials = () => {
    console.log("file exists");
    const result = Promise.resolve(
      readTextFile(".kuebikoInfo.json", { dir: BaseDirectory.Home })
    );
    result.then((value) => {
      console.log(value);
      console.log(value.toString());
      var credentialsFile = JSON.parse(value.toString());
      console.log(credentialsFile.OPEN_API_KEY);
      openAPI.update((n) => credentialsFile.OPEN_API_KEY);
      twitchToken.update((n) => credentialsFile.TWITCH_TOKEN);
      twitchUser.update((n) => credentialsFile.TWITCH_CHANNEL);
      googleCloud.update((n) => credentialsFile.GOOGLE_JSON_PATH);
    });
  };

  export const updateCredentials = () => {
    console.log("testing");
    console.log(
      openAPIValue,
      twitchTokenValue,
      twitchUserValue,
      googleCloudValue
    );
    const result = Promise.resolve(
      writeTextFile(
        ".kuebikoInfo.json",

        `{

    "currentModel" : 0,
    "TWITCH_TOKEN" : "${get(twitchToken)}",
    "TWITCH_CHANNEL" : "${get(twitchUser)}", 
    "OPEN_API_KEY" : "${get(openAPI)}",
    "GOOGLE_JSON_PATH" : "${get(googleCloud)}"

  }`,
        { dir: BaseDirectory.Home }
      )
    );
  };
</script>

<h1>Kuebiko!</h1>
<p>Enter your credentials:(Don't share this info!)</p>
<div class="inputField">
  <input id="OpenAPI" type="password" bind:value={$openAPI} />

  <h4 class="inputLabel">Open AI API Key</h4>
</div>
<div class="inputField">
  <input id="TwitchToken" type="password" bind:value={$twitchToken} />
  <h4 class="inputLabel">Twitch Token</h4>
</div>
<div class="inputField">
  <input id="TwitchUser" type="password" bind:value={$twitchUser} />
  <h4 class="inputLabel">Twitch Username</h4>
</div>
<div class="inputField">
  <input id="GoogleCloud" type="password" bind:value={$googleCloud} />
  <h4 class="inputLabel">Google Cloud JSON Path</h4>
</div>
<div class="buttons">
  <button id="credentialsUpdate" on:click={updateCredentials}> Update! </button>
</div>
