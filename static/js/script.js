$(function() {
    $('.scroll-btn').click(function(){
        var id=$(this).attr('href');
        var position = $(id).offset().top-300;
        $('html,body').animate({
            'scrollTop': position
        }, 500);
    });

    $('.member-list').click(function() {
    var $member_name_list = $(this).find('.member-name-list');
    if($member_name_list.hasClass('open')) {
      $member_name_list.removeClass('open');
      $member_name_list.slideUp();

    } else {
      $member_name_list.addClass('open');
      $member_name_list.slideDown();
      }
  });
});
