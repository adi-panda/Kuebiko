import { writable } from "svelte/store";

export const openAPI = writable("");
export const twitchToken = writable("");
export const twitchUser = writable("");
export const googleCloud = writable("");
export const output = writable("");
export const prompt = writable("");

export const defaultState: State = {
  CURRENT_MODEL: "DAVINCI",
  CURRENT_PAGE: "HOME",
  TWITCH_TOKEN: "",
  TWITCH_CHANNEL: "",
  OPEN_API_KEY: "",
  PROMPT:
    "Simulate a twitch chat with multiple chatters, CHATTER, and DOGGIEBRO a streamer that responds using only 5 words. \n\n<<BLOCK>>",
};

export const state = writable<State>(defaultState);
