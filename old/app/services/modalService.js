/////////////////////////////////////////////////////////////////////
// Init
/////////////////////////////////////////////////////////////////////

function init() {
    setupModalEvents();
}

/////////////////////////////////////////////////////////////////////
// Events
/////////////////////////////////////////////////////////////////////

function setupModalEvents() {
    $('#btn-message-modal-ok').on('click', btnModalMessageOkClickEvent);
}

function btnModalMessageOkClickEvent() {
    console.log('asdsad');
    $('#message-modal').modal('hide');
}

/////////////////////////////////////////////////////////////////////
// Public
/////////////////////////////////////////////////////////////////////

function message(message){
    $('#message-modal-text').html(message);
    $('#message-modal').modal('show');
}

function confirm(message, onConfirm, onCancel = null){
    $('#confirm-modal-text').html(message);
    $('#confirm-modal').modal('show');
    $('#btn-confirm-modal-ok').off('click');
    $('#btn-confirm-modal-cancel').off('click');
    $('#btn-confirm-modal-ok').on('click', () => {
        $('#confirm-modal').modal('hide');
        onConfirm();
    });
    $('#btn-confirm-modal-cancel').on('click', () => {
        $('#confirm-modal').modal('hide');
        if(onCancel) {
            onCancel();
        }
    });
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    init,
    message,
    confirm,
}