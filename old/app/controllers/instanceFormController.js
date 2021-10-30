const dataService = require('../services/dataService');
const modalService = require('../services/modalService');
const instanceService = require('../services/instanceService');
const instanceTypeEnum = require('../enums/instanceTypeEnum');
const gameVersionEnum = require('../enums/gameVersionEnum');
const viewEnum = require('../enums/viewEnum');
const viewService = require('../services/viewService');
const { getSelectedInstanceName } = require('../services/globalVarsService');

/////////////////////////////////////////////////////////////////////
// Setup
/////////////////////////////////////////////////////////////////////

function init() {
    viewService.loadView('#form-instance-view', 'formInstanceView', onLoad, onUpdate);
}

function onLoad() {
    setupButtonEvents();
    setupFormEvents();
}

function onUpdate() {
    const selectedInstanceName = getSelectedInstanceName();
    if(selectedInstanceName) {
        updateFormBySelectedInstance(selectedInstanceName);
    } else {
        updateFormWithDefaultValues();
    }
}

/////////////////////////////////////////////////////////////////////
// Button Events
/////////////////////////////////////////////////////////////////////

function setupButtonEvents() {
    $('#btn-install').on('click', btnInstallEvent);
    $('#btn-cancel').on('click', btnCancelEvent);
    $('#btn-save').on('click', btnSaveEvent);
    $('#btn-finish').on('click', btnFinishEvent);
}

function btnFinishEvent() {
    $('#install-modal').modal('hide');
    btnCancelEvent();
}

function btnCancelEvent() {
    viewService.changeView(viewEnum.instanceView);
}

function btnInstallEvent() {
    $('#install-modal').modal('show');
    $('#btn-finish').attr('disabled', true);
    $('#btn-finish').html('Please wait...');
    $('#btn-finish').removeClass('btn-danger');
    $('#btn-finish').addClass('btn-success');
    $('#install-text').html('Installing instance resources...');
    installInstance();
}

function btnSaveEvent() {
    saveInstance();
    viewService.changeView(viewEnum.instanceView);
}

/////////////////////////////////////////////////////////////////////
// Form Events
/////////////////////////////////////////////////////////////////////

function setupFormEvents() {
    $('#instance-type').on('change', instanceTypeChangeEvent);
    $('#instance-version').on('change', instanceVersionChangeEvent);
    $('#instance-name').on('keyup', instanceNameKeyupEvent);
    $('#instance-nickname').on('change', instanceNicknameChangeEvent);
    $('#instance-map').on('change', instanceMapChangeEvent);
    $('#instance-patch').on('change', instancePatchChangeEvent);
}

function instanceVersionChangeEvent() {
    $('.patch-133').show();
    $('#instance-patch').removeAttr('disabled');
    $('#instance-dg').removeAttr('disabled');
    const version = $('#instance-version').val();
    if(version == gameVersionEnum.full.id) {
        $('#version-hint').html('Full version of the game without any patch. You can install any patch you want. <b>Recommended for single player.</b>');
    } else if(version == gameVersionEnum.multiplayerDemoOfficial.id) {
        $('#version-hint').html('Official multiplayer demo version with patch v1.33 already applied. You can set other patch to be applied for this instance. <b>(It is recommended to use the Unofficial MP Version, since the servers usually use the Patch v1.43).</b>');
        $('#instance-patch').val('');
        $('.patch-133').hide();
    } else if(version == gameVersionEnum.multiplayerDemoUnofficial.id) {
        $('#version-hint').html('Dafoosa\'s MP demo version. This version already contains the patch v1.43 applied. It is recommended to be used to play on multiplayer servers, but the Myg\'s version is preferred since there are the configurations already set.');
        $('#instance-patch').val('patch143');
        $('#instance-patch').attr('disabled', true);
    } else if(version == gameVersionEnum.multiplayerDemoMyg.id) {
        $('#version-hint').html('Myg\'s MP demo version. This version already contains the patch v1.43 applied and some configurations already set. <b>This is the recommended version to play on Multiplayer Servers.</b>');
        $('#instance-patch').val('patch143');
        $('#instance-patch').attr('disabled', true);
        $('#instance-dg').val('1');
        $('#instance-dg').attr('disabled', true);
    }
}

function instancePatchChangeEvent() {
    const val = $(this).val();
    if(val.includes('4')) {
        $('#patch-hint').show();
    } else {
        $('#patch-hint').hide();
    }
}

function instanceTypeChangeEvent() {
    let val = $(this).val();
    showFormByType(val);
}

function instanceNameKeyupEvent() {
    let instanceName = $(this).val();
    if(!instanceName || instanceName.length > 20 || !/^[a-zA-Z0-9]+$/.test(instanceName)) {
        $('#instance-name-check').html('(The instance name is invalid)');
        $('#btn-install').attr('disabled', true);
        return;
    }
    if(dataService.getInstance(instanceName)) {
        $('#instance-name-check').html('(This instance name already exists)');
        $('#btn-install').attr('disabled', true);
        return;
    }
    $('#instance-name-check').html('');
    $('#btn-install').removeAttr('disabled');
}

function instanceNicknameChangeEvent() {
    let nicknameType = $(this).val();
    if(nicknameType == 'custom') {
        $('#instance-custom-nickname').show();
    } else {
        $('#instance-custom-nickname').val('');
        $('#instance-custom-nickname').hide();
    }
}

function instanceMapChangeEvent() {
    let val = $(this).val();
    if(val == 'custom') {
        $('#instance-custom-map').show();
    } else {
        $('#instance-custom-map').val('');
        $('#instance-custom-map').hide();
    }
}

/////////////////////////////////////////////////////////////////////
// Actions
/////////////////////////////////////////////////////////////////////

function updateFormBySelectedInstance(selectedInstanceName) {
    const instanceData = dataService.getInstance(selectedInstanceName);
    $('#btn-install').hide();
    $('#btn-save').show();
    $('#instance-custom-nickname').hide();
    $('#instance-custom-map').hide();
    $('#instances-view').hide();
    $('#instance-name').val(getSelectedInstanceName());
    $('#instance-version').val(instanceData.version);
    $('#instance-patch').val(instanceData.patch);
    $('#instance-type').val(instanceData.type);
    $('#instance-team').val(instanceData.team);
    $('#instance-nickname').val(instanceData.nickname);
    if(instanceData.nickname == 'custom') {
        $('#instance-custom-nickname').val(instanceData.customNickname);
        $('#instance-custom-nickname').show();
    }
    $('#instance-hostname').val(instanceData.hostname);
    $('#instance-port').val(instanceData.port);
    $('#instance-max-players').val(instanceData.maxPlayers);
    $('#instance-game-type').val(instanceData.gameType);
    $('#instance-map').val(instanceData.map);
    if(instanceData.map == 'custom') {
        $('#instance-custom-map').val(instanceData.customMap);
        $('#instance-custom-map').show();
    }
    $('#instance-dg').val(instanceData.installDgVoodoo);
    showFormByType(instanceData.type);
    instanceVersionChangeEvent();
    disableFormEditInputs();
}

function updateFormWithDefaultValues() {
    $('#instance-name').trigger('focus');
    $('#btn-install').show();
    $('#btn-save').hide();
    $('#instances-view').hide();
    $('#instance-custom-nickname').hide();
    $('#instance-custom-map').hide();
    $('#instance-name').val('');
    $('#instance-version').val('multiplayerDemoMyg');
    $('#instance-patch').val('patch143');
    $('#instance-type').val('client');
    $('#instance-team').val('');
    $('#instance-nickname').val('');
    $('#instance-hostname').val('');
    $('#instance-port').val('');
    $('#instance-max-players').val('');
    $('#instance-game-type').val('');
    $('#instance-map').val('');
    $('#instance-dg').val('1');
    showFormByType(instanceTypeEnum.client.id);
    enableFormEditInputs();
    instanceVersionChangeEvent();
}

function enableFormEditInputs() {
    $('#instance-name').removeAttr('disabled');
    $('#instance-version').removeAttr('disabled');
    $('#instance-patch').removeAttr('disabled');
    $('#instance-type').removeAttr('disabled');
    $('#instance-dg').removeAttr('disabled');
}

function disableFormEditInputs() {
    $('#instance-name').attr('disabled', true);
    $('#instance-version').attr('disabled', true);
    $('#instance-patch').attr('disabled', true);
    $('#instance-type').attr('disabled', true);
    $('#instance-dg').attr('disabled', true);
}

function showFormByType(instanceType) {
    if(instanceType == instanceTypeEnum.client.id) {
        $('#client-options').show();
        $('#server-options').hide();
    } else if(instanceType == instanceTypeEnum.host.id) {
        $('#client-options').show();
        $('#server-options').show();
    } else if(instanceType == instanceTypeEnum.dedicated.id) {
        $('#client-options').hide();
        $('#server-options').show();
    } else {
        $('#client-options').hide();
        $('#server-options').hide();
    }
}

function installInstance() {
    const instanceName = $('#instance-name').val();
    let instanceData = {
        version: $('#instance-version').val(),
        patch: $('#instance-patch').val(),
        type: $('#instance-type').val(),
        team: $('#instance-team').val(),
        nickname: $('#instance-nickname').val(),
        customNickname: $('#instance-custom-nickname').val(),
        hostname: $('#instance-hostname').val(),
        port: $('#instance-port').val(),
        maxPlayers: $('#instance-max-players').val(),
        gameType: $('#instance-game-type').val(),
        map: $('#instance-map').val(),
        customMap: $('#instance-custom-map').val(),
        installDgVoodoo: $('#instance-dg').val(),
    };
    setTimeout(() => {
        let status = instanceService.installInstance(
            instanceName, 
            instanceData.version, 
            instanceData.patch, 
            instanceData.installDgVoodoo
        );
        if (status) {
            dataService.saveInstance(instanceName, instanceData);
            // TODO refreshInstanceList();
        }
    }, 100);
}

function saveInstance() {
    const instanceName = $('#instance-name').val();
    let instanceData = dataService.getInstance(instanceName);
    if(!instanceData) {
        modalService.message('The selected instance was not found');
        // TODO refreshInstanceList();
        return;
    }
    instanceData.team = $('#instance-team').val();
    instanceData.nickname = $('#instance-nickname').val();
    instanceData.customNickname = $('#instance-custom-nickname').val();
    instanceData.hostname = $('#instance-hostname').val();
    instanceData.port = $('#instance-port').val();
    instanceData.maxPlayers = $('#instance-max-players').val();
    instanceData.gameType = $('#instance-game-type').val();
    instanceData.map = $('#instance-map').val();
    instanceData.customMap = $('#instance-custom-map').val();
    dataService.saveInstance(instanceName, instanceData);
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init,
};