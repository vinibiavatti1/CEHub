const AdmZip = require('adm-zip');
const { exec } = require('child_process');
const fs = require('fs');
const gameVersionEnum = require('../enums/gameVersionEnum');
const patchEnum = require('../enums/patchEnum');
const dataService = require('./dataService');
const instanceTypeEnum = require('../enums/instanceTypeEnum');
const modalService = require('../services/modalService');

const GAME_CONTENT_PATH = __dirname + '/../../game';
const INSTANCES_PATH = __dirname + '/../../instances';
const SCRIPTS_PATH = __dirname + '/../../scripts';

function installInstance(name, version, patch, applyDgVoodoo) {
    const instancePath = INSTANCES_PATH + '/' + name;

    // Instance Installation
    try {
        fs.mkdirSync(instancePath);
        console.log('Instance home created: ' + instancePath)
        installCE(instancePath, version);
        if((version == gameVersionEnum.full.id || version == gameVersionEnum.multiplayerDemoOfficial.id) && patch != null) {
            applyPatch(instancePath, patch);
        }
        if(applyDgVoodoo == 1 && version != gameVersionEnum.multiplayerDemoMyg.id) {
            installDgVoodoo(instancePath);
        }
        console.log(`Installation done`);
        $('#install-text').html('Installation successfull!');
        $('#btn-finish').removeAttr('disabled');
        $('#btn-finish').html('Finish');
        return true;
    } catch (err) {
        $('#install-text').html('<b class="text-danger">Error!</b> ' + err.message);
        $('#btn-finish').removeAttr('disabled');
        $('#btn-finish').html('Close');
        $('#btn-finish').removeClass('btn-success');
        $('#btn-finish').addClass('btn-danger');
        return false;
    }
}

function installCE(instancePath, version) {
    let fileName = '';
    if(version == gameVersionEnum.multiplayerDemoOfficial.id) {
        fileName = 'codename-eagle-multiplayer-demo-official.zip';
    } else if(version == gameVersionEnum.multiplayerDemoUnofficial.id) {
        fileName = 'codename-eagle-multiplayer-demo-dafoosa.zip';
    } else if(version == gameVersionEnum.multiplayerDemoMyg.id) {
        fileName = 'codename-eagle-multiplayer-demo-myg.zip';
    } else {
        fileName = 'codename-eagle.zip';
    }
    let zip = new AdmZip(GAME_CONTENT_PATH + '/' + fileName);
    zip.extractAllTo(instancePath);
    console.log('CE installed');
}

function applyPatch(instancePath, patch) {
    let zip = '';
    if(patch == patchEnum.patch133.id) {
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-133.zip');
        zip.extractAllTo(instancePath, true);
    } else if(patch == patchEnum.patch133fix.id) {
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-133.zip');
        zip.extractAllTo(instancePath, true);
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-133-singleplayer-fix.zip');
        zip.extractAllTo(instancePath, true);
    } else if(patch == patchEnum.patch141.id) {
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-141.zip');
        zip.extractAllTo(instancePath, true);
    } else if(patch == patchEnum.patch142.id) {
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-141.zip');
        zip.extractAllTo(instancePath, true);
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-142.zip');
        zip.extractAllTo(instancePath, true);
    } else if(patch == patchEnum.patch143.id) {
        zip = new AdmZip(GAME_CONTENT_PATH + '/patch-143.zip');
        zip.extractAllTo(instancePath, true);
    }
    console.log(`Patch ${patch} applied`);
}

function installDgVoodoo(instancePath) {
    let zip = new AdmZip(GAME_CONTENT_PATH + '/dgvoodoo.zip');
    zip.extractAllTo(instancePath, true);
    console.log(`DgVoodoo installed`);
}

function deleteInstanceFolder(instanceName) {
    if(fs.existsSync(`${INSTANCES_PATH}/${instanceName}`)) {
        fs.rmdirSync(`${INSTANCES_PATH}/${instanceName}`, { recursive: true });
    }
}

function instanceFolderExists(instanceName) {
    return fs.existsSync(`${INSTANCES_PATH}/${instanceName}`);
}

function openInstanceFolder(instanceName) {
    if(instanceFolderExists(instanceName)) {
        exec(`start "" "${INSTANCES_PATH}/${instanceName}"`, () => {});
    }
}

function openInstanceDgVoodoo(instanceName) {
    if(instanceFolderExists(instanceName)) {
        exec(`"${INSTANCES_PATH}/${instanceName}/dgVoodooCpl.exe"`, () => {});
    }
}

function killCEProcess(callback = null) {
    exec(`${SCRIPTS_PATH}/kill_ce.bat`, () => {
        if(callback) {
            callback();
        }
    });
}

function runCE(instanceName, connect = null) {
    const instanceData = dataService.getInstance(instanceName);
    if(!instanceData) {
        modalService.message('The selected instance was not found');
        return;
    }
    let profileName = dataService.getProfileName();
    if(!profileName) {
        profileName = 'CE Player';
    }
    if(instanceData.type == instanceTypeEnum.sp.id) {
        runCESinglePlayer(
            instanceName
        );
    } else if(instanceData.type == instanceTypeEnum.client.id) {
        runCEMultiplayerClient(
            instanceName, 
            instanceData.nickname,
            instanceData.team,
            connect
        );
    } else if(instanceData.type == instanceTypeEnum.host.id) {
        runCEMultiplayerHost(
            instanceName,
            instanceData.customNickname ? instanceData.customNickname : profileName,
            instanceData.team,
            instanceData.hostname,
            instanceData.port,
            instanceData.maxPlayers,
            instanceData.customMap ? instanceData.customMap : instanceData.map,
            instanceData.gameType,
        );
    } else {
        runCEDedicated(
            instanceName, 
            instanceData.hostname,
            instanceData.port,
            instanceData.maxPlayers,
            instanceData.customMap ? instanceData.customMap : instanceData.map,
            instanceData.gameType,
        );
    }
}

function runCEWithParams(instanceName, nickname, team, hostname, port, maxPlayers, map, gameType, dedicated, connect, callback = null) {
    const instanceData = dataService.getInstance(instanceName);
    if(!instanceData) {
        modalService.message(`The instance ${instanceName} could not be found`);
        return;
    }

    // Set CE executable file
    let ceExeName = 'ce.exe';
    if(!fs.existsSync(`${INSTANCES_PATH}/${instanceName}/ce.exe`)) {
        ceExeName = 'game.exe';
    }

    // Set command
    let command = `cd "${INSTANCES_PATH}/${instanceName}" && ${ceExeName}`;
    if(instanceData.type == instanceTypeEnum.host.id || instanceData.type == instanceTypeEnum.dedicated.id) {
        if(port) {
            command += ` +host "${port}"`;
        } else {
            command += ` +host`;
        }
    }
    if(nickname) {
        command += ` +name "${nickname}"`;
    } 
    if(team) {
        command += ` +team "${team}"`;
    } 
    if(hostname) {
        command += ` +hostname "${hostname}"`;
    } 
    if(maxPlayers) {
        command += ` +maxplayers ${maxPlayers}`;
    } 
    if(map) {
        command += ` +map "${map}"`;
    } 
    if(gameType) {
        command += ` +game "${gameType}"`;
    } 
    if(dedicated) {
        command += ` +dedicated`;
    } 
    if(connect) {
        command += ` +connect ${connect}`;
    } 
    console.log('Command: ' + command);
    killCEProcess(() => {
        exec(command, () => {
            killCEProcess(callback);
        });
    });
}

function runCESinglePlayer(instanceName, callback = null) {
    runCEWithParams(instanceName, null, null, null, null, null, null, null, null, null, callback);
}

function runCEMultiplayerClient(instanceName, nickname, team, connect, callback = null) {
    runCEWithParams(instanceName, nickname, team, null, null, null, null, null, null, connect, callback);
}

function runCEMultiplayerHost(instanceName, nickname, team, hostname, port, maxPlayers, map, gameType, callback) {
    runCEWithParams(instanceName, nickname, team, hostname, port, maxPlayers, map, gameType, null, null, callback);
}

function runCEDedicated(instanceName, hostname, port, maxPlayers, map, gameType, callback) {
    runCEWithParams(instanceName, null, null, hostname, port, maxPlayers, map, gameType, true, null, callback);
}

module.exports = {
    installInstance,
    deleteInstanceFolder,
    instanceFolderExists,
    openInstanceFolder,
    openInstanceDgVoodoo,
    killCEProcess,
    runCE,
};