$(document).ready(function(){
$(".login_input input").focus(function(){
$(this).parents("span").css({"border":"2px solid rgb(38 43 134)","transition":".3s"});
});
$(".login_input input").blur(function(){
    $(this).parents("span").css({"border":"2px solid #e6e6e8","transition":".3s"});
    });


});

    $(document).ready(function() {
        $(".btn_icon_add").click(function() {
            var input = $(this).siblings("#fieldname2_1");
            input.val(parseInt(input.val()) + 1);
           
        });

        $(".btn_icon_sub").click(function() {
            var input = $(this).siblings("#fieldname2_1");
            if (parseInt(input.val()) > 0) {
                input.val(parseInt(input.val()) - 1);
            }
        });
    });
    
    var totalPoints = document.getElementById('totalPoints2').innerHTML;
    var differenceValue = '1000';
    var tierLevelPoints = '17999';
    var calculatePointsPercentage = (totalPoints - differenceValue) / (tierLevelPoints - differenceValue) * ('100');
    var dataPercentage = calculatePointsPercentage.toFixed(0);
    
    $(function(value){
      $("#tierPointsValue2").attr("data-percent2", dataPercentage);
      $('.target-chart2').easyPieChart({
          animate: 2000,
          lineWidth: 18,
          scaleColor: false,
          lineCap: 'square',
          size: 200,
          trackColor: "#999999",
          barColor: "#b97346" // ADVANTAGE TIER COLOR
          // #8a090d - CHOICE TIER COLOR
          // #b88c3b - PREFERRED TIER COLOR
          // #636466 - ELITE TIER COLOR
          // #000000 - OWNERS CLUB COLOR
      });
    });
    $('.totalTierPoints').each(function () {
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        }, {
            duration: 2000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });
    
   




    var totalPoints1 = document.getElementById('totalPoints1').innerHTML;
    var differenceValue1 = '1000';
    var tierLevelPoints1 = '17999';
    var calculatePointsPercentage1 = (totalPoints1 - differenceValue1) / (tierLevelPoints1 - differenceValue1) * ('100');
    var dataPercentage1 = calculatePointsPercentage1.toFixed(0);
    
    $(function(value){
      $("#tierPointsValue1").attr("data-percent1", dataPercentage1);
      $('.target-chart1').easyPieChart({
          animate: 2000,
          lineWidth: 18,
          scaleColor: false,
          lineCap: 'square',
          size: 200,
          trackColor: "#999999",
          barColor: "#b97346" // ADVANTAGE TIER COLOR
          // #8a090d - CHOICE TIER COLOR
          // #b88c3b - PREFERRED TIER COLOR
          // #636466 - ELITE TIER COLOR
          // #000000 - OWNERS CLUB COLOR
      });
    });
    $('.totalTierPoints1').each(function () {
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        }, {
            duration: 2000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });
 
