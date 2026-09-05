function getLocation() {

    const message =
        document.getElementById("location-message");

    if (!navigator.geolocation) {

        message.innerText =
            "Geolocation is not supported by your browser.";

        return;
    }

    message.innerText =
        "Getting your location...";

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude =
                position.coords.latitude;

            const longitude =
                position.coords.longitude;


            document.getElementById("id_latitude").value =
                latitude;

            document.getElementById("id_longitude").value =
                longitude;
                document.getElementById("id_location").value =
    "Latitude: " + latitude + ", Longitude: " + longitude;


            message.innerText =
                "✓ Location detected successfully.";

        },

        function(error) {

            message.innerText =
                "Unable to get location. Please enter it manually.";

        }
    );
}
