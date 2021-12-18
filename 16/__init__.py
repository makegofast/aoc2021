class BITSPacketDecoder(object):
    def __init__(self, packet):
        self.packet = packet
        self.bits = self.hex2bin(self.packet)
        self.index = 0

    def hex2bin(self, hex_string):
        ret = ''
        for c in hex_string:
            ret += bin(int(c, 16))[2:].rjust(4, '0') 

        return ret

    def bits_left(self):
        ret = len(self.bits) - self.index
        return ret

    def read(self, read_len):
        if self.bits_left() < read_len:
            print("read underrun")
            return None

        ret = self.bits[self.index:self.index+read_len]

        #print(self.bits)
        #print(' ' * self.index + '*' * read_len + ' = ' + ret + ' (' + str(int(ret, 2)) + ')')
        #print()

        self.index += read_len

        return ret

    def read_packet(self):
        version = int(self.read(3), 2)
        type_id = int(self.read(3), 2)
        
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
            more = int(self.read(1))
            bit_string += self.read(4)

        return {'version': version, 'type_id': type_id, 'literal': int(bit_string, 2)}

    def parse_payload_op(self, version, type_id):
        subpackets = []

        length_type_id = int(self.read(1))

        if length_type_id == 0:
            subpacket_length = int(self.read(15), 2)
        elif length_type_id == 1:
            subpacket_count = int(self.read(11), 2)

        while self.bits_left() > 12:
            subpacket = self.read_packet()
            if subpacket:
                subpackets.append(subpacket)
            else:
                print("no subpacket?, breaking")
                break

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

    def parse_packets(self, data):
        print(data)
        bd = BITSPacketDecoder(data)
        print(bd.bits)
        print()

        packets = bd.read_packet()

        return packets

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    bits = BITS()
    bits.load_data(data) 
    packets = bits.parse_packets(data)
    version_sum = bits.get_version_sum(packets)
    print('version_sum', version_sum)

def solution_part_2(data):
    bits = BITS()
    bits.load_data(data) 
    packets = bits.parse_packets(data)
    result = bits.evaluate_packets(packets)
    print('eval results', result)

if __name__ == '__main__':
    solution_part_1(get_test_data())
    solution_part_1(get_data())

    #solution_part_2(get_test_data())
    #solution_part_2(get_data())
