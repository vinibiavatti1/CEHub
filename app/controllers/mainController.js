const dataService = require('../services/dataService');
const instancesController = require('./instancesController');
const profileController = require('./profileController');
const menuController = require('./menuController');
const connectController = require('./connectController');
const modalService = require('../services/modalService');
const instanceFormController = require('./instanceFormController');

/////////////////////////////////////////////////////////////////////
// Init
/////////////////////////////////////////////////////////////////////

window.addEventListener('DOMContentLoaded', () => {
    // Initialize services
    dataService.init();
    modalService.init();
    
    // Initialize controllers
    menuController.init();
    instancesController.init();
    instanceFormController.init();
    profileController.init();
    connectController.init();  
});
