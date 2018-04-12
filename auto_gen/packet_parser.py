# ------------------------------------------------------------------------------
# File          : packet_parser.py
# Description   : parsing the packet definition file
# Author        : Ke Xu
# History        
# 1.0 04/12/2018: initial version
# ------------------------------------------------------------------------------
import sys
import re
import xml.etree.ElementTree

elem = xml.etree.ElementTree.parse('packet_defines.xml').getroot()

for packet in elem:
    packet_name   = packet.attrib.get('name')
    packet_length = int(packet.attrib.get('length'))
    # Sanity check
    if packet_length <= 0:
        sys.exit("Error: Packet %s length is %d! Exit..." % (packet_name, packet_length))

    field_total_length = 0
    for field in packet:
        field_name          = field.attrib.get('name')
        field_position      = field.attrib.get('position')
        field_position_digit= re.findall('\d+', field_position)
        field_position_msb  = int(field_position_digit[0])
        field_position_lsb  = int(field_position_digit[1])
        field_width         = int(field.attrib.get('width'))
        field_total_length  = field_total_length + field_width 
        field_type          = field.attrib.get('type')
        # Sanity check
        # Check whether field_width is greater than 0
        if field_width <= 0:
            sys.exit("Error: Packet = %s, field = %s, width = %d! Exit..." % (packet_name, field_name, field_width)) 
        # Check whether field_position and width match
        if field_width != field_position_msb - field_position_lsb + 1:
            sys.exit("Error: Packet = %s, field = %s, position %s and width %s mismatch! Exit..." % (packet_name, field_name, field_position, str(field_width)))

    # Sanity check
    # Check whether packet length equals summed field length
    if field_total_length != packet_length:
        sys.exit("Error: packet = %s, packet length %d mismatches with summed field total length %d! Exit..." % (packet_name, packet_length, field_total_length))
    # Check whether field definition completes
    if field_position_lsb != 0:
        sys.exit("Error: packet = %s, last lsb = %d, packet definition is not complete! Exit..." % (packet_name, field_position_lsb))


