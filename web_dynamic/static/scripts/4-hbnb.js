$( document ).ready(function() {
    const api = 'http://' + window.location.hostname;
    $.get(api + ':5001/api/v1/status', function(response) {
        if (response.status === 'OK') {
            $("#api_status").addClass('available');
        } else {
            $("#api_status").removeClass('available');
        }
    });

    $.ajax({
        url: api + ':5001/api/v1/places_search/',
        type: 'POST',
        data: '{}',
        contentType: 'application/json',
        dataType: 'json',
        success: handleClick
    })
    
    let amenities = {};
     $('input[type="checkbox"]').change(function() {
         if ($(this).is(':checked')) {
             amenities[$(this).attr('data-id')] = $(this).attr('data-name');
         } else {
             delete amenities[$(this).attr('data-id')];
         }
         $(".amenities h4").text(Object.values(amenities).join(', '));
     });

    $("button").click(function() {
        $.ajax({
            url: api + ':5001/api/v1/places_search/',
            type: 'POST',
            data: JSON.stringify({'amenities': Object.keys(amenities)}),
            contentType: 'application/json',
            dataType: 'json',
            success: handleClick
        })
    })
});

function handleClick(data) {
    $(".places").empty();
    $(".places").append(data.map(place => {
        return `<article>
        <div class="headline">
            <h2>${place.name}</h2>
            <div class="price_by_night">$${place.price_by_night}</div>
        </div>
        <div class="information">
            <div class="max_guest">
                <div class="guest_icon"></div>
                <p>${place.max_guest} Guest</p>
            </div>
            <div class="number_rooms">
                <div class="bed_icon"></div>
                <p>${place.number_rooms} Room</p>
            </div>
            <div class="number_bathrooms">
                <div class="bath_icon"></div>
                <p>${place.number_bathrooms} Bathroom</p>
            </div>
        </div>
        <div class="description">
        ${place.description}
        </div>
        </article>`
    }))
}