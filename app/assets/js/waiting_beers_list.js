$('#removeBeerModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var beer_id = button.data('beer-id') // Extract info from data-* attributes
    var beer_name = button.data('beer-name')
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('#beerId').val(beer_id)
    modal.find('#beerName').text(beer_name)
})

$("#waitingBeerSubmit").click(function () {
    $('#waitingBeerForm').submit();
});

