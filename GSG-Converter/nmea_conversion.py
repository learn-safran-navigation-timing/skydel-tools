import pynmea2
import csv
import codecs


class NmeaFunction():

    def __init__(self, *args, **kwargs):
        self.ind = 0
        self.table_gga_elapsed = []
        self.table_gga_time = []

    def start_data(self, file_path, folder_path):

        traj_fieldnames = ['Elapsed time (ms)', 'TimeStamp', 'Latitude', 'Longitude',
                           'Antenna Alt above sea level (mean)']
        self.nmea_file = file_path
        self.traj_filename = str(folder_path) + "/" + "nmea_traj.csv"
        self.traj_file_open = open(self.traj_filename, 'a', newline='')
        self.traj_csvfile_writer = csv.DictWriter(self.traj_file_open, fieldnames=traj_fieldnames)
        self.traj_csvfile_writer.writeheader()

        self.nmea_file = codecs.open(self.nmea_file, 'r', encoding='utf-8',
                                     errors='ignore')

        try:
            for line in self.nmea_file.readlines():

                try:

                    msg = pynmea2.parse(line)

                    try:
                        if msg.sentence_type == 'GGA':
                            self.save_parsed_data(msg)
                            self.ind = self.ind + 1
                    except AttributeError as att_err_1:
                        print(att_err_1)
                        if msg.sentence_types == 'GGA':
                            self.save_parsed_data(msg)
                            self.ind = self.ind + 1

                except pynmea2.ParseError as e:
                    print('Parse error: {}'.format(e))
                    continue

                except UnicodeDecodeError as uni_err:
                    print(uni_err)
                    continue
            self.traj_file_open.close()

        except UnicodeDecodeError as uni_er:
            print(uni_er)

        return self.traj_filename

    def save_parsed_data(self, msg):
        """This function will save each NMEA message read on the NMEA file into the corrresponding csv file"""

        try:

            print(repr(msg))

            gga_timestamp = str(msg.timestamp)

            if str(gga_timestamp) == "None":
                pass
            else:
                print(self.ind)

                start_time = gga_timestamp.split(":")

                gga_hour = start_time[0]
                gga_minute = start_time[1]
                gga_s = start_time[2].split("+")
                #gga_sec = int(round(float(gga_s[0])))
                #gga_milli_sec = float(gga_s[0]) * 1000
                gga_total_millisec = ((int(gga_hour) * 60 + int(gga_minute)) * 60) * 1000 + float(gga_s[0]) * 1000

                if float(gga_total_millisec) == 0.0:
                    self.ind = 0
                    pass
                else:
                    self.table_gga_elapsed.append(gga_total_millisec)
                    self.table_gga_time.append(gga_timestamp)

                    self.elapsed_gga = gga_total_millisec - self.table_gga_elapsed[0]

                    gga_lat = msg.latitude

                    gga_lon = msg.longitude

                    gga_altitude = msg.altitude

                    self.traj_csvfile_writer.writerow(
                        {'Elapsed time (ms)': self.elapsed_gga, 'TimeStamp': gga_timestamp, 'Latitude': gga_lat,
                         'Longitude': gga_lon,
                         'Antenna Alt above sea level (mean)': gga_altitude})

        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))

        except KeyError as err:
            print(err)
            pass

        except AttributeError as att_err:
            print(att_err)
            pass
