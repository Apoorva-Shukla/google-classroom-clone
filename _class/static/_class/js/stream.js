$(document).on('click', '.announce, #announce_cancel_btn', (e) => {
    $('.announce-area').toggleClass('d-none');
    $('.announce').toggleClass('d-none');
    $('.announce-area').find('textarea').focus();
});

function validatePostForm() {
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
}

$(document).on('input', '#announce_textarea', (e) => {
    validatePostForm();
});

$(document).on('click', '#announce_cancel_btn', (e) => {
    $('.clear_attachment').click();
});

$(document).on('submit', '#announce_form', (e) => {
    e.preventDefault();

    let data = new FormData();

    data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
    data.append('text', $('#announce_textarea').val());
    data.append('file', document.querySelector('#announce_add_attachment').files[0]);
    data.append('user', 1);
    data.append('classroom', 1);
    data.append('_name', 'post');

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
            document.querySelector('#announce_textarea').disabled = false;
            // Do not un-disable the post btn
            // document.getElementById('announce_post_btn').disabled = false;

            document.querySelector('#announce_add_attachment').value = '';
            document.querySelector('#announce_textarea').value = '';
            document.querySelector('.attachment_preview_fluid').innerHTML = '';
            document.querySelector('.attachment_preview').classList.add('d-none');

            // updating the post section
            $('.stream_posts').load(location.href + ' .stream_posts_fluid');
            // updating the pagination button section
            $('.pagination_buttons').load(location.href + ' .pagination_buttons_fluid');
        },
        beforeSend: () => {
            document.getElementById('announce_add_attachment').disabled = true;
            document.getElementById('announce_add_attachment_label').classList.add('disabled');
            document.getElementById('announce_cancel_btn').disabled = true;
            document.getElementById('announce_post_btn').disabled = true;
            document.querySelector('#announce_textarea').disabled = true;
        },
        error: () => {
            alert('Something went wrong, please try again');
            document.getElementById('announce_add_attachment').disabled = false;
            document.getElementById('announce_add_attachment_label').classList.remove('disabled');
            document.getElementById('announce_cancel_btn').disabled = false;
            document.querySelector('#announce_textarea').disabled = false;

            validatePostForm();
        },
    });
});

$(document).on('input', '#announce_add_attachment', (e) => {
    let fileInput = document.querySelector('#announce_add_attachment');
    let file = fileInput.files[0];
    let previewArea = document.querySelector('.attachment_preview');
    let previewAreaFluid = document.querySelector('.attachment_preview_fluid');
    previewArea.classList.remove('d-none');

    var html = '';
    let url;
    if (file.type.includes('image')) {
        url = URL.createObjectURL(file);
        html = `<img src="${url}" alt=" " class="max_image">`;
    } else if (file.type.includes('video')) {
        url = URL.createObjectURL(file);
        html = `<video src="${url}" controls class="max_image"></video>`;
    } else if (file.type.includes('audio')) {
        url = URL.createObjectURL(file);
        html = `<audio src="${url}" controls></audio>`;
    } else {
        html = `
            <div class="py-5 text-white">
                <span class="px-2 py-3 mx-3" style="background-color: #f34646;border-radius: 3px 20px 3px 3px;">
                    <span>${file.name.toString().split('.')[file.name.toString().split('.').length-1]}</span>
                </span>
                <span>${file.name.toString()}</span>
            </div>
        `;
    }

    previewAreaFluid.innerHTML = html;
});

$(document).on('click', '.clear_attachment', (e) => {
    document.querySelector('#announce_add_attachment').value = '';
    document.querySelector('.attachment_preview_fluid').innerHTML = '';
    document.querySelector('.attachment_preview').classList.add('d-none');
});

// post comment
$(document).on('submit', '.post_comment_form', (e) => {
    e.preventDefault();

    let data = new FormData();
    let text = document.getElementById(`${e.target.id.toString().replace('form', 'input')}`);
    data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
    data.append('post', Number(e.target.id.toString().replace('_post_comment_form', '')));
    data.append('text', text.value);
    data.append('_name', 'comment');

    $.ajax({
        url: window.location,
        method: 'POST',
        data: data,
        processData: false,
        contentType: false,
        success: (data) => {
            text.disabled = false;
            text.value = '';

            // render newest comment
            let comment = $.parseJSON(data.comment)[0].fields;
            let avatar = data.avatar;
            let user = data.user;

            let id = `#${e.target.id.toString().replace('_post_comment_form', '')}_comments_section`;
            let commentSection = $(id).find('div.comments_section_fluid');
            commentSection.parent().removeClass('d-none');

            let avatarHtml = ''
            if (avatar == '') {
                avatarHtml = `<img class="photo" src="../../../media/defaults/user/default_user_img.png" alt=" ">`
            } else {
                avatarHtml = `<img class="photo" src="${avatar}" alt=" ">`
            }

            let months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

            let date = comment.date.split('-')[2];
            let mon = months[Number(comment.date.split('-')[1]) - 1];
            let year = comment.date.split('-')[0];

            let hour = comment.time.split(':')[0];
            let min = comment.time.split(':')[1];

            commentSection.prepend(`
            <div class="e_comment py-2">
                <div class="d-flex">
                    <div class="mx-3 my-auto" style="margin-left: 0!important;">
                        ${avatarHtml}
                    </div>
                    <div class="my-auto">
                        <div>
                            <span class="text-secondary">${user}</span>
                            <small class="text-secondary">${mon} ${Number(date)}, ${year} ${hour}:${min}</small>
                        </div>
                        <div>
                            <span>${comment.text}</span>
                        </div>
                    </div>
                </div>
            </div>
            `);
        },
        beforeSend: () => {
            text.disabled = true;
        },
        error: () => {
            alert('Something went wrong, please try again')
            text.disabled = false;
            text.focus();
        },
    });
});

function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);

    // kvp looks like ['key1=value1', 'key2=value2', ...]
    var kvp = document.location.search.substr(1).split('&');
    let i=0;

    for(; i<kvp.length; i++){
        if (kvp[i].startsWith(key + '=')) {
            let pair = kvp[i].split('=');
            pair[1] = value;
            kvp[i] = pair.join('=');
            break;
        }
    }

    if(i >= kvp.length){
        kvp[kvp.length] = [key,value].join('=');
    }

    // can return this or...
    let params = kvp.join('&');

    // reload page with new params
    document.location.search = params;
}