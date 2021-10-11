const dataService = require('../services/dataService');
const viewService = require('../services/viewService');

/////////////////////////////////////////////////////////////////////
// Setup
/////////////////////////////////////////////////////////////////////

function init() {
    viewService.loadView('#profile-view', 'profileView', onLoad, onUpdate);
}

function onLoad() {
    refreshSidenavProfile();
    setupButtonEvents();
    setupFormEvents();
    refreshProfileData();
}

function onUpdate() {
}

/////////////////////////////////////////////////////////////////////
// Button Events
/////////////////////////////////////////////////////////////////////

function setupButtonEvents() {
    $('#btn-save-profile').on('click', btnSaveProfileEvent);
    $('#btn-cancel-profile').on('click', btnCancelProfileEvent);
} 
    
function btnSaveProfileEvent() {
    saveProfile();
    $('#btn-save-profile').attr('disabled', true);
    $('#btn-cancel-profile').attr('disabled', true);
}

function btnCancelProfileEvent() {
    $('#profile-name').val(dataService.getProfileName());
    $('#btn-save-profile').attr('disabled', true);
    $('#btn-cancel-profile').attr('disabled', true);
}

/////////////////////////////////////////////////////////////////////
// Form Validation
/////////////////////////////////////////////////////////////////////

function setupFormEvents() {
    $('#profile-name').on('keyup', profileNameKeyupEvent);
}

function profileNameKeyupEvent() {
    $('#btn-cancel-profile').removeAttr('disabled');
    let val = $(this).val();
    if(!val || val.length > 10) {
        $('#profile-name-check').html('(The profile name is invalid)');
        $('#btn-save-profile').attr('disabled', true);
        return;
    }
    $('#profile-name-check').html('');
    $('#btn-save-profile').removeAttr('disabled');
}

/////////////////////////////////////////////////////////////////////
// Actions
/////////////////////////////////////////////////////////////////////

function saveProfile() {
    const profileName = $('#profile-name').val();
    dataService.saveProfileName(profileName);
    refreshSidenavProfile();
}

function refreshProfileData() {
    $('#profile-name').val(dataService.getProfileName());
}

function refreshSidenavProfile() {
    $('#profile').html(dataService.getProfileName());
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init
};