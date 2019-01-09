$(function () {
    $.ajax({
        url:' https://api.shenjian.io/?appid=28421114fb33b6419ca765ae36546c2f',
        type:'get',
        dataType:'jsonp',
        success:function (data) {
            // console.log(data)
        },
        error:function (err) {
            console.log(err)
        }
    })
})
$(function () {
    var swiper = new Swiper('.swiper-container', {
      pagination: {
        el: '.swiper-pagination',
      },
        loop : true,
        autoplay:true,
    });
});