// Remove beer

$('#removeBeerModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var beer_id = button.data('beer-id') // Extract info from data-* attributes
    var beer_name = button.data('beer-name')
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback). //
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('#beerId').val(beer_id)
    modal.find('#beerName').text(beer_name)
})

// Modify beer

// Submit using a button outside the form
$("#waitingBeerSubmit").click(function () {
    $('#waitingBeerForm').submit();
});

// Ajax
function fillTheForms(data) {
    fillTheBeerForm(data.beer);
    fillTheWaitingbeerForm(data.waitingbeer, data.beer);
}

function fillTheBeerForm(beer_data) {
    var form = $('#beerForm')
    for (var key in beer_data) {
        form.find('input[name="' + key + '"]').val(beer_data[key])
    }
}

function fillTheWaitingbeerForm(waitingbeer_data, beer_data) {
    var form = $('#waitingBeerForm')
    for (var key in beer_data) {
        var waitingbeer_key = "_" + key
        form.find('input[name="' + waitingbeer_key + '"]')
            .val(waitingbeer_data[waitingbeer_key])
            .attr('placeholder', beer_data[key])
    }
}

$('#modifyBeerModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var beer_id = button.data('beer-id') // Extract info from data-* attributes
    var beer_name = button.data('beer-name')
    // Start AJAX
    $.get(
        "/pub/beers/api/beer",
        {id: beer_id},
        fillTheForms,
        "json"
    );
    // End AJAX
    var modal = $(this)
    modal.find('#id_beer_id').val(beer_id)
    //modal.find('#beerName').text(beer_name)
})