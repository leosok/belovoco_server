
$( "input[type='checkbox']" ).change(function(){
    // Anonymer Upload wird de-/aktiviert


    if (this.checked){
        $("#input_upload_email").attr('disabled', 'disabled');
    }
    else {
        $("#input_upload_email").removeAttr('disabled');
    }
    
});
