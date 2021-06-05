$(document).on('click', '.announce, #announce_cancel_btn', (e) => {
    $('.announce-area').toggleClass('d-none');
    $('.announce').toggleClass('d-none');
    $('.announce-area').find('textarea').focus();
});

$(document).on('input', '#announce_textarea', (e) => {
    let input = $('#announce_textarea');
    let space_count = 0;
    let enter_count = 0;
    for (let i of input.val()) {
        if (i == ' ') {
            space_count++;
        } else if (i == '\n') {
            enter_count++;
        }
    }
    if (input.val().toString() != '' && space_count != input.val().length && enter_count != input.val().length) {
        $('#announce_post_btn').prop('disabled', false);
    } else {
        $('#announce_post_btn').prop('disabled', true);
    }
});