const viewEnum = require('../enums/viewEnum');

/////////////////////////////////////////////////////////////////////
// Public
/////////////////////////////////////////////////////////////////////

function loadView(selector, fileName, onLoadFn, onUpdateFn) {
    $(selector).load(__dirname + '/../../views/' + fileName + '.html', () => {
        $(selector).on('update', onUpdateFn);
        onLoadFn();
    });
}

function changeView(view) {
    // Hide views
    for(const key in viewEnum) {
        $(viewEnum[key].selector).hide();
    }
    
    // Open view
    $(view.selector).show();
    $(view.selector).trigger('update');
}

/////////////////////////////////////////////////////////////////////
// Exports
/////////////////////////////////////////////////////////////////////

module.exports = {
    loadView,
    changeView
}