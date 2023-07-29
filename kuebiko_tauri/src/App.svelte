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
    saveState($state);
  };
</script>

<title>Kuebiko</title>
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
