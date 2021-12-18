import pprint

import sys
sys.path.append('..')

import lib.text

class BITSPacketDecoder(object):
    def __init__(self, packet):
        self.packet = packet
        self.bits = self.hex2bin(self.packet)
        self.bit_labels = '' 
        self.index = 0

    def hex2bin(self, hex_string):
        ret = ''
        for c in hex_string:
            ret += bin(int(c, 16))[2:].rjust(4, '0') 

        return ret

    def bits_left(self):
        ret = len(self.bits) - self.index
        return ret

    def read(self, read_len, bit_label):
        if self.bits_left() < read_len:
            print("read underrun")
            return None

        ret = self.bits[self.index:self.index+read_len]

        preview_width = 60
        skip = max(self.index - preview_width, 0)

        print(self.bits[skip:skip+preview_width*2])
        print(self.bit_labels[skip:] + lib.text.bcolor('green', bit_label * read_len) + " -> %s (dec %s)" % (ret, str(int(ret, 2))))
        print()

        self.bit_labels += bit_label * read_len

        self.index += read_len

        return ret

    def read_packet(self):
        version = int(self.read(3, 'V'), 2)
        type_id = int(self.read(3, 'T'), 2)
        
        print('version: %s type_id: %s' % (version, type_id))

        if type_id == 4:
            ret = self.parse_payload_4(version, type_id)
        else:
            ret = self.parse_payload_op(version, type_id)

        return ret

    def parse_payload_4(self, version, type_id):
        bit_string = ""
        more = 1
        while more:
            more = int(self.read(1, 'n'))
            bit_string += self.read(4, 'N')

        return {'version': version, 'type_id': type_id, 'literal': int(bit_string, 2)}

    def parse_payload_op(self, version, type_id):
        subpackets = []

        length_type_id = int(self.read(1, 'I'))

        subpacket_length = None
        subpacket_count = None

        if length_type_id == 0:
            subpacket_length = int(self.read(15, 'L'), 2)
            bit_stop = self.index + subpacket_length
        elif length_type_id == 1:
            subpacket_count = int(self.read(11, 'C'), 2)

        packet_count = 0
        while (
                (subpacket_count and packet_count < subpacket_count)
                or
                (subpacket_length and self.index < bit_stop)
            ) and self.bits_left() >= 11:

            subpacket = self.read_packet()
            packet_count += 1
            if subpacket:
                subpackets.append(subpacket)
            else:
                raise ValueError('no subpacket when expecting subpacket')

        return {'version': version, 'type_id': type_id, 'subpackets': subpackets}

class BITS(object):
    def __init__(self):
        self.transmissions = []

    def load_data(self, data):
        for line in data:
            self.transmissions.append(line)

    def get_version_sum(self, packet):
        version_sum = packet.get('version') 

        if 'subpackets' in packet:
            for subpacket in packet['subpackets']:
                version_sum += self.get_version_sum(subpacket)

        return version_sum

    def evaluate_packet(self, packet, depth=0):
        type_id = packet['type_id']

        if type_id == 4 and 'subpackets' in packet:
            raise ValueError('WTF')

        if type_id == 4:
            return packet['literal']

        if 'subpackets' in packet:
            values = []
            for subpacket in packet['subpackets']:
                values.append(self.evaluate_packet(subpacket, depth+1))

            print((' ' * depth) + str(depth) + ' eval %s of %s' % (type_id, values))
            
            if type_id == 0:
                ret = sum(values)
                print("sum %s = %s" % (values, ret))
                return ret 
            elif type_id == 1:
                product = 1
                for v in values:
                    product *= v
                print("product %s = %s" % (values, product))
                return product
            elif type_id == 2:
                ret = min(values)
                print("min %s = %s" % (values, ret))
                return ret 
            elif type_id == 3:
                ret = max(values)
                print("max %s = %s" % (values, ret))
                return ret 
            elif type_id == 4:
                raise ValueError("WTF srsly")
            elif type_id == 5:
                ret = 1 if values[0] > values[1] else 0
                print("%s gt %s = %s" % (values[0], values[1], ret))
                return ret
            elif type_id == 6:
                ret = 1 if values[0] < values[1] else 0
                print("%s lt %s = %s" % (values[0], values[1], ret))
                return ret
            elif type_id == 7:
                ret = 1 if values[0] == values[1] else 0
                print("%s eq %s = %s" % (values[0], values[1], ret))
                return ret 
            else:
                raise ValueError('Unknown type_id %s' % type_id)

        print('mystery packet')
        pprint.pprint(packet)
        raise ValueError('WTF')

    def parse_packets(self, transmissions):
        ret = {} 
        for transmission in transmissions:
            print(transmission)

            bd = BITSPacketDecoder(transmission)

            parsed_transmission = bd.read_packet()
            print(parsed_transmission)

            if bd.bits_left():
                leftovers = bd.read(bd.bits_left(), 'x')
                if int(leftovers):
                    raise ValueError("Left bits on the table: %s" % leftovers) 

            ret.update({transmission: parsed_transmission})

        return ret 

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    bits = BITS()
    bits.load_data(data) 
    parsed_transmissions = bits.parse_packets(data)

    for transmission, parsed_transmission in parsed_transmissions.items():
        version_sum = bits.get_version_sum(parsed_transmission)
        print('version_sum', version_sum)

def solution_part_2(data):
    bits = BITS()
    bits.load_data(data) 
    parsed_transmissions = bits.parse_packets(data)
    for transmission, parsed_transmission in parsed_transmissions.items():
        print(transmission)
        result = bits.evaluate_packet(parsed_transmission)
        print('eval results', result)

if __name__ == '__main__':
    #solution_part_1(get_test_data())
    #solution_part_1(get_data())

    #solution_part_2(get_test_data())
    solution_part_2(get_data())
