/**
 *
 * BASE JS
 *
 */

var CURRENT_URL_SPLITTED = window.location.href.split('#')[0].split('?')[0].split('/'),
    CURRENT_URL_FILENAME = CURRENT_URL_SPLITTED[CURRENT_URL_SPLITTED.length - 1],
    $SIDEBAR_MENU        = $('#sidebar-left');


/**
 *
 * Function: Sidebar
 *
 */
function init_sidebar() {
    // For Debug (ex. $SIDEBAR_MENU.log();)
    $.fn.log = function() {
        return this;
    };

    //if(CURRENT_URL_FILENAME) {
    //    console.log("空です");
    //} else {
    //
    // add class "active"
    var current_sidebar = $SIDEBAR_MENU.find('a[href$="'+ CURRENT_URL_FILENAME +'"]');
    current_sidebar.parent('li').addClass('nav-active');
    current_sidebar.parents('li.nav-parent').addClass('nav-expanded nav-active');
    $SIDEBAR_MENU.log();
};

/**
 *
 * Execute
 *
 */
$(document).ready(function() {
    init_sidebar();
});

