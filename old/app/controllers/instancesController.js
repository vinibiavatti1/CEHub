const dataService = require('../services/dataService');
const modalService = require('../services/modalService');
const instanceService = require('../services/instanceService');
const instanceTypeEnum = require('../enums/instanceTypeEnum');
const gameVersionEnum = require('../enums/gameVersionEnum');
const patchEnum = require('../enums/patchEnum');
const viewEnum = require('../enums/viewEnum');
const viewService = require('../services/viewService');
const globalVarsService = require('../services/globalVarsService');

/////////////////////////////////////////////////////////////////////
// Setup
/////////////////////////////////////////////////////////////////////

function init() {
    viewService.loadView('#instances-view', 'instancesView', onLoad, onUpdate);
}

function onLoad() {
    refreshInstanceList();
    setupButtonEvents();
}

function onUpdate() {
    refreshInstanceList();
}

/////////////////////////////////////////////////////////////////////
// Button Events
/////////////////////////////////////////////////////////////////////

function setupButtonEvents() {
    $('#btn-add').on('click', btnAddEvent);
    $('#btn-edit').on('click', btnEditEvent);
    $('#btn-run').on('click', btnRunEvent);
    $('#btn-delete').on('click', btnDeleteEvent);
    $('#btn-quick-add').on('click', btnAddEvent);
    $('#btn-refresh').on('click', btnRefrestEvent);
    $('#btn-open-folder').on('click', btnOpenFolderEvent);
    $('#btn-open-dg').on('click', btnOpenDgEvent);
    $('#btn-connect').on('click', btnConnectEvent);
}

function btnConnectEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    $('#instance-name-connect').html(globalVarsService.getSelectedInstanceName());
    viewService.changeView(viewEnum.connectView);
}

function btnOpenDgEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    instanceService.openInstanceDgVoodoo(globalVarsService.getSelectedInstanceName());
}

function btnOpenFolderEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    instanceService.openInstanceFolder(globalVarsService.getSelectedInstanceName());
}

function btnRefrestEvent() {
    refreshInstanceList();
}

function btnDeleteEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    modalService.confirm(
        `Do you really want to delete the "${globalVarsService.getSelectedInstanceName()}" instance?`,
        () => {
            deleteInstance(globalVarsService.getSelectedInstanceName());
            refreshInstanceList();
            disableInstanceButtons();
        }
    );
}

function btnRunEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    instanceService.runCE(globalVarsService.getSelectedInstanceName());
}

function selectInstanceEvent() {
    $('.instance-panel').removeClass('selected');
    $('#btn-run').attr('disabled', true);
    $('#btn-connect').attr('disabled', true);
    $('#btn-edit').removeAttr('disabled');
    $('#btn-delete').removeAttr('disabled');
    $('#btn-open-folder').removeAttr('disabled');
    $('#btn-open-dg').removeAttr('disabled');
    $(this).addClass('selected');

    const instanceType = $(this).attr('data-type');
    if(instanceType == instanceTypeEnum.dedicated.id || instanceType == instanceTypeEnum.sp.id) {
        $('#btn-run').removeAttr('disabled');
    } else {
        $('#btn-run').removeAttr('disabled');
        $('#btn-connect').removeAttr('disabled');
    }

    globalVarsService.setSelectedInstanceName($(this).attr('data-name'));
}

function btnAddEvent() {
    globalVarsService.clearSelectedInstanceName();
    viewService.changeView(viewEnum.formView);
}

function btnEditEvent() {
    if(!globalVarsService.getSelectedInstanceName()) {
        modalService.message('Please, select an instance');
        return;
    }
    const instanceData = dataService.getInstance(globalVarsService.getSelectedInstanceName());
    if(!instanceData) {
        modalService.message('The selected instance was not found');
        refreshInstanceList();
        return;
    }
    viewService.changeView(viewEnum.formView);
}

/////////////////////////////////////////////////////////////////////
// Actions
/////////////////////////////////////////////////////////////////////

function disableInstanceButtons() {
    $('#btn-run').attr('disabled', true);
    $('#btn-connect').attr('disabled', true);
    $('#btn-edit').attr('disabled', true);
    $('#btn-delete').attr('disabled', true);
    $('#btn-open-folder').attr('disabled', true);
    $('#btn-open-dg').attr('disabled', true);
}

function refreshInstanceList() {
    $('#instances').empty();
    disableInstanceButtons();
    const instances = dataService.getInstances();
    if(Object.keys(instances).length == 0) {
        $('#no-instance-message').show();
        return;
    }
    $('#no-instance-message').hide();
    for(const instanceName in instances) {
        const instanceData = instances[instanceName];
        let instanceTemplate = $('#instance-template').html();
        instanceTemplate = instanceTemplate.replace(/\{instanceName\}/g, instanceName);
        instanceTemplate = instanceTemplate.replace(/\{instanceTypeId\}/g, instanceData.type);
        instanceTemplate = instanceTemplate.replace(/\{instanceVersion\}/g, gameVersionEnum[instanceData.version].name);
        instanceTemplate = instanceTemplate.replace(/\{instancePatch\}/g, patchEnum[instanceData.patch] ? patchEnum[instanceData.patch].name : 'No Patch');
        instanceTemplate = instanceTemplate.replace(/\{instanceType\}/g, instanceTypeEnum[instanceData.type].name);
        let errorMessage = '';
        if(!instanceService.instanceFolderExists(instanceName)) {
            errorMessage = 'Could not find the folder';
        }
        instanceTemplate = instanceTemplate.replace(/\{errorMessage\}/g, errorMessage);
        $('#instances').append(instanceTemplate);
    }
    $('.instance-panel').on('click', selectInstanceEvent);
}

function deleteInstance(instanceName) {
    try {
        instanceService.deleteInstanceFolder(instanceName);
        dataService.deleteInstance(instanceName);
    } catch (err) {
        console.error(err);
        modalService.message('An error ocurred to remove the selected instance: ' + err.message);
    }
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init,
};