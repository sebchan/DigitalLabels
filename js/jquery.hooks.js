jQuery(document).ready(function() {
    
    
    $('#img, #txt').each(function(){
        var w = $(this).find('li').outerWidth() + parseFloat($(this).find('li').css('margin-right'));
        $(this).width(w*($(this).find('li:last-child').index()+1));
        this.hit = function(i){
            var t = 1024;
            $(this).animate({'left':$('body').width()/2-((i+0.5)*w)}, t);
            $(this).find('li').removeClass('active');
            $(this).find('li:nth-child('+(i+1)+')').addClass('active');
        };
        this.nudge = function(n){
            var i = $(this).find('.active').index() + n;
            this.hit(i);
        };
    });
    
    $('#txt').each(function(){
        
    });
    
    $('#img, #txt').find('li').each(function(){
        $(this).click(function(){
            var i = $(this).index();
            $('#img, #txt').each(function(){ this.hit(i); });
        });
    });
    
    $('#img li.home').click();
    $('#img, #txt').each(function(){ this.nudge(-1); });
    
}); //end doc.ready

/* plugins + fns */

/* Generic carini plugin for catching mouseclicks outside a JQ object */
(function($){
    $.fn.extend({
        mouseTrap: function(opt){
            var def = { close:this, positionMe:1, mask:0 },
                opt = $.extend(def,opt);
            return this.each(function(){
                var obj = $(this);
                if( opt.positionMe ){ obj.css({'position':'relative'}); }
                $('#mousetrap').remove();
                obj.before($('<div id="mousetrap" class="'+(opt.mask?'mask':'')+'"/>').css({'height':$(window).height(),'width':$(window).width()}).click(function(){ $(opt.close).hide(); $('#mousetrap').remove(); }));
                obj.click(function(){ if( $(opt.close).is(':hidden') ){ $('#mousetrap').remove(); } });
            });
        }
    });
})(jQuery);
