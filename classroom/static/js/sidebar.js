$(document).on('click', '.hide-sidebar', (e) => {
    document.querySelector('.sidebar').style.boxShadow = 'none';
    document.querySelector('.sidebar').style.width = '0';
});

$(document).on('click', '.show-sidebar', (e) => {
    document.querySelector('.sidebar').style.width = '350px';
    document.querySelector('.sidebar').style.boxShadow = '0 0 13px 2px #999';
});