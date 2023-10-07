import { get } from "svelte/store";
import { state } from "./store";
import {
  exists,
  readTextFile,
  BaseDirectory,
  writeTextFile,
  createDir,
} from "@tauri-apps/api/fs";
import { appDataDir, sep } from "@tauri-apps/api/path";

export const initPrefs = async () => {
  console.log("Initializing prefs");
  const result1 = await exists(`.kuebikoInfo.json`, {
    dir: BaseDirectory.AppData,
  });
  if (result1) {
    console.log("File Found");
    getState();
  } else {
    console.log("File Not Found");
    saveState(get(state), true);
  }
};

export const saveState = async (currentState: State, first: boolean) => {
  if (first) await createDir(await appDataDir());
  const result = Promise.resolve(
    writeTextFile(".kuebikoInfo.json", JSON.stringify(currentState), {
      dir: BaseDirectory.AppData,
    })
  );
};

export const getState = () => {
  console.log("file exists");
  const result = Promise.resolve(
    readTextFile(".kuebikoInfo.json", { dir: BaseDirectory.AppData })
  );
  result.then((value) => {
    console.log(value.toString());
    var credentialsFile = JSON.parse(value.toString());
    state.set(credentialsFile);
  });
};
