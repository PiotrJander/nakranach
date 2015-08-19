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
});


$("#addWaitingBeerInput").select2({
    //placeholder: "wpisz fragment nazwy…",
    //allowClear: true,
    language: {
        inputTooShort: function (e) {
            var t = e.minimum - e.input.length, n = "Wprowadź jeczcze " + t + " lub więcej znaków";
            return n
        },
        searching: function () {
            return "Szukam…"
        },
        noResults: function () {
            return 'Nie znaleźliśmy pasującego piwa. Kliknij przycisk obok, żeby utworzyć nowe piwo.';
        },
    },
    ajax: {
        url: "/beers/api/search/",
        method: 'GET',
        dataType: 'json',
        delay: 1000,
        data: function (params) {
            return {
                q: params.term, // search term
                //page: params.page
            };
        },
        processResults: function (data, page) {
            // parse the results into the format expected by Select2.
            // since we are using custom formatting functions we do not need to
            // alter the remote JSON data
            return {
                results: data
            };
        },
        cache: true
    },
    //id: function (object) { return object.id },
    escapeMarkup: function (markup) {
        return markup;
    }, // let our custom formatter work
    minimumInputLength: 1,
    templateResult: formatBeer, // omitted for brevity, see the source of this page
    templateSelection: formatBeerSelection // omitted for brevity, see the source of this page
});

$("#addWaitingBeerInput").on('select2:select', function (event) { $('#addWaitingBeerForm').submit() });

function formatBeer(beer) {
    if (beer.loading) return beer.text;

    var markup = '<div>'
    markup += '<div><strong>' + beer.brewery + '</strong> ' + beer.name + '</div>'
    markup += '<div>' + beer.secondary_data + '</div>'
    markup += '</div>'

    return markup
}

function formatBeerSelection(beer) {
    return beer.text;
}