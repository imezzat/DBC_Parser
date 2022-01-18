import os
import re
import sys

from Generic.DBC_files.dbc_parser_constants import SIGS_FILE_NAMES, DBC_PATHS
from dbc_parser import DbcParser
from dbc_parser_constants import MSG_CYCLE_TIME_ENTRY, msgs_to_exclude_from_cycle_time, MSG_NAME_CYCLETIME_METHODS, \
    MSG_CYCLE_TIME_FILE_HEADER, MSG_CYCLE_TIME_HASHMAP_DEC, CYCLE_TIME_HASHMAP_NAME_SUFFIX, MSG_CYCLE_TIME_FILE_NAME


def create_msg_name_cycle_time_map_from_two_maps(msg_id_name_map: dict, msg_id_cycl_time_map: dict):
    msg_name_cycl_time_map = dict()
    for msg_id in filter(lambda x: msg_id_name_map[x] not in msgs_to_exclude_from_cycle_time, msg_id_name_map.keys()):
        try:
            msg_name_cycl_time_map[msg_id_name_map[msg_id]] = msg_id_cycl_time_map[msg_id]
        except:
            print("msg with id {id} was not found".format(id=msg_id), file=sys.stderr)
    return msg_name_cycl_time_map


def write_cycle_time_map_x_to_file(op, host_tx_msgs_list, msg_cycle_t_map: dict, struct_name):
    op.write(MSG_CYCLE_TIME_HASHMAP_DEC.format(name=struct_name + "_Host_Tx"))
    for msg_name in filter(lambda x: x in host_tx_msgs_list, msg_cycle_t_map.keys()):
        op.write(MSG_CYCLE_TIME_ENTRY.format(msg=msg_name, cycle_t=msg_cycle_t_map[msg_name]))
    op.write("}};\n")
    op.write(MSG_CYCLE_TIME_HASHMAP_DEC.format(name=struct_name + "_Host_Rx"))
    for msg_name in filter(lambda x: x not in host_tx_msgs_list, msg_cycle_t_map.keys()):
        op.write(MSG_CYCLE_TIME_ENTRY.format(msg=msg_name, cycle_t=msg_cycle_t_map[msg_name]))
    op.write("}};\n")


def write_msg_name_cycle_time_mapping_to_file(file_name: str, msg_name_cycle_map_1: dict, msg_name_cycle_map_2: dict,
                                              struct_1_name: str, struct_2_name: str, host_tx_msgs_list):
    with open(file_name, 'w') as op:
        op.write(MSG_CYCLE_TIME_FILE_HEADER.format(
            pack=".".join(re.split(r'[\\/]', os.path.dirname(os.path.realpath(__file__)))[-2:]),
            cl=file_name.split('.')[0]))
        write_cycle_time_map_x_to_file(op, host_tx_msgs_list, msg_cycle_t_map=msg_name_cycle_map_1,
                                       struct_name=struct_1_name)
        write_cycle_time_map_x_to_file(op, host_tx_msgs_list, msg_cycle_t_map=msg_name_cycle_map_2,
                                       struct_name=struct_2_name)
        op.write(MSG_NAME_CYCLETIME_METHODS)


def main():
    parse_dbcs()
    parse_dbc_write_msg_cycle_time()


def parse_dbcs():
    msg_id_name = dict()
    msg_id_name[SIGS_FILE_NAMES["CAN2"].split('.')[0]] = {}
    msg_id_name[SIGS_FILE_NAMES["CAN1"].split('.')[0]] = {}
    msg_id_name[SIGS_FILE_NAMES["SPI"].split('.')[0]] = {}
    DbcParser.parse_dbc(dbc_file_path=DBC_PATHS["CAN2"], signals_file=SIGS_FILE_NAMES["CAN2"],
                        msg_id_name=msg_id_name[SIGS_FILE_NAMES["CAN2"].split('.')[0]])
    DbcParser.parse_dbc(dbc_file_path=DBC_PATHS["CAN1"], signals_file=SIGS_FILE_NAMES["CAN1"],
                        msg_id_name=msg_id_name[SIGS_FILE_NAMES["CAN1"].split('.')[0]])
    DbcParser.parse_dbc(dbc_file_path=DBC_PATHS["SPI"], signals_file=SIGS_FILE_NAMES["SPI"],
                        msg_id_name=msg_id_name[SIGS_FILE_NAMES["SPI"].split('.')[0]], is_msg_id_hex=True)


def parse_dbc_write_msg_cycle_time():
    msg_name_id_map_p_can, msg_name_sending_node_map_p_can, msg_id_cycle_time_map_p_can = DbcParser.parse_dbc_cycle_time(
        file=DBC_PATHS["CAN2"])
    msg_name_id_map_v_can, msg_name_sending_node_map_v_can, msg_id_cycle_time_map_v_can = DbcParser.parse_dbc_cycle_time(
        file=DBC_PATHS["CAN1"])
    host_tx_messages = DbcParser.get_Host_Tx_Messages_list(
        msg_node_map={**msg_name_sending_node_map_v_can, **msg_name_sending_node_map_p_can})
    msg_name_cycle_time_v_can = create_msg_name_cycle_time_map_from_two_maps(msg_id_name_map=msg_name_id_map_v_can,
                                                                             msg_id_cycl_time_map=msg_id_cycle_time_map_v_can)
    msg_name_cycle_time_p_can = create_msg_name_cycle_time_map_from_two_maps(msg_id_name_map=msg_name_id_map_p_can,
                                                                             msg_id_cycl_time_map=msg_id_cycle_time_map_p_can)
    write_msg_name_cycle_time_mapping_to_file(file_name=MSG_CYCLE_TIME_FILE_NAME,
                                              msg_name_cycle_map_1=msg_name_cycle_time_v_can,
                                              msg_name_cycle_map_2=msg_name_cycle_time_p_can,
                                              struct_1_name=SIGS_FILE_NAMES["CAN1"].split('_')[
                                                                0] + CYCLE_TIME_HASHMAP_NAME_SUFFIX,
                                              struct_2_name=SIGS_FILE_NAMES["CAN2"].split('_')[
                                                                0] + CYCLE_TIME_HASHMAP_NAME_SUFFIX,
                                              host_tx_msgs_list=host_tx_messages)
    print("Msg cycle times Java file is Generated.")


if __name__ == "__main__":
    main()
