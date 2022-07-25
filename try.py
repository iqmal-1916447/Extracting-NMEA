# try to parse GPS NMEA data file
nmea_data = "GPS200526.nmea"

def read_NMEA():
    # Read the NMEA data file
    infile = open(nmea_data, 'r')

    # Array to store position & altitude
    latitude = []
    longitude = []
    altitude = []

    # Read NMEA line by line
    try:
        counter = 1     # Counting input data from sample file
        for i in infile:
            dataGPS = i.split(',')
            
            # Get minimum recommended GPS position from RMC message
            if dataGPS[0] == "$GPRMC":
                # Get position only if GPS status is valid (code: A)
                if dataGPS[2] == "A":
                    # Get NMEA latitude
                    latitude_GPS = float(dataGPS[3])
                    if dataGPS[4] == "S":   # if south, then put -ve 
                        latitude_GPS = -latitude_GPS

                    # Convert latitude coordinate ddmm.mmmm to decimal degree (dd)
                    latitude_degree = int(latitude_GPS/100)     # divide by 100 to move decimal, then truncate decimal places; so get 2 most significant digit
                    latitude_minute = latitude_GPS - latitude_degree * 100  # get the minute part
                    latitude = latitude_degree + latitude_minute / 60 

                    # Get NMEA longitude
                    longitude_GPS = float(dataGPS[5])
                    if dataGPS[6] == "W":    # if west, then put -ve
                        longitude_GPS = -longitude_GPS

                    # Convert longitude coordinate dddmm.mmmm to decimal degree (dd)
                    longitude_degree = int(longitude_GPS/100)
                    longitude_minute = longitude_GPS - longitude_degree * 100
                    longitude = longitude_degree + longitude_minute / 60 


            # Get Altitude from GGA message
            if dataGPS[0] == "$GPGGA":
                if dataGPS[6] != "0":   # Valid position fix
                    if dataGPS[6] == "1":
                        print(str(counter) + ". GPS fix (SPS)")
                    elif dataGPS[6] == "2":
                        print(str(counter) + ". DGPS fix")
                    elif dataGPS[6] == "3":
                        print(str(counter) + ". PPS fix")

                    altitude = dataGPS[9]
                    counter += 1

                    print(f"Latitude: {latitude:.6f}; Longitude: {longitude:.6f}; Altitude: {altitude}\n") 

            # Display the position & altitude in KML format (view in Google Earth)
            # Output / write to KML file
            with open("position.kml", 'w') as position:
                position.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <Placemark>
        <name>
                Rider's Location [Longitude: %s  Latitude: %s] 
        </name>
        <description>
            Real-time position via NMEA data
        </description>
        <Point>
            <coordinates>%s, %s</coordinates>
        </Point>
        </Placemark>
    </Document>
</kml>
""" %(longitude, latitude, longitude, latitude))

    except Exception as e:
        print(e)

    # Close NMEA data file
    infile.close()

if __name__ == "__main__":
    # Run the function
    read_NMEA()
