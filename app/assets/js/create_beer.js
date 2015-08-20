$('#chooseBreweryField, #chooseStyleField').select2();
$('#addNewBreweryInputs').hide()
$('#chooseBreweryField').prop('required', true)


$('#createNewBreweryCheckbox').change(function() {
    if (this.checked) {
        $('#chooseBreweryField')
            .hide()
            .select2('destroy')
            .prop('required', false)
        $('label[for="chooseBreweryField"]').hide()
        $('#addNewBreweryInputs')
            .show()
            .prop('required', true)
    } else {
        $('#chooseBreweryField')
            .show()
            .select2()
            .prop('required', true)
        $('label[for="chooseBreweryField"]').show()
        $('#addNewBreweryInputs')
            .hide()
            .prop('required', false)
    }
});