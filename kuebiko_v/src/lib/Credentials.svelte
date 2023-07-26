<script lang="ts" context="module">
  import { state } from "../store";
  import { saveState } from "../prefs";

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
</script>

<h1>Kuebiko!</h1>
<p>Enter your credentials:(Don't share this info!)</p>
<div class="inputField">
  <input id="OpenAPI" type="password" bind:value={$state.OPEN_API_KEY} />
  <h4 class="inputLabel">Open AI API Key</h4>
</div>
<div class="inputField">
  <input id="TwitchToken" type="password" bind:value={$state.TWITCH_TOKEN} />
  <h4 class="inputLabel">Twitch Token</h4>
</div>
<div class="inputField">
  <input id="TwitchUser" type="password" bind:value={$state.TWITCH_CHANNEL} />
  <h4 class="inputLabel">Twitch Username</h4>
</div>

<div class="buttons">
  <button id="credentialsUpdate" on:click={() => saveState($state)}>
    Update!
  </button>
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
</div>

<style>
  input {
    font-size: small;
  }
  .passwordButton {
    width: 2rem;
    height: 2rem;
  }
  .buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
