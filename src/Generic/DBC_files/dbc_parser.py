import os
import re
import shutil
import sys
import traceback
from typing import List

from dbc_parser_constants import SIGNALS_ENUM_METHODS, SIGS_ENUM_CONSTRUCTOR, REGEX_EXT_SIGS_ATTS_FROM_BULK, \
    REGEX_SIGS_INIT_VAL, SIG_FILE_HEADER, ECU_NAMES_DBC, SIGNAL_ENUM_INSTANCE_VARS, REGEX_CAPTURE_MSGS_SIGS, \
    RAW_REGEX_MSG_ID_NAME_SENDING_NODE, REGEX_MSG_ID_CYCLE_TIME


class DbcParser:
    @staticmethod
    def write_sig_file(*, signals_file: str, msg_sig_map: dict,
                       signal_enum_instance_vars=SIGNAL_ENUM_INSTANCE_VARS) -> None:
        parent_package = ".".join(re.split(r'[\\/]', os.path.dirname(os.path.realpath(__file__)))[-2:])
        """
        Writes each frame in a separate file named signals_file_frame
        :param signals_file: File Name to be used (ex: PCAN_Signals.java)
        :param msg_sig_map: Msg:list of signals dictionary (used to print each msg in a separate file)
        :param signal_enum_instance_vars: Optional Arg for instance vars used by Signal enum
        """
        shutil.rmtree(signals_file.split('_')[0])
        os.makedirs(signals_file.split('_')[0])
        for msg, list_of_sig_and_attributes in msg_sig_map.items():
            if len(list_of_sig_and_attributes[0]) == 0:
                continue
            with open(signals_file.split('_')[0] + "//" + signals_file.split('.')[0] + '_' + msg + '.java', 'w') as op:
                op.write(SIG_FILE_HEADER.format(
                    pack=parent_package + "." + signals_file.split('_')[0],
                    cl=signals_file.split('.')[0] + '_' + msg,
                    base_class=re.sub(r'\d', '', signals_file.split('.')[0])[:-1],
                    parent_pack=parent_package))
                for sig_and_attributes in list_of_sig_and_attributes:
                    try:
                        op.write(
                            sig_and_attributes[0] + "(" + ','.join(
                                map(str,
                                    ["\"" + s + "\"" for s in sig_and_attributes[1:]])) + "),\n")
                    except IndexError as ex:
                        print("".join(traceback.TracebackException.from_exception(ex).format()))
                        exit(1)
                op.write(signal_enum_instance_vars)
                op.write(SIGS_ENUM_CONSTRUCTOR.format(
                    cl=signals_file.split('.')[0] + '_' + msg) + SIGNALS_ENUM_METHODS + "\n}")

    @staticmethod
    def parse_dbc(*, dbc_file_path: str, signals_file: str,
                  raw_regex_msg_signals_map: str = REGEX_CAPTURE_MSGS_SIGS,
                  write_sig_file: bool = True, msg_id_name: dict = None, is_msg_id_hex: bool = False,
                  sig_msg_map: dict = None, sig_list=None) -> None:
        """
        Parses the dbc file passed & writes each msg / frame to its own file in a directory names as the 1st 3 chars
        of signals_file param provided.
        Method args list:
        dbc_file_path -> path to dbc file to be parsed
        signals_file -> Name of Sigs file to be written to including extension
        raw_regex_msg_signals_map -> regex used to capture  the whole frame (Msg with its sigs),
                                      Each match is then broken down using another regex Value can be
                                      overwritten as needed but keep in mind that regex assumes that empty lines
                                      are replaced by '$' to avoid catastrophic backtracking
                                      (empty lines are replaced by '$' within the method)
        write_sigs_file -> optional flag to specify if sigs file are to be written (default is True)
        msg_id_name -> optional dictionary to store msg id name mapping (used here mainly to get init val of each signal)
                        if a dict is provided the modified dict will have the msg id:name mappings.
        is_msg_id_hex -> optional bool to specify whether the msgID in the dbc  file is in Hex format. (default is False)
        """
        if sig_msg_map is None:
            sig_msg_map = dict()
        if msg_id_name is None:
            msg_id_name = dict()
        msg_sig_map, msg_sig_name_init_val = dict(), dict()
        try:
            with open(
                    dbc_file_path.strip(), 'r', encoding='unicode_escape') as f:
                file_string = re.sub(r"^$", "$", f.read(), 0, re.MULTILINE)
                matches = re.finditer(raw_regex_msg_signals_map, file_string, re.MULTILINE | re.DOTALL)
        except FileNotFoundError as ex:
            print("file {0} is not found".format(dbc_file_path), file=sys.stderr)
            print("".join(traceback.TracebackException.from_exception(ex).format()))
            exit(1)
        for msg in matches:
            msg_id_name["0x" + str(hex(int(msg.group('Msg_ID')))).upper()[-2:] if is_msg_id_hex else msg.group(
                'Msg_ID')] = msg.group('Msg_Name').strip()
            signals_attributes = re.finditer(REGEX_EXT_SIGS_ATTS_FROM_BULK, msg.group('Sigs'))
            msg_sig_map[msg.group('Msg_Name').strip()] = list()
            for sig_att in signals_attributes:
                msg_sig_map[msg.group('Msg_Name').strip()].append(
                    [sig_att.group('Sig_Name'),
                     sig_att.group('Bits'),
                     sig_att.group('Signed_unsigned'),
                     sig_att.group('Factor'), sig_att.group('Offset'),
                     sig_att.group('min'), sig_att.group('max')])
                sig_msg_map[sig_att.group('Sig_Name')] = signals_file.split(".")[0] + "_" + msg.group(
                    'Msg_Name').strip() + "." + sig_att.group('Sig_Name')
                if sig_list is not None:
                    sig_list.add(
                        signals_file.split('.')[0] + '_' + msg.group('Msg_Name') + '.' + sig_att.group('Sig_Name'))
        matches = re.finditer(REGEX_SIGS_INIT_VAL, file_string)
        for match in matches:
            msg_sig_name_init_val[msg_id_name[match.group('Msg_ID')] + "_" + match.group('Sig_Name')] = \
                match.group('InitVal')
        for msg in msg_sig_map:
            for sig in msg_sig_map[msg]:
                sig.append(msg_sig_name_init_val.get(msg + "_" + sig[0], '0'))
        if write_sig_file:
            DbcParser.write_sig_file(signals_file=signals_file, msg_sig_map=msg_sig_map)
        print(signals_file.split('.')[0] + " dbc is parsed " + ("and Java file Generated" if write_sig_file else ""))

    @staticmethod
    def parse_dbc_cycle_time(*, file: str,
                             raw_regex_id_msg_name_sending_node: str =
                             RAW_REGEX_MSG_ID_NAME_SENDING_NODE,
                             raw_regex_msg_id_cycle_time: str = REGEX_MSG_ID_CYCLE_TIME):
        msg_id_name_map, msg_name_sending_node_map, msg_id_cycle_time_map = dict(), dict(), dict()
        try:
            with open(
                    file.strip(), 'r', encoding='unicode_escape') as f:
                s = f.read()
                matches = re.finditer(raw_regex_id_msg_name_sending_node, s, re.MULTILINE | re.DOTALL)
        except FileNotFoundError as ex:
            print("file {0} is not found".format(file), file=sys.stderr)
            print("".join(traceback.TracebackException.from_exception(ex).format()))
            exit(1)
        for msg in matches:
            msg_id_name_map[msg.group('Msg_ID')] = msg.group('Msg_Name').strip()
            msg_name_sending_node_map[msg.group('Msg_Name')] = msg.group('Sending_Node').strip()
        matches = re.finditer(raw_regex_msg_id_cycle_time, s)
        for msg in matches:
            msg_id_cycle_time_map[msg.group('Msg_ID')] = msg.group('Cycle_t').strip()
        return msg_id_name_map, msg_name_sending_node_map, msg_id_cycle_time_map

    @staticmethod
    def get_Host_Tx_Messages_list(*, msg_node_map: dict, ecu_names_dbc: List[str] = ECU_NAMES_DBC) -> list:
        """
        :param ecu_names_dbc: Optional Arg (list containing the Host ECU Names in each of the dbc files)
        :param msg_node_map: Dictionary containing all the can msg names mapping to the sending node
        :return: List of All Host Tx Message
        """
        host_tx_msgs_list = list()
        for Msg in filter(lambda x: msg_node_map[x] in ecu_names_dbc, msg_node_map.keys()):
            host_tx_msgs_list.append(Msg)
        return host_tx_msgs_list
