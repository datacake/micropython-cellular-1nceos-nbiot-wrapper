/*
    Cellular UDP Standard Device Template for API Devices
    (c) Datacake GmbH
    Feel free to modify
*/

// helper function
function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;
}

// actual decoder
function Decoder(request) {

    // convert the incoming webhook payload to json object
    var payload = JSON.parse(request.body);

    // access reports inside webhook from iotcreators
    var reports = payload.reports;

    // we will need this to store data we want to send to datacake
    var datacakeFields = [];

    // webhook from iotcreators can contain more than one device
    for (var i = 0; i < reports.length; i++) {

        var report = reports[i];
        
        // extract serial number or IMEI from report
        // one report = one device
        var serial = report.serialNumber;

        // extract sensor payload
        var sensorPayload = report.value;

        // convert byte string into hex-buffer
        // we need to do this in order to work with byte decoding
        var bytes = hexToBytes(sensorPayload);

        // extract and convert bytes
        var temperature = ((bytes[0] << 8) + bytes[1]) / 10.0;
        var humidity = ((bytes[2] << 8) + bytes[3]) / 10.0;
        var battery = bytes[4] / 10.0;
        var pressure = ((bytes[5] << 8) + bytes[6]);
        var light = ((bytes[7] << 8) + bytes[8]);
        var lte_seconds = ((bytes[9] << 8) + bytes[10]);
        
        // Example for GPS Location
        var lat = 53.362; // please adapt to your device
        var lon = 6.394; // please adapt 
        var location = "(" + lat + "," + lon + ")";

      	// now create an array which we are forwarding to Datacake
        // this array should contain dictionaries each holding a measurement value
        datacakeFields.push(
            {
                "device": serial, // serial number so IMEI of Device on Datacake
                "field": "TEMPERATURE", // field identifier on database
                "value": temperature, // value for field coming out of webhook
            },
            {
                "device": serial,
                "field": "HUMIDITY",
                "value": humidity,
            },
            {
                "device": serial,
                "field": "BATTERY",
                "value": battery,
            },
            {
                "device": serial,
                "field": "PRESSURE",
                "value": pressure
            },
            {
                "device": serial,
                "field": "LIGHT",
                "value": light
            },
            {
                "device": serial,
                "field": "LTE_SECONDS",
                "value": lte_seconds
            },
            {
                "device": serial,
                "field": "LOCATION",
                "value": location,
            }
        );
    }
		
    // returning sends the data to Datacake
    return datacakeFields;
}
