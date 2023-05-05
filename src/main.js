const { exists, readTextFile, BaseDirectory, writeTextFile, readDir} = window.__TAURI__.fs;
const { Command } = window.__TAURI__.shell;
// import { readTextFile, BaseDirectory } from '@tauri-apps/api/fs';




window.addEventListener("DOMContentLoaded", () => {
  // console.log(BaseDirectory.AppConfig);

  console.log("test")
  var doesExist = false;
  const result1 = Promise.resolve(exists('.kuebikoInfo.json', { dir: BaseDirectory.Home}));
  result1.then((value) => {
    console.log(value);
    if(value){
      saveCredentials();
    } else {
      updateCredentials();
    }
  });
  //const credentialsFile = JSON.parse(result);
});

const saveCredentials = () => {
  console.log("file exists");
  const result = Promise.resolve(readTextFile('.kuebikoInfo.json', { dir: BaseDirectory.Home}));
  result.then((value) => {
    console.log(value);
    console.log(value.toString());
    var credentialsFile = JSON.parse(value.toString());
    console.log(credentialsFile.OPEN_API_KEY);
    document.getElementById("OpenAPI").value = credentialsFile.OPEN_API_KEY;
    document.getElementById("TwitchToken").value = credentialsFile.TWITCH_TOKEN;
    document.getElementById("TwitchUser").value = credentialsFile.TWITCH_CHANNEL;
    document.getElementById("GoogleCloud").value = credentialsFile.GOOGLE_JSON_PATH;
  });
}

function updateCredentials(){
  console.log("testing")
  const result = Promise.resolve(writeTextFile('.kuebikoInfo.json', 
  `{

    "currentModel" : 0,
    "TWITCH_TOKEN" : "${document.getElementById("TwitchToken").value}",
    "TWITCH_CHANNEL" : "${document.getElementById("TwitchUser").value}", 
    "OPEN_API_KEY" : "${document.getElementById("OpenAPI").value}",
    "GOOGLE_JSON_PATH" : "${document.getElementById("GoogleCloud").value}"

  }`, 
  { dir: BaseDirectory.Home}));
  result.then((value) => {
    saveCredentials();
  });
} 

async function executeScript(){
  const test = await (new Command ("list-cwd", ["-l" , "../"]).execute());
  document.getElementById("OutPut").innerHTML += (test.stdout + "<br>");
  console.log(test.stdout);
  
  const entries = await readDir('codingProjects', { dir: BaseDirectory.Home});
  var file_path = "";
  var found_file = false;
  for (const entry of entries){
    if(entry.name == "Kuebiko"){
      file_path = entry.path;
      found_file = true;
    }
  }
  if(!found_file){
    document.getElementById("OutPut").innerHTML += ("Kuebiko not found in home directory" + "<br>");
    return;
  }

  console.log(file_path);

  const command = new Command("run-python-script", ["run", "-n", "base", "--live-stream", "--no-capture-output", "python", file_path + "/main.py"]);
  //const command = new Command("test-python-script", ["../test.py"]);
  command.on('close', data => {
    console.log(`command finished with code ${data.code} and signal ${data.signal}`)
  });
  command.on('error', error => console.error(`command error: "${error}"`));

  command.stdout.on('data', line => document.getElementById("OutPut").innerHTML += (line + "<br>"));
  command.stderr.on('data', line => document.getElementById("OutPut").innerHTML += (line + "<br>"));
  const child = await command.spawn();
  console.log('pid:', child.pid)  
}

function buildEnv(){
  const result = Promise.resolve(new Command("build-conda-env", ["env", "create", "--name", "kuebiko", "--f", "../environment.yml"]).sxecute());
  result.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });
  result.then((value) => {
    console.log("test");
    console.log(value);
  });

}
