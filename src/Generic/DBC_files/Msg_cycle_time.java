package Generic.DBC_files;
import java.util.LinkedHashMap;
public class Msg_cycle_time{

@SuppressWarnings("serial")
 public static LinkedHashMap<String, Integer> CAN1_Msg_Name_Cycle_Time_Map_Host_Tx= new LinkedHashMap<String, Integer>() {{
 put("Msg_05231AA",200);
}};

@SuppressWarnings("serial")
 public static LinkedHashMap<String, Integer> CAN1_Msg_Name_Cycle_Time_Map_Host_Rx= new LinkedHashMap<String, Integer>() {{
 put("Msg_0A5CE1327",10);
put("S_039",40);
}};

@SuppressWarnings("serial")
 public static LinkedHashMap<String, Integer> CAN2_Msg_Name_Cycle_Time_Map_Host_Tx= new LinkedHashMap<String, Integer>() {{
 put("Msg_0",56);
put("O_I_f___1",56);
put("O_I_f___2",56);
put("O_I_f___3",56);
put("O_I_f___4",56);
put("O_I_f___5",56);
put("O_I_f___6",56);
put("O_I_f___7",56);
put("O_I_f___8",56);
put("O_I_f___9",56);
put("O_I_f___10",56);
put("O_I_f___11",56);
put("O_I_f___12",56);
}};

@SuppressWarnings("serial")
 public static LinkedHashMap<String, Integer> CAN2_Msg_Name_Cycle_Time_Map_Host_Rx= new LinkedHashMap<String, Integer>() {{
 put("RCanT",250);
}};

/**
 * 
 * @param Tx_Rx 		true for Host_Tx
 * @param CAN1_CAN2		true for CAN1
 * @param msgName		msgName for which cycleTime is needed
 * @return				returns cycle time of msg or Null if msg is not found.
 */
public static int getCanMsgCycleTime(boolean Tx_Rx,boolean CAN1_CAN2, String msgName) {
	return (CAN1_CAN2)?getCAN1MsgCycleTime(Tx_Rx, msgName):getCAN2MsgCycleTime(Tx_Rx, msgName);
}
private static int getCAN2MsgCycleTime(boolean tx_Rx, String msgName) {
	return (tx_Rx)?CAN2_Msg_Name_Cycle_Time_Map_Host_Tx.get(msgName):CAN2_Msg_Name_Cycle_Time_Map_Host_Rx.get(msgName);
}
private static int getCAN1MsgCycleTime(boolean tx_Rx, String msgName) {
	return (tx_Rx)?CAN1_Msg_Name_Cycle_Time_Map_Host_Tx.get(msgName):CAN1_Msg_Name_Cycle_Time_Map_Host_Rx.get(msgName);
}
}
