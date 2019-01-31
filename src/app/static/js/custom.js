$(document).ready(function () {

    $(".searchbyname").hide()
    $(".searchbylocation").hide()
    $(".searchbyduration").hide()
    $(".searchbyprice").hide()

    $(".name").click(function () {

        if ($(".searchbyname").is(':hidden')) {
            //do something I am hidden!
            $(".searchbyname").slideDown();
            console.log('name clicked');
        }

        else {
            $(".searchbyname").slideUp()
        }
    });


    $(".duration").click(function () {

        if ($(".searchbyduration").is(':hidden')) {
            //do something I am hidden!
            $(".searchbyduration").slideDown();
        }

        else {
            $(".searchbyduration").slideUp()
        }
    });


    $(".location").click(function () {
        if ($(".searchbylocation").is(':hidden')) {
            //do something I am hidden!
            $(".searchbylocation").slideDown();
        }

        else {
            $(".searchbylocation").slideUp()
        }
    });

    $(".price").click(function () {

        if ($(".searchbyprice").is(':hidden')) {
            //do something I am hidden!
            $(".searchbyprice").slideDown();
        }
        else {
            $(".searchbyprice").slideUp()
        }
    });


});




jQuery(document).ready(function() {
    var x = $(".x").offset();
    var y = $('.y').offset();

    jQuery(window).scroll(function() {
        var scrolltop = jQuery(window).scrollTop();

        if ( scrolltop >= x.top && scrolltop <=y.top ) {
            jQuery(".x").addClass('fixed');
            jQuery(".y").addClass('reduce');
        } else {
            jQuery(".x").removeClass('fixed');
            jQuery(".x").removeClass('reduce');

        }

    });
