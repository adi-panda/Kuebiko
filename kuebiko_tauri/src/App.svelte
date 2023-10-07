<script lang="ts">
  import Home from "./lib/Home.svelte";
  import Prompt from "./lib/Prompt.svelte";
  import Credentials from "./lib/Credentials.svelte";
  import { state } from "./store";
  import { initPrefs, saveState, getState } from "./prefs";
  import { onMount } from "svelte";
  onMount(() => {
    initPrefs();
  });

  const changeScreen = (screen: Page) => {
    $state.CURRENT_PAGE = screen;
    saveState($state, false);
  };
</script>

<div class="app">
  <div class="logo-holder">
    <h1>kuebiko.</h1>
  </div>
  <div class="menuButtons">
    <button class="menuButton" on:click={() => changeScreen("HOME")}>
      Home
    </button>
    <button class="menuButton" on:click={() => changeScreen("CREDENTIALS")}>
      Credentials
    </button>
    <button class="menuButton" on:click={() => changeScreen("PROMPT")}>
      Prompt
    </button>
  </div>

  {#if $state.CURRENT_PAGE === "HOME"}
    <Home />
  {:else if $state.CURRENT_PAGE === "CREDENTIALS"}
    <Credentials />
  {:else if $state.CURRENT_PAGE === "PROMPT"}
    <Prompt />
  {/if}
</div>

<style>
  h1 {
    font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
      "Lucida Sans", Arial, sans-serif;
  }
  .logo-holder {
    margin-top: -3rem;
  }
  .app {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-right: 2rem;
    height: calc(100vh - 9rem);
  }
  .menuButtons {
    margin-bottom: 2rem;
  }
</style>
