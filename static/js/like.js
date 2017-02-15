$(document).ready(function(){
    $('#likeButton').on('click',function(){ 
        var likes = parseInt($(this).val())+1;
        var dislikes = parseInt($(this).next().val());
        var perL=(likes/(likes+dislikes))*100;
        var perD=(dislikes/(likes+dislikes))*100;
        $(this).siblings("div").children('#dislikes').css({"width": ""+perD+"%"});
        $(this).siblings("div").children('#likes').css({"width": ""+perL+"%"});
        $(this).val(""+likes.toString()+" Like");
        var id_img = $("this").siblings("div").children('#likes').val();
        $.ajax({
            type: 'POST',
            url: '/like/',
            data: {'id_img':id_img },
            success: function(obj){
                console.log(obj);
            },
            error:function() {
                alert('error saving like');
            }
            
    });
    $('#dislikeButton').on('click',function(){
         var dislikes = parseInt($(this).val())+1;
        var likes = parseInt($(this).prev().val());
        var perL=(likes/(likes+dislikes))*100;
        var perD=(dislikes/(likes+dislikes))*100;
        $(this).siblings("div").children('#dislikes').css({"width": ""+perD+"%"});
        $(this).siblings("div").children('#likes').css({"width": ""+perL+"%"});
        $(this).val(""+likes.toString()+" dislikes"); 
        var id_img = $("this").siblings("div").children('#likes').val();
        $.ajax({
            type: 'POST',
            url: '/dislike/',
            data: {'id_img':id_img},
            success: function(obj){
                console.log(obj);
            },
            error:function() {
                alert('error saving like');
            }
    });
});