$(document).ready(function(){
    $('.likeButton').on('click',function(){ 
        var obj = $(this).val();
        var likes = parseInt(obj)+1;
        $(this).val(""+likes.toString()+" Like");
        var id_img = $("this").siblings("div").children('#likes').val();
        $.ajax({
            type: 'POST',
            url: '/like/',
            data: {'id_img',id_img},
            success: function(obj){
                console.log(obj);
            },
            error(function() {
                alert('error saving like');
            });
            
    });
    $('.dislikeButton').on('click',function(){
        var obj = $(this).val();
        var likes = parseInt(obj)+1;
        $(this).val(""+likes.toString()+" dislikes"); 
        var id_img = $("this").siblings("div").children('#likes').val();
        $.ajax({
            type: 'POST',
            url: '/dislike/',
            data: {'id_img',id_img},
            success: function(obj){
                console.log(obj);
            },
            error(function() {
                alert('error saving like');
            });
    });
});