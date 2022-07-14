# Import
import csv
import os
import shutil
import pandas as pd
import re

class RinexReader:

    def __init__(self):
        self.path = "tmp"

    def find_header(self, filename):
        header = ''
        headers_infos = []
        j = 0
        rinex_detection = 0
        if filename:
            with open(filename) as handler:
                for i, line in enumerate(handler):

                    header += line
                    headers_infos.append(line)

                    j += 1

                    if 'GLO' in line:
                        rinex_detection = rinex_detection + 1

                    if 'RINEX VERSION' in line:
                        rinex_detection = rinex_detection + 1

                    if 'END OF HEADER' in line:
                        rinex_detection = rinex_detection + 1
                        break

            return j, rinex_detection, headers_infos

    def readRinex(self, fileName, lineSkip):

        self.path = "tmp"
        try:
            os.mkdir(self.path)
        except OSError:
            print("Creation of the directory %s failed" % self.path)
        else:
            print("Successfully created the directory %s " % self.path)

        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        with open(fileName) as f:
            for i, l in enumerate(f):
                pass
        length = i + 1
        length_skipline = i + 1 - lineSkip

        with open(fileName, 'r') as f:
            lines = f.readlines()
            new_lines = lines[lineSkip:length]

        return new_lines, length_skipline

    def readline(self, new_lines, length_skipline):

        csv_list = []

        df = pd.DataFrame()

        for j in range(0, length_skipline, 4):

            sv_infos = new_lines[j: j + 4]

            if "R" in sv_infos[0]:
                str_sv = str(sv_infos[0])
                sv_name = str_sv[:3]
                sv_name = sv_name.replace(" ", "")
                sv_name = re.split('(\d+)', sv_name)
                sv_name = sv_name[1]

                sv_date = str(sv_infos[0])
                sv_date = sv_date[3:]

            else:
                str_sv = str(sv_infos[0])
                sv_name = str_sv[:3]
                sv_name = sv_name.replace(" ", "")

                sv_date = str(sv_infos[0])
                sv_date = sv_date[3:]

            sv_date = sv_date.replace('e', 'E')
            sv_date = sv_date.replace('D', 'E')
            sv_date = sv_date.replace('E-', 'Eneg').replace('-', ' -').split()
            sv_date = [item.replace('Eneg', 'E-') for item in sv_date]

            sv_year = sv_date[0]
            sv_month = sv_date[1]
            sv_day = sv_date[2]
            sv_hour = sv_date[3]
            sv_minutes = sv_date[4]
            sv_secondes = sv_date[5]
            sv_clock_bias = sv_date[6]
            sv_freq_draft = sv_date[7]
            sv_frame_time = sv_date[8]

            csv_name = self.path + "\\" + str(sv_name) + ".csv"

            sv_x = sv_infos[1]
            sv_x = sv_x.replace('e', 'E')
            sv_x = sv_x.replace('D', 'E')

            sv_x = sv_x.replace('E-', 'Eneg').replace('-', ' -').split()
            sv_x = [item.replace('Eneg', 'E-') for item in sv_x]

            sv_x_position = sv_x[0]
            sv_x_velocity = sv_x[1]
            sv_x_acceleration = sv_x[2]
            sv_x_health = sv_x[3]

            sv_y = sv_infos[2]
            sv_y = sv_y.replace('e', 'E')
            sv_y = sv_y.replace('D', 'E')

            sv_y = sv_y.replace('E-', 'Eneg').replace('-', ' -').split()
            sv_y = [item.replace('Eneg', 'E-') for item in sv_y]

            sv_y_position = sv_y[0]
            sv_y_velocity = sv_y[1]
            sv_y_acceleration = sv_y[2]
            sv_y_health = sv_y[3]

            sv_z = sv_infos[3]
            sv_z = sv_z.replace('e', 'E')
            sv_z = sv_z.replace('D', 'E')
            sv_z = sv_z.replace('E-', 'Eneg').replace('-', ' -').split()
            sv_z = [item.replace('Eneg', 'E-') for item in sv_z]

            sv_z_position = sv_z[0]
            sv_z_velocity = sv_z[1]
            sv_z_acceleration = sv_z[2]
            sv_z_health = sv_z[3]

            """sat_data = {"name:", sv_name, "X position:", sv_x_position, "X velocity:", sv_x_velocity,
                        " X acceleration:",
                        sv_x_acceleration, "Y position:", sv_y_position, "Y velocity:", sv_y_velocity,
                        "Y acceleration:",
                        sv_y_acceleration, "Z position:", sv_z_position, "Z velocity:", sv_z_velocity,
                        "Z acceleration:",
                        sv_z_acceleration}"""

            sv_x_position = sv_x_position.replace("D", "e")
            sv_y_position = sv_y_position.replace("D", "e")
            sv_z_position = sv_z_position.replace("D", "e")

            sv_x_velocity = sv_x_velocity.replace("D", "e")
            sv_y_velocity = sv_y_velocity.replace("D", "e")
            sv_z_velocity = sv_z_velocity.replace("D", "e")

            sv_x_acceleration = sv_x_acceleration.replace("D", "e")
            sv_y_acceleration = sv_y_acceleration.replace("D", "e")
            sv_z_acceleration = sv_z_acceleration.replace("D", "e")

            dff = pd.DataFrame([[sv_name, sv_hour, sv_minutes, sv_secondes, sv_x_position]],
                               columns=['Sat_ID', 'hour', 'min', 'sec', 'x'])
            # Tack it on the end
            df = df.append(dff)

            totalsec = int(sv_hour) * 3600 + int(sv_minutes) * 60 + int(float(sv_secondes))
            fieldnames = ['Sat_ID', 'year', 'month', 'day', 'hour', 'min', 'sec', 'totalsec', 'bias', 'freq', 'frame',
                          'x', 'y', 'z', 'vx', 'vy', 'vz', 'ax', 'ay', 'az', 'health', 'freq_num', 'age']


            if csv_name not in csv_list:
                csv_list.append(csv_name)
                with open(csv_name, 'a+', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        'Sat_ID': sv_name, 'year': sv_year, 'month': sv_month, 'day': sv_day, 'hour': sv_hour,
                        'min': sv_minutes, 'sec': sv_secondes, 'totalsec': totalsec,
                        'bias': float(sv_clock_bias), 'freq': float(sv_freq_draft), 'frame': float(sv_frame_time),
                        'x': float(sv_x_position), 'y': float(sv_y_position), 'z': float(sv_z_position),
                        'vx': float(sv_x_velocity), 'vy': float(sv_y_velocity), 'vz': float(sv_z_velocity),
                        'ax': float(sv_x_acceleration), 'ay': float(sv_y_acceleration), 'az': float(sv_z_acceleration),
                        'health': float(sv_x_health), 'freq_num': float(sv_y_health), 'age': float(sv_z_health)})
            else:

                with open(csv_name, 'a+', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow({
                        'Sat_ID': sv_name, 'year': sv_year, 'month': sv_month, 'day': sv_day, 'hour': sv_hour,
                        'min': sv_minutes, 'sec': sv_secondes, 'totalsec': totalsec,
                        'bias': float(sv_clock_bias), 'freq': float(sv_freq_draft), 'frame': float(sv_frame_time),
                        'x': float(sv_x_position), 'y': float(sv_y_position), 'z': float(sv_z_position),
                        'vx': float(sv_x_velocity), 'vy': float(sv_y_velocity), 'vz': float(sv_z_velocity),
                        'ax': float(sv_x_acceleration), 'ay': float(sv_y_acceleration), 'az': float(sv_z_acceleration),
                        'health': float(sv_x_health), 'freq_num': float(sv_y_health), 'age': float(sv_z_health)})