declare type Model = "DAVINCI" | "LLAMA" | "GPTTURBO" | "CUSTOMGPT";
declare type Page = "HOME" | "SETTINGS" | "ABOUT" | "CREDENTIALS" | "PROMPT";

declare interface State {
  CURRENT_MODEL: Model;
  CURRENT_PAGE: Page;
  TWITCH_TOKEN: string;
  TWITCH_CHANNEL: string;
  OPEN_API_KEY: string;
  PROMPT: string;
}
