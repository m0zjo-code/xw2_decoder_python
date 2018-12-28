import xw2lib

input_data = xw2lib.open_text_file("beep")

input_data = xw2lib.sanitise_string(input_data)

valid_packet_locations = xw2lib.find_packets(input_data)
print("Number of packets found: %i" % len(valid_packet_locations))

for packet_location in valid_packet_locations:
    packet = xw2lib.extract_packet(input_data, packet_location)
    packet_converted = xw2lib.convert_packet(packet)
    packet_converted_list = xw2lib.split_packet(packet_converted)
    
    xw2lib.decode_packet(packet_converted_list)
    

