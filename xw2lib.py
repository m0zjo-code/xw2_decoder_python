from tabulate import tabulate

def open_text_file(in_file_name):
    f = open(in_file_name, "r")
    return f.read()

def sanitise_string(input_string):
    input_string = input_string.upper()
    input_string = ' '.join(input_string.split())
    input_string = input_string.strip('\n')
    return input_string

#def find_packets(input_string):
    
# From: https://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: 
            return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def find_all_occurences(a_str, sub):
    return list(find_all(a_str, sub))

def find_packets(input_string):
    call_prefix = "BJ1S"
    start_id = "XW2 XW2" #-10
    stop_id = "CAMSAT CAMSAT" #-106
    
    call_locs = find_all_occurences(input_string, call_prefix)
    
    start_locs = find_all_occurences(input_string, start_id)
    start_locs[:] = [x - 10 for x in start_locs]
    
    stop_locs = find_all_occurences(input_string, stop_id)
    stop_locs[:] = [x - 106 for x in stop_locs]
    
    valid_packets = list(set(call_locs)&set(start_locs)&set(stop_locs))
    
    return valid_packets

def extract_packet(input_string, location):
    return input_string[location:location+119]
    
def convert_packet(packet):
    packet = packet.replace("T", "0")
    packet = packet.replace("R", "1")
    packet = packet.replace("U", "2")
    packet = packet.replace("V", "3")
    packet = packet.replace("4", "4")
    packet = packet.replace("I", "5")
    packet = packet.replace("6", "6")
    packet = packet.replace("K", "7")
    packet = packet.replace("M", "8")
    packet = packet.replace("N", "9")
    return packet

def split_packet(packet):
    return packet.split(" ")

def decode_packet(packet):
    
    ch_offset = 3
    
    try:
        satellite_name = callsign_lookup(packet[0])
    except:
        satellite_name = "Invalid Callsign"
    
    try:
        frame_mark = frame_lookup(packet[ch_offset+1])
    except:
        frame_mark = ("Unknown", "Unknown", "Unknown")
    
    try:
        sat_mode = op_mode(packet[ch_offset+2])
    except:
        sat_mode = ("Unknown", "Unknown", "Unknown")
    
    try:
        supply_v = supply_voltage_convert(packet[ch_offset+3])
    except:
        supply_v = ("Unknown", "Unknown", "Unknown")
    
    try:
        supply_i = supply_current_convert(packet[ch_offset+4])
    except:
        supply_i = ("Unknown", "Unknown", "Unknown")
    
    try:
        dcdc_out_v = dcdc_out_v_convert(packet[ch_offset+5])
    except:
        dcdc_out_v = ("Unknown", "Unknown", "Unknown")
        
    try:    
        dcdc_out_i = dcdc_out_i_convert(packet[ch_offset+6])
    except:
        dcdc_out_i = ("Unknown", "Unknown", "Unknown")
    
    try:
        obc_v = obc_v_convert(packet[ch_offset+7])
    except:
        obc_v = ("Unknown", "Unknown", "Unknown")
    
    try:
        obc_temp = obc_temp_convert(packet[ch_offset+8])
    except:
        obc_temp = ("Unknown", "Unknown", "Unknown")
    
    try:
        pa_temp = pa_temp_convert(packet[ch_offset+9])
    except:
        pa_temp = ("Unknown", "Unknown", "Unknown")
        
    try:
        rx_agc = rx_agc_convert(packet[ch_offset+10])
    except:
        rx_agc = ("Unknown", "Unknown", "Unknown")
        
    try:
        rf_pwr_fwd = rf_pwr_fwd_convert(packet[ch_offset+11])
    except:
        rf_pwr_fwd = ("Unknown", "Unknown", "Unknown")
        
    try:
        rf_pwr_rev = rf_pwr_rev_convert(packet[ch_offset+12])
    except:
        rf_pwr_rev = ("Unknown", "Unknown", "Unknown")
        
    cpu_info = cpu_info_convert(packet[ch_offset+13:ch_offset+23])
    
    #print(satellite_name)
    #print(frame_mark)
    #print(sat_mode)
    #print(supply_v)
    #print(supply_i)
    #print(dcdc_out_v)
    #print(dcdc_out_i)
    #print(obc_v)
    #print(obc_temp)
    #print(pa_temp)
    #print(rx_agc)
    #print(rf_pwr_fwd)
    #print(rf_pwr_rev)
    #print(cpu_info)
    
    return (satellite_name, 
            frame_mark, 
            sat_mode, 
            supply_v, 
            supply_i, 
            dcdc_out_v, 
            dcdc_out_i, 
            obc_v, 
            obc_temp, 
            pa_temp, 
            rx_agc, 
            rf_pwr_fwd, 
            rf_pwr_rev, 
            cpu_info)
    
    
def cpu_info_convert(packet):
    #print(packet)
    #print(len(packet))
    packet = ''.join(packet)
    packet = bin(int(packet, 16))[2:].zfill(len(packet)*4)
    
    try:
        cpu_reset_ctr = int(get_word(packet, 0), 2)
    except:
        cpu_reset_ctr = -1
    
    try:
        cmd_tx_ctr = int(get_word(packet, 1)[7-7:8-5], 2)
    except:
        cmd_tx_ctr = -1
     
    try:
        crc_result = int(get_word(packet, 1)[7-4], 2)
    except:
        crc_result = -1
        
    try:
        ins1 = int(get_word(packet, 1)[7-3:8] + get_word(packet, 2), 2)
    except:
        ins1 = -1
        
    try:
        ins2 = int(get_word(packet, 3) + get_word(packet, 4)[7-7:8-4], 2)
    except:
        ins2 = -1
        
    try:
        tlm_frames_rx = int(get_word(packet, 4)[7-3:8], 2)
    except:
        tlm_frames_rx = -1
        
    try:
        tlm_frames_tx = int(get_word(packet, 5), 2)
    except:
        tlm_frames_tx = -1
        
    try:
        ins3 = int(get_word(packet, 6) + get_word(packet, 7)[7-7:8-4], 2)
    except:
        ins3 = -1
        
    try:
        ins4 = int(get_word(packet, 7)[7-3:8] + get_word(packet, 8)[7-7:8-4], 2)
    except:
        ins4 = -1
        
    try:
        obc_op_mode = int(get_word(packet, 8)[7-3:8-1], 2)
    except:
        obc_op_mode = -1   
        
    try:
        write_flash_success = int(get_word(packet, 8)[7-0], 2)
    except:
        write_flash_success = -1    
        
    try:
        i2c_watchdog_enable = int(get_word(packet, 9)[7-7], 2)
    except:
        i2c_watchdog_enable = -1   
        
    try:
        i2c_recon_ctr = int(get_word(packet, 8)[7-6:8-4], 2)
    except:
        i2c_recon_ctr = -1 
        
    try:
        tc_sw_watchdog_switch = int(get_word(packet, 9)[7-3], 2)
    except:
        tc_sw_watchdog_switch = -1 
        
    try:
        tc_sw_watchdog_reset_no = int(get_word(packet, 9)[7-2:8-0], 2)
    except:
        tc_sw_watchdog_reset_no = -1 
        
    try:
        adc_sw_reset_switch = int(get_word(packet, 10)[7-7], 2)
    except:
        adc_sw_reset_switch = -1 
        
    try:
        adc_sw_reset_no = int(get_word(packet, 10)[7-6:8-4], 2)
    except:
        adc_sw_reset_no = -1 
        
    try:
        temp_meas_watchdog_switch = int(get_word(packet, 10)[7-3], 2)
    except:
        temp_meas_watchdog_switch = -1 
        
    try:
        temp_meas_watchdog_no = int(get_word(packet, 10)[7-2:8-0], 2)
    except:
        temp_meas_watchdog_no = -1 
        
    try:
        adc_cpu_reset_switch = int(get_word(packet, 11)[7-7], 2)
    except:
        adc_cpu_reset_switch = -1 
        
    try:
        adc_cpu_reset_no = int(get_word(packet, 11)[7-6:8-4], 2)
    except:
        adc_cpu_reset_no = -1 
        
    try:
        spi_watchdog_switch = int(get_word(packet, 11)[7-3], 2)
    except:
        spi_watchdog_switch = -1 
        
    try:
        spi_meas_watchdog_no = int(get_word(packet, 11)[7-2:8-0], 2)
    except:
        spi_meas_watchdog_no = -1 
        
    try:
        flash_config_successful = int(get_word(packet, 12)[7-7], 2)
    except:
        flash_config_successful = -1
        
    try:
        tlm_packet_ctr = int(get_word(packet, 12)[7-6:8-4], 2)
    except:
        tlm_packet_ctr = -1 
        
    try:
        sat_no = int(get_word(packet, 12)[7-3:8-0], 2)
    except:
        sat_no = -1  
    
    try:
        software_version = int(get_word(packet, 13)[7-7:8-4], 2)
    except:
        software_version = -1
        
    try:
        tlm_tx_rate = int(get_word(packet, 13)[7-3], 2)
    except:
        tlm_tx_rate = -1
        
    try:
        check_flag = int(get_word(packet, 13)[7-2:8] + get_word(packet, 14), 2)
    except:
        check_flag = -1
        
    output = (cpu_reset_ctr, 
              cmd_tx_ctr, 
              crc_result, 
              ins1, 
              ins2, 
              tlm_frames_rx, 
              tlm_frames_tx, 
              ins3, 
              ins4, 
              obc_op_mode, 
              write_flash_success, 
              i2c_watchdog_enable, 
              i2c_recon_ctr, 
              tc_sw_watchdog_switch, 
              tc_sw_watchdog_reset_no, 
              adc_sw_reset_switch, 
              adc_sw_reset_no, 
              spi_watchdog_switch, 
              spi_meas_watchdog_no, 
              flash_config_successful, 
              tlm_packet_ctr, 
              sat_no, 
              software_version, 
              tlm_tx_rate, 
              check_flag)
        
    return output

def get_word(packet, w):
    p = packet[w*8:w*8+8]
    return p
    
def rf_pwr_rev_convert(packet):
    N = float(packet)/10
    return "%.1fmW" % N, N, "mW"  
    
def rf_pwr_fwd_convert(packet):
    N = int(packet)
    return "%imW" % N, N, "mW"
    
def rx_agc_convert(packet):
    N = float(packet)
    val = N*1.3/100
    return "%.2fV" % val, val, "V"
    
def pa_temp_convert(packet):
    N = int(packet[1:2])
    sgn = int(packet[0])
    val = -1 * sgn + N
    return "%idegC" % val, val, "degC"
    
def obc_v_convert(packet):
    N = float(packet)
    val = (N*2 / 100)
    return "%.2fV" % val, val, "V"

def obc_temp_convert(packet):
    N = int(packet[1:2])
    sgn = int(packet[0])
    val = -1 * sgn + (N - 64)
    return "%idegC" % val, val, "degC"

def dcdc_out_i_convert(packet):
    N = int(packet)
    val = (N + 256)
    return "%imA" % val, val, "mA"
    
def dcdc_out_v_convert(packet):
    N = float(packet)
    val = (N + 256)/ 100
    return "%.2fV" % val, val, "V"
    
def supply_voltage_convert(packet):
    supply_v = float(packet)/10
    return "%.1fV" % supply_v, supply_v, "V"

def supply_current_convert(packet):
    supply_i = int(packet)
    return "%imA" % supply_i, supply_i, "mA"

def op_mode(mode):
    return {
        "001": "Mode 1 (CW Beacon, Transmit Per 6 minutes)",
        "010": "Mode 2 (CW Beacon, Continuously)",
        "011": "Mode 3 (CW Beacon + Linear Transponder)",
        "100": "Mode 4 (CW Beacon + Telemetry)",
        "101": "Mode 5 (CW Beacon + Linear Transponder + Telemetry)",
        "110": "Mode 6 (Inter-Satellite-Link)",
        "111": "Mode 7 (Test Mode)",
    }[mode]
    
def frame_lookup(mark):
    return {
        "AAA": "Telemetry Mode",
        "BBB": "FLASH Download Succeed",
        "CCC": "FLASH Download Failure",
    }[mark]
    
def callsign_lookup(call):
    return {
        "BJ1SB": "XW-2A",
        "BJ1SC": "XW-2B",
        "BJ1SD": "XW-2C",
        "BJ1SE": "XW-2D",
        "BJ1SF": "XW-2E",
        "BJ1SG": "XW-2F",
    }[call] 

def get_table_subjects():
    main_tlm = (
        "ID (From Callsign)",
        "Data frame mark",
        "Current operating mode",
        "Primary power supply voltage",
        "Primary power supply current",
        "DC / DC converter output voltage",
        "DC / DC converter output current",
        "OBC power voltage",
        "OBC temperature",
        "RF power amplifier temperature",
        "Receiver AGC voltage",
        "RF forward power",
        "RF reflected power"
         )
    
    obc_tlm = (
        "CPU Reset Counter",
        "Command transmission counter",
        "CRC check result",
        "Instruction counter 1",
        "Instruction counter 2",
        "Telemetry frames received counter",
        "Telemetry frames transmitted counter",
        "Instruction counter 3",
        "Instruction counter 4",
        "Power on operating mode",
        "Write FLASH success flag",
        "I2C software watchdog switch flag",
        "I2C reconnecting initialized counter",
        "TC software watchdog switch flag",
        "TC software watchdog reset times counter",
        "ADC software watchdog switch flag",
        "ADC software watchdog reset times counter",
        "Temperature measurement software watchdog switch flag",
        "Temperature software watchdog reset times counter",
        "CPU ADC watchdog switch flag",
        "CPU ADC watchdog reset times counter",
        "SPI software watchdog switch flag",
        "SPI reconnecting initialized counter",
        "FLASH successfully configured flag",
        "Telemetry data packet counter",
        "Satellite Number",
        "Software version number",
        "Telemetry transmission rate flag",
        "Check flag"
        )
    return (main_tlm, obc_tlm)
        
        

def generate_packet_string(decoded_packet):
    titles = get_table_subjects()
    
    #print(decoded_packet)
    
    print_string_main = tabulate([
        [titles[0][0], decoded_packet[0]],
        [titles[0][1], decoded_packet[1]],
        [titles[0][2], decoded_packet[2]],
        [titles[0][3], decoded_packet[3][0]],
        [titles[0][4], decoded_packet[4][0]],
        [titles[0][5], decoded_packet[5][0]],
        [titles[0][6], decoded_packet[6][0]],
        [titles[0][7], decoded_packet[7][0]],
        [titles[0][8], decoded_packet[8][0]],
        [titles[0][9], decoded_packet[9][0]],
        [titles[0][10], decoded_packet[10][0]],
        [titles[0][11], decoded_packet[11][0]],
        [titles[0][12], decoded_packet[12][0]],
        ], headers=['Parameter', 'Value'], tablefmt="presto")
    
    obc_data = decoded_packet[13]
    
    #print(len(obc_data))
    
    obc_vals = []
    for i in range(0, 25):
        obc_vals.append([titles[1][i], obc_data[i]])
        
    print_string_obc = tabulate(obc_vals, headers=['Parameter', 'Value'], tablefmt="presto")
    
    return print_string_main, print_string_obc

def print_packet(decoded_packet, pkt_no, no_packets):
    
    print_string, print_string_obc = generate_packet_string(decoded_packet)
    
    print("Packet %i/%i" % (pkt_no, no_packets))
    
    print("+-- Satellite Parameters:\n")
    print(print_string)
    print("\n")
    print("+-- OBC Parameters:\n")
    print(print_string_obc)
    
def get_titles():
    intro = """
+-----------------------------------------+
|                                         |
|      xw2read - A simple XW-2            |
|             CW telemetry decoder        |
|                                         |
|      Jonathan Rawlinson/M0ZJO 2018      |
|                                         |
|               MIT Licence               |
|                                         |
+-----------------------------------------+

"""
    return intro
    
