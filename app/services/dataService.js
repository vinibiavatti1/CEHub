const fs = require('fs');
const DATA_FILE_PATH = './data/data.json';
const INITIAL_DATA_FILE_PATH = './data/data_initial.json';
const modalService = require('./modalService');

/////////////////////////////////////////////////////////////////////
// Data
/////////////////////////////////////////////////////////////////////

let _data = null;

/////////////////////////////////////////////////////////////////////
// Init
/////////////////////////////////////////////////////////////////////

function init() {
    loadData(true);
}

/////////////////////////////////////////////////////////////////////
// Private
/////////////////////////////////////////////////////////////////////

function loadData(retry = true) {
    try {
        const file = fs.readFileSync(DATA_FILE_PATH);
        _data = JSON.parse(file.toString());
    } catch(err) {
        modalService.message('An error ocurred to load data file: ' + err.message + '. The data file will be re-created');
        resetDataFile();
        if(retry) {
            loadData(false);
        }
    }
}

function saveData(data) {
    const strContent = JSON.stringify(data);
    fs.writeFileSync(DATA_FILE_PATH, strContent);
    _data = data
}

function resetDataFile() {
    const initialData = fs.readFileSync(INITIAL_DATA_FILE_PATH);
    fs.writeFileSync(DATA_FILE_PATH, initialData);
}

/////////////////////////////////////////////////////////////////////
// Public
/////////////////////////////////////////////////////////////////////

function getInstance(instanceName) {
    return _data.instances[instanceName];
}

function saveInstance(instanceName, data) {
    _data.instances[instanceName] = data;
    saveData(_data);
}

function deleteInstance(instanceName) {
    delete _data.instances[instanceName];
    saveData(_data);
}

function getInstances() {
    return _data.instances;
}

function getServer(serverName) {
    return _data.servers[serverName];
}

function getServers() {
    return _data.servers;
}

function saveServer(serverName, address) {
    _data.servers[serverName] = address;
    saveData(_data);
}

function deleteServer(serverName) {
    delete _data.servers[serverName];
    saveData(_data);
}

function getProfileName() {
    return _data.profile.name;
}

function saveProfileName(profileName) {
    _data.profile.name = profileName;
    saveData(_data);
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init,
    getInstance,
    saveInstance,
    deleteInstance,
    getServers,
    saveServer,
    deleteServer,
    getInstances,
    getServer,
    getProfileName,
    saveProfileName,
}