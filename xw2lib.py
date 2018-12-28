

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
    
    print(packet)
    
    ch_offset = 3
    
    try:
        satellite_name = callsign_lookup(packet[0])
    except:
        satellite_name = "Invalid Callsign"
    
    frame_mark = frame_lookup(packet[ch_offset+1])
    
    sat_mode = op_mode(packet[ch_offset+2])
    
    supply_v = supply_voltage_convert(packet[ch_offset+3])
    
    supply_i = supply_current_convert(packet[ch_offset+4])
    
    dcdc_out_v = dcdc_out_v_convert(packet[ch_offset+5]) 
    
    dcdc_out_i = dcdc_out_i_convert(packet[ch_offset+6])
    
    obc_v = obc_v_convert(packet[ch_offset+7])
    
    try:
        obc_temp = obc_temp_convert(packet[ch_offset+8])
    except:
        obc_temp = "Unknown"
    
    try:
        pa_temp = pa_temp_convert(packet[ch_offset+9])
    except:
        pa_temp = "Unknown"
        
    try:
        rx_agc = rx_agc_convert(packet[ch_offset+10])
    except:
        rx_agc = "Unknown"
        
    try:
        rf_pwr_fwd = rf_pwr_fwd_convert(packet[ch_offset+11])
    except:
        rf_pwr_fwd = "Unknown"
        
    try:
        rf_pwr_rev = rf_pwr_rev_convert(packet[ch_offset+12])
    except:
        rf_pwr_rev = "Unknown"
        
    cpu_info = cpu_info_convert(packet[ch_offset+13:ch_offset+23])
    
    print(satellite_name)
    print(frame_mark)
    print(sat_mode)
    print(supply_v)
    print(supply_i)
    print(dcdc_out_v)
    print(dcdc_out_i)
    print(obc_v)
    print(obc_temp)
    print(pa_temp)
    print(rx_agc)
    print(rf_pwr_fwd)
    print(rf_pwr_rev)
    print(cpu_info)
    
    
def cpu_info_convert(packet):
    print(packet)
    print(len(packet))
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
        
    output = [cpu_reset_ctr, cmd_tx_ctr, crc_result, ins1, ins2, tlm_frames_rx, tlm_frames_tx, ins3, ins4, obc_op_mode, 
              write_flash_success, i2c_watchdog_enable, i2c_recon_ctr, tc_sw_watchdog_switch, tc_sw_watchdog_reset_no, 
              adc_sw_reset_switch, adc_sw_reset_no, spi_watchdog_switch, spi_meas_watchdog_no, flash_config_successful, 
              tlm_packet_ctr, sat_no, software_version, tlm_tx_rate, check_flag]
        
    return output

def get_word(packet, w):
    p = packet[w*8:w*8+8]
    return p
    
def rf_pwr_rev_convert(packet):
    N = float(packet)/10
    return "%.1fmW" % N  
    
def rf_pwr_fwd_convert(packet):
    N = int(packet)
    return "%imW" % N
    
def rx_agc_convert(packet):
    N = float(packet)
    val = N*1.3/100
    return "%.2fV" % val
    
def pa_temp_convert(packet):
    N = int(packet[1:2])
    sgn = int(packet[0])
    val = -1 * sgn + N
    return "%idegC" % val
    
def obc_v_convert(packet):
    N = float(packet)
    val = (N*2 / 100)
    return "%.2fV" % val

def obc_temp_convert(packet):
    N = int(packet[1:2])
    sgn = int(packet[0])
    val = -1 * sgn + (N - 64)
    return "%idegC" % val

def dcdc_out_i_convert(packet):
    N = int(packet)
    val = (N + 256)
    return "%imA" % val
    
def dcdc_out_v_convert(packet):
    N = float(packet)
    val = (N + 256)/ 100
    return "%.2fV" % val
    
def supply_voltage_convert(packet):
    supply_v = float(packet)/10
    return "%.1fV" % supply_v

def supply_current_convert(packet):
    supply_i = int(packet)
    return "%imA" % supply_i

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
