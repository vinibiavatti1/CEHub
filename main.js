const { app, BrowserWindow } = require('electron');
const path = require('path');
const packageJson = require('./package.json');

/////////////////////////////////////////////////////////////////////
// Data
/////////////////////////////////////////////////////////////////////

const DEBUG = true;

/////////////////////////////////////////////////////////////////////
// Logic
/////////////////////////////////////////////////////////////////////

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 900,
        height: 600,
        title: `CEHub ${packageJson.version}`,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, './app/controllers/mainController.js')
        }
    })
    if(!DEBUG) {
        mainWindow.setMenu(null);
    }
    mainWindow.loadFile('index.html');

    // Open the DevTools.
    // mainWindow.webContents.openDevTools()
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    })
})

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
});
