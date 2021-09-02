$(function(){
$('button').click(function(){
    var global_model = $('#global_model').val();
    var text_review = $('#input_value').val();
    $.ajax({
        url: '/fedn_predict',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response){
            $('#msg').removeClass('hide');
            $('#msg').html('<div class="alert alert-success" role="alert"> Prediction: (0 = negative, 1 = positive): '+ response+ '</div>');
            $('#msg').addClass('success');
        },
        error: function(error){
            $('#msg').removeClass('hide');
            $('#msg').html('<div class="alert alert-danger" role="alert">'+ response +'</div>');
            $('#msg').addClass('error');
        }
    });
});
});