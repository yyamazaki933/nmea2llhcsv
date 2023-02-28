#!/usr/bin/env python3
import rosbag

bag_filename = '/media/yudai/ssd/20230222_lv3_proto/map/corrected.bag'
nmea_topic = '/ins/nmea_sentence'
csv_filename = bag_filename.replace('.bag', '.csv')


def writeCSV(bag_filename: str, csv_filename: str):
    with open(csv_filename, mode='w') as f:
        header = 'stamp,latitude,longitude,altitude'
        f.write(header + '\n')
        bag = rosbag.Bag(bag_filename)

        for topic, msg, t in bag.read_messages():
            if topic == nmea_topic:
                t = msg.header.stamp.to_sec()
                s = msg.sentence.split(',')

                if s[0] == "$GPGGA":
                    lat_deg = int(float(s[2])/100.0)
                    lat_min = (float(s[2]) - (lat_deg*100))/60.0
                    lon_deg = int(float(s[4])/100.0)
                    lon_min = (float(s[4]) - (lon_deg*100))/60.0
                    lat = lat_deg + lat_min
                    lon = lon_deg + lon_min
                    geoid = float(s[11])

                    row = str(t) + ',' + str(lat) + ',' + \
                        str(lon) + ',' + str(geoid)
                    f.write(row + '\n')
                    print(row)


if __name__ == '__main__':
    writeCSV(bag_filename, csv_filename)
