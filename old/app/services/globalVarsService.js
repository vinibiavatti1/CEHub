function getSelectedInstanceName() {
    return $('#selectedInstanceNameVar').html();
}

function setSelectedInstanceName(name) {
    $('#selectedInstanceNameVar').html(name);
}

function clearSelectedInstanceName() {
    $('#selectedInstanceNameVar').html('');
}

module.exports = {
    getSelectedInstanceName,
    setSelectedInstanceName,
    clearSelectedInstanceName
};