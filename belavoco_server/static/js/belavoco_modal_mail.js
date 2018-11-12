


function modal_upload_button_click(){

    $('#ModalEmail').modal('hide');
//TODO: add actual Upload Capability
    alert ( $("#input_upload_email").val() );
    //#creator_email
}

$('#input_upload_email').validator({
    custom: {
        emailexist: function ($el) {
            var result = checkUserEmail($el.val())
                .done(function (r) {
                    if (!r.success) {
                        // email already in use
                        return r;
                    } 
                })
            return result.responseText;
        }
    }
});


$( "input[type='checkbox']" ).change(function(){
    // Anonymer Upload wird de-/aktiviert


    if (this.checked){
        $("#input_upload_email").attr('disabled', 'disabled');
    }
    else {
        $("#input_upload_email").removeAttr('disabled');
    }

});



