$(document).ready(function () {
    $(document).on('click', '.show-modal', function (e) {
        e.preventDefault();
        const dataset = this.dataset;
        $('body').css('overflow', 'hidden');
        showModal(dataset.type, dataset.src, dataset.download, dataset.title, dataset.id, dataset.profile, dataset.location, dataset.caption);
        $('.pop-story').attr('data-slide', dataset.slide).addClass('md-show');
    });
    
    $(document).on('click', '.pop-up .fa-chevron-right, .pop-up .fa-chevron-left', function (e) {
        let slide = parseInt($(this).parent().attr('data-slide'));
        let length = $('.modal-item').length - 1;
        if ($(this).hasClass('fa-chevron-right')) {
            slide ++;
            slide = slide > length ? 0 : slide;
        } else {
            slide --;
            slide = slide < 0 ? length : slide;
        }
        $(this).parent().attr('data-slide', slide);
        const dataset = $('.modal-item').eq(slide).find('p')[0].dataset;
        showModal(dataset.type, dataset.src, dataset.download, dataset.title, dataset.id, dataset.profile, dataset.location, dataset.caption);
    });
    $('.pop-story').swipe({
        swipeStatus: function (event, phase, direction) {
            if (phase === "end") {
                if (direction === 'left') {
                    $('.pop-up .fa-chevron-right').trigger('click');
                }else if (direction === 'right') {
                    $('.pop-up .fa-chevron-left').trigger('click');
                }else if (direction === 'up' || direction === 'down') {
                    $('.close').trigger('click');
                }
            }
        }, excludedElements: "label, button, input, select, textarea, a, .noSwipe",
    });
    $(window).on('keydown', function (e) {
        if(e.keyCode === 37){
            $('.pop-up .fa-chevron-left').trigger('click');
        }else if(e.keyCode === 39){
            $('.pop-up .fa-chevron-right').trigger('click');
        }
    });
    $('.md-overlay, .close-search, .close').click(function (e) {
        e.preventDefault();
        $('body').css('overflow', '');
        $('.pop-up').removeClass('md-show');
        $('.pop-story .pop-content').html('');
    });
});
function showModal(type, src, download, title, storyId, profile, location, caption) {
    $('.story-pic').attr('src', profile);
    $('.story-name').text(title);
    $('.story-caption').html(caption + ' - at  <strong>' + location + '</strong>');
    $('.download').attr('href',src);
    if (type === "photo") {
        $('.pop-content').html('<img class="inst-content" src="'+src+'">');
    } else {
        if(src.indexOf('iphone') + 1) {
            $.ajax({
                url: src,
                method: 'get',
            }).done(function (data) {
                $('.pop-content').html('<video class="inst-content" src="'+data+'" controls="" playsinline="" webkit-playsinline=""></video>');
                $('.pop-up video')[0].play();
            });
        }else{
            $('.pop-content').html('<video class="inst-content" src="'+src+'" controls="" playsinline="" webkit-playsinline=""></video>');
            $('.pop-up video')[0].play();
        }
    }
    if (storyId && !getCookie('story_'+storyId)) {
        setCookie('story_'+storyId,'true',1);
        const countElement = $('.avatar .count');
        if (countElement) {
            const countStories = parseInt(countElement.text()) - 1;
            if (countStories <= 0) {
                $('.avatar').removeClass('user-info-avatar-active');
                countElement.remove();
            }else{
                countElement.text(countStories)
            }
        }
    }
}

function timestampToTime(unix_timestamp, onlyTime = false){
    const date = new Date(unix_timestamp * 1000);
    const hours = date.getHours();
    const minutes = "0" + date.getMinutes();
    if(onlyTime){
        return  hours + ':' + minutes.substr(-2);
    }
    const year = date.getFullYear();
    const month = date.getMonth();
    const day = date.getDate();
    return  year + '-' + day + '-' + month + ' ' + hours + ':' + minutes.substr(-2);
}

