"use strict";

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const ipc = ipcMain

// Keep a global reference of the mainWindowdow object, if you don't, the mainWindowdow will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow = null;
let loadingScreen = null;
let subpy = null;

const PY_DIST_FOLDER = "dist-python"; // python distributable folder
const PY_ROOT_FOLDER = "run_app"; // python distributable folder
const PY_SRC_FOLDER = "web_app"; // path to the python source
const PY_MODULE = "run_app.py"; // the name of the main module

const isRunningInBundle = () => {
  return require("fs").existsSync(path.join(__dirname, PY_DIST_FOLDER));
};

const getPythonScriptPath = () => {
  if (!isRunningInBundle()) {
    return path.join(__dirname, PY_SRC_FOLDER, PY_MODULE);
  }
  if (process.platform === "win32") {
    return path.join(
      __dirname,
      PY_DIST_FOLDER,
      PY_ROOT_FOLDER,
      PY_MODULE.slice(0, -3) + ".exe"
    );
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE);
};

const startPythonSubprocess = () => {
  let script = getPythonScriptPath();
  if (isRunningInBundle()) {
    subpy = require("child_process").execFile(script, []);
  } else {
    subpy = require("child_process").spawn("python", [script]);
  }
};

const killPythonSubprocesses = (main_pid) => {
  const python_script_name = path.basename(getPythonScriptPath());
  let cleanup_completed = false;
  const psTree = require("ps-tree");
  psTree(main_pid, function (err, children) {
    let python_pids = children
      .filter(function (el) {
        return el.COMMAND == python_script_name;
      })
      .map(function (p) {
        return p.PID;
      });
    // kill all the spawned python processes
    python_pids.forEach(function (pid) {
      process.kill(pid);
    });
    subpy = null;
    cleanup_completed = true;
  });
  return new Promise(function (resolve, reject) {
    (function waitForSubProcessCleanup() {
      if (cleanup_completed) return resolve();
      setTimeout(waitForSubProcessCleanup, 30);
    })();
  });
};

// Loading Screen
function createLoadingScreen() {
  loadingScreen = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    resizable: false,
  })

  loadingScreen.loadFile('splash/index.html')

  loadingScreen.on('closed', () => {
    loadingScreen = null
  })
  
  loadingScreen.webContents.on('did-finish-load', () => {
    loadingScreen.show()
  })
}

// Main Window
const createMainWindow = () => {
  // Create the browser mainWindow
  mainWindow = new BrowserWindow({
    show: false,
    frame: false,
    resizeable: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      devTools: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Load the index page
  mainWindow.loadURL("http://localhost:4040/");

  //// CLOSE APP
  ipc.on('minimizeApp', ()=>{
    mainWindow.minimize()
  })

  //// MAXIMIZE RESTORE APP
  ipc.on('maximizeRestoreApp', ()=>{
      if(mainWindow.isMaximized()){
          mainWindow.restore()
      } else {
          mainWindow.maximize()
      }
  })
  // Check if is Maximized
  mainWindow.on('maximize', ()=>{
      mainWindow.webContents.send('isMaximized')
  })
  // Check if is Restored
  mainWindow.on('unmaximize', ()=>{
      mainWindow.webContents.send('isRestored')
  })

  //// CLOSE APP
  ipc.on('closeApp', ()=>{
      mainWindow.close()
  })

  // Open the DevTools.
  mainWindow.webContents.openDevTools();

  // Emitted when the mainWindow is closed.
  mainWindow.on("closed", function () {
    // Dereference the mainWindow object
    mainWindow = null;
  });

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
    mainWindow.maximize()
  })

  // mainWindow.once('ready-to-show', () => {
  //   mainWindow.maximize()
  // })
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", function () {
  // start the backend server
  startPythonSubprocess();
  createLoadingScreen()
  setTimeout(() => {
    if (loadingScreen) {
      loadingScreen.close()
    }
    createMainWindow()
    mainWindow.show()
  }, 1000);
});

// disable menu
app.on("browser-window-created", function (e, window) {
  window.setMenu(null);
});

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    let main_process_pid = process.pid;
    killPythonSubprocesses(main_process_pid).then(() => {
      app.quit();
    });
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (subpy == null) {
    startPythonSubprocess();
  }
  if (win === null) {
    createMainWindow();
  }
});

app.on("quit", function () {
  // do some additional cleanup
});
