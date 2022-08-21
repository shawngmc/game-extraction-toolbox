'''
Reader for Apple Binary PList

### shawngmc NOTE ###
Pulled from https://github.com/ValadAmoleo/sf30ac-extractor/blob/mame/bplist.py
Altered to:
* Be much more pythonic/linted/etc.

#### WydD NOTE ####
Original project https://github.com/farcaller/bplist-python
This has been altered to
* Be Py3k compatible
* Support the specific tail format of the sf30ac files

#################################################################################
# Copyright (C) 2009-2011 Vladimir "Farcaller" Pouzanov <farcaller@gmail.com>   #
#                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining a copy  #
# of this software and associated documentation files (the "Software"), to deal #
# in the Software without restriction, including without limitation the rights  #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
# copies of the Software, and to permit persons to whom the Software is         #
# furnished to do so, subject to the following conditions:                      #
#                                                                               #
# The above copyright notice and this permission notice shall be included in    #
# all copies or substantial portions of the Software.                           #
#                                                                               #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN     #
# THE SOFTWARE.                                                                 #
#################################################################################
'''

import struct
from datetime import datetime, timedelta
import plistlib

class BPListReader(object):
    '''Reader for Apple Binary PList'''
    def __init__(self, in_data):
        self.data = in_data
        self.objects = []
        self.resolved = {}
        self.offset_size = None
        self.object_ref_size = None
        self.number_of_objects = None
        self.top_object = None
        self.table_offset = None
        self.top_object = None
        self.offset_table = None
        self.offsets = None

    def __unpack_int_struct(self, size, in_data):
        '''__unpack_int_struct(size, string) -> int

        Unpacks the integer of given size (1, 2 or 4 bytes) from string
        '''
        if size == 1:
            int_format = '!B'
        elif size == 2:
            int_format = '!H'
        elif size == 4:
            int_format = '!I'
        elif size == 8:
            int_format = '!Q'
        else:
            raise Exception('int unpack size '+str(size)+' unsupported')
        return struct.unpack(int_format, in_data)[0]

    def __unpack_int(self, offset):
        '''__unpack_int(offset) -> int

        Unpacks int field from plist at given offset
        '''
        return self.__unpack_int_meta(offset)[1]

    def __unpack_int_meta(self, offset):
        '''__unpack_int_meta(offset) -> (size, int)

        Unpacks int field from plist at given offset and returns its size and value
        '''
        obj_header = struct.unpack('!B', self.data[offset:offset+1])[0]
        _, obj_info = (obj_header & 0xF0), (obj_header & 0x0F)
        int_sz = 2**obj_info
        return int_sz, self.__unpack_int_struct(int_sz, self.data[offset+1:offset+1+int_sz])

    def __resolve_int_size(self, obj_info, offset):
        '''__resolve_int_size(obj_info, offset) -> (count, offset)

        Calculates count of objref* array entries and returns count and offset to first element
        '''
        if obj_info == 0x0F:
            ofs, obj_count = self.__unpack_int_meta(offset+1)
            objref = offset+2+ofs
        else:
            obj_count = obj_info
            objref = offset+1
        return obj_count, objref

    def __unpack_float_struct(self, size, in_data):
        '''__unpack_float_struct(size, string) -> float

        Unpacks the float of given size (4 or 8 bytes) from string
        '''
        if size == 4:
            float_format = '!f'
        elif size == 8:
            float_format = '!d'
        else:
            raise Exception('float unpack size '+str(size)+' unsupported')
        return struct.unpack(float_format, in_data)[0]

    def __unpack_float(self, offset):
        '''__unpack_float(offset) -> float

        Unpacks float field from plist at given offset
        '''
        obj_header = struct.unpack('!B', self.data[offset])[0]
        _, obj_info = (obj_header & 0xF0), (obj_header & 0x0F)
        int_sz = 2**obj_info
        return int_sz, self.__unpack_float_struct(int_sz, self.data[offset+1:offset+1+int_sz])

    def __unpack_date(self, offset):
        stored_time_delta = int(struct.unpack(">d", self.data[offset+1:offset+9])[0])
        return datetime(year=2001,month=1,day=1) + timedelta(seconds=stored_time_delta)

    def __unpack_item(self, offset):
        '''__unpack_item(offset)

        Unpacks and returns an item from plist
        '''
        obj_header = struct.unpack('!B', self.data[offset:offset+1])[0]
        obj_type, obj_info = (obj_header & 0xF0), (obj_header & 0x0F)
        if   obj_type == 0x00:
            if   obj_info == 0x00:
                # null   0000 0000
                return None
            elif obj_info == 0x08:
                # bool   0000 1000           // false
                return False
            elif obj_info == 0x09:
                # bool   0000 1001           // true
                return True
            elif obj_info == 0x0F:
                # fill   0000 1111           // fill byte
                raise Exception("0x0F Not Implemented") # this is really pad byte, FIXME
            else:
                raise Exception('unpack item type '+str(obj_header)+' at '+str(offset)+ 'failed')
        elif obj_type == 0x10:
            #     int    0001 nnnn   ...
            # # of bytes is 2^nnnn, big-endian bytes
            return self.__unpack_int(offset)
        elif obj_type == 0x20:
            #    real    0010 nnnn   ...
            # # of bytes is 2^nnnn, big-endian bytes
            return self.__unpack_float(offset)
        elif obj_type == 0x30:
            #    date    0011 0011   ...
            # 8 byte float follows, big-endian bytes
            return self.__unpack_date(offset)
        elif obj_type == 0x40:
            #    data    0100 nnnn   [int]   ...
            # nnnn is number of bytes unless 1111 then int count follows, followed by bytes
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            return self.data[objref:objref+obj_count] # we return data as str
        elif obj_type == 0x50:
            #    string  0101 nnnn   [int]   ...
            # ASCII string, nnnn is # of chars, else 1111
            # then int count, then bytes
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            return self.data[objref:objref+obj_count].decode('ascii')
        elif obj_type == 0x60:
            #    string  0110 nnnn   [int]   ...
            # Unicode string, nnnn is # of chars, else 1111
            # then int count, then big-endian 2-byte uint16_t
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            return self.data[objref:objref+obj_count*2].decode('utf-16be')
        elif obj_type == 0x80:
            #    uid     1000 nnnn   ...     // nnnn+1 is # of bytes
            # FIXME: Accept as a string for now
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            return self.data[objref:objref+obj_count]
        elif obj_type == 0xA0:
            #    array   1010 nnnn   [int]   objref*
            # nnnn is count, unless '1111', then int count follows
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            arr = []
            for i in range(obj_count):
                arr.append(
                    self.__unpack_int_struct(
                        self.object_ref_size,
                        self.data[objref + i * self.object_ref_size:
                            objref + i * self.object_ref_size + self.object_ref_size]
                    )
                )
            return arr
        elif obj_type == 0xC0:
            #   set      1100 nnnn   [int]   objref*
            # nnnn is count, unless '1111', then int count follows
            # not serializable via apple implementation
            raise Exception("0xC0 Not Implemented") # FIXME: implement
        elif obj_type == 0xD0:
            #   dict     1101 nnnn   [int]   keyref* objref*
            # nnnn is count, unless '1111', then int count follows
            obj_count, objref = self.__resolve_int_size(obj_info, offset)
            keys = []
            for i in range(obj_count):
                keys.append(
                    self.__unpack_int_struct(
                        self.object_ref_size,
                        self.data[objref + i * self.object_ref_size:
                            objref + i * self.object_ref_size +self.object_ref_size]
                    )
                )
            values = []
            objref += obj_count*self.object_ref_size
            for i in range(obj_count):
                values.append(
                    self.__unpack_int_struct(
                        self.object_ref_size,
                        self.data[objref + i * self.object_ref_size:
                            objref + i * self.object_ref_size + self.object_ref_size]
                    )
                )
            dic = {}
            for i in range(obj_count):
                dic[keys[i]] = values[i]
            return dic
        else:
            raise Exception('don\'t know how to unpack obj type '+hex(obj_type)+' at '+str(offset))

    def __resolve_object(self, idx):
        try:
            return self.resolved[idx]
        except KeyError:
            obj = self.objects[idx]
            if isinstance(obj, list):
                new_array = []
                for i in obj:
                    new_array.append(self.__resolve_object(i))
                self.resolved[idx] = new_array
                return new_array
            if isinstance(obj, dict):
                new_dict = {}
                for key, value in obj.items():
                    resolved_key = self.__resolve_object(key)
                    resolved_value = self.__resolve_object(value)
                    new_dict[resolved_key] = resolved_value
                self.resolved[idx] = new_dict
                return new_dict
            else:
                self.resolved[idx] = obj
                return obj

    def parse(self):
        '''Parse the BPList'''
        # read header
        if self.data[:5] == b'<?xml':
            # load XML formated data and convert it
            plist_elements = {'bundles': {}}
            for bundle in plistlib.loads(self.data)['bundles']:
                plist_elements['bundles'].update({bundle['bundleName']: {'files': bundle['files']}})
            return plist_elements
        elif self.data[:8] != b'bplist00':
            raise Exception('Bad magic')

        # read trailer
        offset_size, object_ref_size, num_objects, top_obj, table_offset = struct.unpack(
            '!BB4xI4xI4xI', self.data[-26:]
        )
        self.offset_size = offset_size
        self.object_ref_size = object_ref_size
        self.number_of_objects = num_objects
        self.top_object = top_obj
        self.table_offset = table_offset
        self.top_object = self.table_offset - 8

        # read offset table
        self.offset_table = self.data[self.table_offset:-26]
        self.offsets = []
        offset_table = self.offset_table
        for i in range(self.number_of_objects):
            offset_entry = offset_table[:self.offset_size]
            offset_table = offset_table[self.offset_size:]
            self.offsets.append(self.__unpack_int_struct(self.offset_size, offset_entry))
        #print("** plist offsets: %s" % (self.offsets))

        # read object table
        self.objects = []
        k = 0
        for i in self.offsets:
            obj = self.__unpack_item(i)
            #print("** plist unpacked %d %s %s at %d" % (k, type(obj), obj, i))
            k += 1
            self.objects.append(obj)

        # rebuild object tree
        #for i in range(len(self.objects)):
        #    self.__resolveObject(i)

        # return root object
        return self.__resolve_object(self.number_of_objects-1)
