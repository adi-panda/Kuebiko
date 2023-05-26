
<title>Kuebiko</title>
<script lang = "ts">
import Home from "./lib/Home.svelte";
import Prompt, {loadPrompt} from "./lib/Prompt.svelte";
import Credentials, {loadCredentials} from "./lib/Credentials.svelte";

let currentScreen = "home";
let appLoaded = false;
if(!appLoaded){
  loadCredentials();
  loadPrompt();
  appLoaded = true;
}
</script>
<div class = "menuButtons">
  <button class = "menuButton" on:click={() => currentScreen = "home"}>
    Home
  </button>
  <button class="menuButton" on:click={() => currentScreen = "credentials"}>
    Credentials
  </button>
  <button class="menuButton" on:click={() => currentScreen = "Prompt"}>
    Prompt
  </button>
</div>

<section>

  {#if currentScreen === "home"}
    <Home/>
  {:else if currentScreen === "credentials"}
    <Credentials/>
  {:else if currentScreen = "Prompt"}
    <Prompt/>
  {/if}

</section>


