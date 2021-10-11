const dataService = require('../services/dataService');
const modalService = require('../services/modalService');
const viewEnum = require('../enums/viewEnum');
const instanceService = require('../services/instanceService');
const { getSelectedInstanceName } = require('../services/globalVarsService');
const viewService = require('../services/viewService');

/////////////////////////////////////////////////////////////////////
// Setup
/////////////////////////////////////////////////////////////////////

function init() {
    viewService.loadView('#connect-view', 'connectView', onLoad, onUpdate);
}

function onLoad() {
    refreshServerList();
    setupFormEvents();
    setupButtonEvents();
}

function onUpdate() {
}

/////////////////////////////////////////////////////////////////////
// Button Events
/////////////////////////////////////////////////////////////////////

function setupButtonEvents() {
    $('#btn-cancel-connect').on('click', btnCancelEvent);
    $('#refresh-server-list').on('click', btnRefreshServerListEvent);
    $('#btn-address-add').on('click', btnAddressAddEvent);
    $('#btn-direct-connect').on('click', btnDirectConnectEvent);
}

function btnDirectConnectEvent() {
    const address = $('#address-direct').val();
    connect(address);
}

function btnCancelEvent() {
    viewService.changeView(viewEnum.instanceView);
}

function btnRefreshServerListEvent() {
    refreshServerList();
}

function btnAddressAddEvent() {
    const serverAddress = $('#server-address').val();
    const serverName = $('#server-name').val();
    if(!serverName) {
        modalService.message('You must enter an address name.');
        return;
    }
    if(!serverAddress) {
        modalService.message('You must enter an address.');
        return;
    }
    if(dataService.getServer(serverName)) {
        modalService.message('Address not saved. The identifier already exists!');
        return;
    }
    dataService.saveServer(serverName, serverAddress);
    $('#server-address').val('');
    $('#server-name').val('');
    refreshServerList();
}

/////////////////////////////////////////////////////////////////////
// Form Events
/////////////////////////////////////////////////////////////////////

function setupFormEvents() {
    $('#address-direct').on('keyup', addressDirectKeyupEvent);
    $('#server-address').on('keyup', addressEvent);
    $('#server-name').on('keyup', addressEvent);
}

function addressEvent() {
    const serverAddress = $('#server-address').val();
    const serverName = $('#server-name').val();
    if(serverAddress && serverName) {
        $('#btn-address-add').removeAttr('disabled');
    } else {
        $('#btn-address-add').attr('disabled', true);
    }
}

function addressDirectKeyupEvent() {
    const val = $('#address-direct').val();
    if(val) {
        $('#btn-direct-connect').removeAttr('disabled');
    } else {
        $('#btn-direct-connect').attr('disabled', true);
    }
}

/////////////////////////////////////////////////////////////////////
// Server List Events
/////////////////////////////////////////////////////////////////////

function setupServerListEvents() {
    $('.btn-delete-server').on('click', btnDeleteServer);
    $('.btn-join-server').on('click', btnConnectEvent);
}

function btnConnectEvent() {
    const address = $(this).attr('data-address');
    connect(address);
}

function btnDeleteServer() {
    const serverName = $(this).attr('data-name');
    modalService.confirm(
        `Do you really want to delete the "${serverName}" address?`,
        () => {
            dataService.deleteServer(serverName);
            refreshServerList();
        },
    );
}

/////////////////////////////////////////////////////////////////////
// Actions
/////////////////////////////////////////////////////////////////////

function refreshServerList() {
    $('#server-list').empty();
    const servers = dataService.getServers();
    for(const serverName in servers) {
        const serverAddress = servers[serverName];
        let template = `
        <tr>
            <td>${serverName}</td>
            <td>${serverAddress}</td>
            <td>
                <button data-address="${serverAddress}" class="btn-join-server btn btn-success">Join!</button>
                <button data-name="${serverName}" class="btn-delete-server btn btn-danger">Delete</button>
            </td>
        </tr>
        `;
        $('#server-list').append(template);
    }
    setupServerListEvents();
}

function connect(address) {
    if(!address) {
        modalService.message('Please, enter an address to join');
        return;
    }
    instanceService.runCE(getSelectedInstanceName(), address);
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init,
};