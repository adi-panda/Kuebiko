import { get } from "svelte/store";
import { state } from "./store";
import {
  exists,
  readTextFile,
  BaseDirectory,
  writeTextFile,
  readDir,
} from "@tauri-apps/api/fs";

export const initPrefs = async () => {
  console.log("Initializing prefs");
  const result1 = await exists(".kuebikoInfo.json", {
    dir: BaseDirectory.Home,
  });
  if (result1) {
    console.log("File Found");
    getState();
  } else {
    console.log("File Not Found");
    saveState(get(state));
  }
};

export const saveState = (currentState: State) => {
  console.log("file written");
  const result = Promise.resolve(
    writeTextFile(".kuebikoInfo.json", JSON.stringify(currentState), {
      dir: BaseDirectory.Home,
    })
  );
};

export const getState = () => {
  console.log("file exists");
  const result = Promise.resolve(
    readTextFile(".kuebikoInfo.json", { dir: BaseDirectory.Home })
  );
  result.then((value) => {
    console.log(value.toString());
    var credentialsFile = JSON.parse(value.toString());
    state.set(credentialsFile);
  });
};
