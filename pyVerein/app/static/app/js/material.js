// Top App Bar
const topAppBarElement = document.querySelector('.mdc-top-app-bar');
const topAppBar = new mdc.topAppBar.MDCTopAppBar(topAppBarElement);

// Drawer
let drawer = new mdc.drawer.MDCTemporaryDrawer(document.querySelector('.mdc-drawer--temporary'));
document.querySelector('.menu').addEventListener('click', () => drawer.open = !drawer.open);

// Floating action button
const fabRipple = new mdc.ripple.MDCRipple(document.querySelector('.mdc-fab'));

//Atrribution dialog
var dialog = new mdc.dialog.MDCDialog(document.querySelector('#attribution-dialog'));
function showAttributions() {
    dialog.lastFocusedTarget = this;
    dialog.show();
}

// Lineripple
var ripple_sel = document.querySelector('.mdc-line-ripple');
if (ripple_sel != null){
    const lineRipple = new mdc.lineRipple.MDCLineRipple();
}

// Textfield
var textfield_sel = document.querySelector('.mdc-text-field');
if (textfield_sel != null){
    const textField = new mdc.textField.MDCTextField();
}

// List
var list_ripple_sel = document.querySelectorAll('.mdc-list-item');
if (list_ripple_sel != null){
    list_ripple_sel.forEach(function(val){
        mdc.ripple.MDCRipple.attachTo(val);
    });
}