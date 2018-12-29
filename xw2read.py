import xw2lib

input_data = xw2lib.open_text_file("beep")

input_data = xw2lib.sanitise_string(input_data)

valid_packet_locations = xw2lib.find_packets(input_data)
print(xw2lib.get_titles())
no_packets = len(valid_packet_locations)
print("Number of packets found: %i\n" % no_packets)


pkt_no = 1
for packet_location in valid_packet_locations:
    packet = xw2lib.extract_packet(input_data, packet_location)
    packet_converted = xw2lib.convert_packet(packet)
    packet_converted_list = xw2lib.split_packet(packet_converted)
    
    decoded_packet = xw2lib.decode_packet(packet_converted_list)
    
    #print(decoded_packet)
    
    xw2lib.print_packet(decoded_packet, pkt_no, no_packets)
    pkt_no = pkt_no + 1
    
    

