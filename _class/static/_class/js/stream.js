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

$(document).on('submit', '#announce_form', (e) => {
    e.preventDefault();

    var data = new FormData();

    data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
    data.append('text', $('#announce_textarea').val());
    data.append('file', document.querySelector('#announce_add_attachment').files[0]);
    data.append('user', 1);
    data.append('classroom', 1);

    $.ajax({
        url: window.location,
        method: 'POST',
        data: data,
        processData: false,
        contentType: false,
        success: (data) => {
            e.target.reset();

            document.getElementById('announce_add_attachment').disabled = false;
            document.getElementById('announce_add_attachment_label').classList.remove('disabled');
            document.getElementById('announce_cancel_btn').disabled = false;
            // Do not un-disable the post btn
            // document.getElementById('announce_post_btn').disabled = false;

            $('.stream_posts').load(location.href + ' .e_stream_post');
        },
        beforeSend: () => {
            document.getElementById('announce_add_attachment').disabled = true;
            document.getElementById('announce_add_attachment_label').classList.add('disabled');
            document.getElementById('announce_cancel_btn').disabled = true;
            document.getElementById('announce_post_btn').disabled = true;
        },
    });
});