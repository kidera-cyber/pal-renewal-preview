function resizeHandler(){
    var wh = window.innerHeight;
    $("#space").css({"height":wh+'px'});
}
function scrHndl(){
    var ssh = $(window).scrollTop();
    var sh = $(window).innerHeight();
    var fh = $("#copyR").offset().top;
    var footH = $("#copyR").outerHeight(); 
    var sct = ssh + sh;
    if( sct > fh ){
        $("#linkArea").css({"position":"absolute","bottom":footH+"px"});
    }else{
        $("#linkArea").css({"position":"fixed","bottom":"0"});
        $("#linkArea").css("left", -$(window).scrollLeft());
    }
}
function topSizeHndl(){
    var bw = 1160;
    var bh = 620;
    var ww = ($('#main').width())-60*2;
    var wh = ($('#main').height())-100*2;
    var sw = ww/bw;
    var sh = wh/bh;
    var scale = Math.min(sw,sh);
    $("#mainWrap").css({"transform":"scale("+scale+")"});
}
$(function(){
    //SPACE
    $('#main').after('<div id="space"></div>');
    $('#overview .comW').after('<span id="space02"></span>');
    
	//ANCHOR SMOOTH SCROLL
	$('.anchor').click(function() {
        var ww = $(window).innerWidth();
		var speed = 800;
		var href= $(this).attr("href");
		var target = $(href == "#" || href == "" ? 'html' : href);
		var position = target.offset().top;
		$('body,html').animate({scrollTop:position}, speed, 'easeInOutQuint');
        if(ww < 661){
			$("#navWrap,#menuBtn").removeClass("active");
		}
		return false;
	});
    
    //FUNCTION CAROUSEL
    var owlFuntion = $("ul#funcList");
	owlFuntion.owlCarousel({
        margin:0,
		loop:true,
		items:1,
		autoplay:false,
		autoplayHoverPause:false,
        smartSpeed:500,
    });
    owlFuntion.on('changed.owl.carousel', function(event) {
        $("#funcNav li a, #funcDesc li, ul#funcNum li").removeClass("active");
        $("#funcNav li a:eq("+event.page.index+"),#funcDesc li:eq("+event.page.index+"),ul#funcNum li:eq("+event.page.index+")").addClass("active");
    });
    $("#funcNav li a").click(function(){
        var index = $(this).data("cindex");
        owlFuntion.trigger('to.owl.carousel',index);
    });
    $("#funcCalCont .prev a").on("click",function(){
        owlFuntion.trigger('prev.owl.carousel');
    });
    $("#funcCalCont .next a").on("click",function(){
        owlFuntion.trigger('next.owl.carousel');
    });
    
    //OPERATION CAROUSEL
    var owlOperation = $("ul#operImgList");
	owlOperation.owlCarousel({
        margin:0,
		loop:true,
		items:1,
		autoplay:false,
		autoplayHoverPause:false,
        smartSpeed:500,
    });
    owlOperation.on('changed.owl.carousel', function(event) {
        $("ul#operTxtList li,ul#operNav li a").removeClass("active");
        $("ul#operTxtList li:eq("+event.page.index+"),ul#operNav li a:eq("+event.page.index+")").addClass("active");
    });
    $("ul#operNav li a").click(function(){
        var index = $(this).data("cindex");
        owlOperation.trigger('to.owl.carousel',index);
    });
    $("#operCalCont .prev a").on("click",function(){
        owlOperation.trigger('prev.owl.carousel');
    });
    $("#operCalCont .next a").on("click",function(){
        owlOperation.trigger('next.owl.carousel');
    });
    
    //MENU TRIGGER
    $("#menuBtn").on("click",function(){
		$(this).toggleClass("active");
		$("#navWrap").toggleClass("active");
	});
    
    //LOADING
    $(window).on("load scroll resize",function(){
        var ww = $(window).innerWidth();
        if(ww > 661){
            scrHndl();
            topSizeHndl();
            resizeHandler();
        }
    });
    $(window).on('load',function(){
        $("#loading").delay(500).fadeOut(1000);
    });
});