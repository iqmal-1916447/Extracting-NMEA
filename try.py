# try to parse GPS NMEA data file
nmea_data = "GPS200525.nmea"

def read_NMEA():
    # Read the NMEA data file
    infile = open(nmea_data, 'r')

    # Storing longitude, latitude and altitude
    latitude = []
    longitude = []
    altitude = []

    # Read NMEA line by line
    try:
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

                    # print(f"Latitude: {latitude:.6f}; Longitude: {longitude:.6f}")

            # Get Altitude from GGA message
            if dataGPS[0] == "$GPGGA":
                if dataGPS[6] != "0":   # Valid position fix
                    if dataGPS[6] == "1":
                        print("GPS fix (SPS)")
                    elif dataGPS[6] == "2":
                        print("DGPS fix")
                    elif dataGPS[6] == "3":
                        print("PPS fix")

                    altitude = dataGPS[9]
                    # print (f"Altitude: {altitude}\n\n")

            print(f"Latitude: {latitude:.6f}; Longitude: {longitude:.6f}; Altitude: {altitude}") 








    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Run the function
    read_NMEA()
