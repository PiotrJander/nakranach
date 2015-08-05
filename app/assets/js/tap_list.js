$('#emptyTapModal, #changeBeerModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var tap_id = button.data('tap-id') // Extract info from data-* attributes
    var tap_number = button.data('tap-number')
    var beer_name = button.data('beer-name')
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('#id_tap_id').val(tap_id)
    modal.find('#tapNo').text(tap_number)
    modal.find('#beerName').text(beer_name)
})
