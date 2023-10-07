<script lang="ts" context="module">
  import { state } from "../store";
  import { saveState } from "../prefs";
  import { open } from "@tauri-apps/api/shell";
  import { BaseDirectory } from "@tauri-apps/api/fs";
  import { sep, resolveResource } from "@tauri-apps/api/path";

  let visible = false;

  const switchPassword = () => {
    visible = !visible;
    //@ts-ignore
    document.querySelector("#OpenAPI").type = visible ? "text" : "password";
    //@ts-ignore
    document.querySelector("#TwitchUser").type = visible ? "text" : "password";
    //@ts-ignore
    document.querySelector("#TwitchToken").type = visible ? "text" : "password";
  };
  const openFolder = async () => {
    const resourcePath = await resolveResource("../../python_files");
    const result = await open(resourcePath);
  };
</script>

<p>Enter your credentials:</p>
<p><i>(Don't share this info!)</i></p>
<div class="inputs">
  <div class="inputField">
    <h4 class="inputLabel">Open AI API Key</h4>
    <input id="OpenAPI" type="password" bind:value={$state.OPEN_API_KEY} />
  </div>
  <div class="inputField">
    <h4 class="inputLabel">Twitch Token</h4>
    <input id="TwitchToken" type="password" bind:value={$state.TWITCH_TOKEN} />
  </div>
  <div class="inputField">
    <h4 class="inputLabel">Twitch Username</h4>
    <input id="TwitchUser" type="password" bind:value={$state.TWITCH_CHANNEL} />
  </div>
</div>

<div class="buttons">
  <button on:click={() => switchPassword()} class="passwordButton">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      ><path
        fill="currentColor"
        d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5s5 2.24 5 5s-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3s3-1.34 3-3s-1.34-3-3-3z"
      /></svg
    ></button
  >
  <button class="credentialsUpdate" on:click={() => saveState($state)}>
    Update!
  </button>
  <button on:click={() => openFolder()} class="passwordButton">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      ><path
        fill="currentColor"
        d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"
      /></svg
    >
    Project Folder
    </button
  >
</div>

<style lang="scss">
  @import "../app.scss";
  .inputs{
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 2rem;
    gap: 0.5rem;
    align-items: left;
  }

  .passwordButton {
    @extend button;
    width: max-content;
    height: 2.5rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    color: white;
    align-items: center;
    text-align: center;
  }

  .credentialsUpdate{
    background-color: #00e09209;
    border-color: #00e092;
    height: 2.5rem;
    width: 100%;
  }

  .credentialsUpdate:hover{
    background-color: #00e092;
  }

  .inputField {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    align-items: left;
    text-items: left;
    width:  100%;
    h4{
      margin: 0.5rem;
    }
  }

  p{
    margin: 0rem;
    i{
      color: #989898;
      font-size: 0.75rem;
    }
  }

  input {
    font-family: monospace;
    text-align: left;
    margin: 0rem;
    padding: 0.5rem;
    width:  100%;
  }

  .buttons {
    display: grid;
    grid-template-columns: max-content 1fr max-content;
    align-items: left;
    width: 100%;
  }
</style>
