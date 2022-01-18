REGEX_CAPTURE_MSGS_SIGS = r"BO_\s+(?P<Msg_ID>[0-9]+)\s+(?P<Msg_Name>[\w_\d]+):\s+\d+\s+\w+$\s+(?P<Sigs>[^$]+)"
"""# Used to capture the Msg along with all its signals from dbc
(added $ between Msgs in place of empty lines) to avoid catastrophic backtracking since the file is huge
"""
SIGNAL_ENUM_INSTANCE_VARS = ";\nprivate int Bits;\n private boolean Signed_unsigned;\n private double Factor;\n " \
                            "private double " \
                            "Offset;\n private BigDecimal InitVal;\n private BigDecimal Min;\n private BigDecimal " \
                            "Max;\nprivate BigDecimal MinDbc;\n private BigDecimal MaxDbc;\nprivate BigDecimal " \
                            "Bva_Min;\nprivate BigDecimal Bva_Max;\n" \
                            "private int precision;\nprivate LinkedHashMap<String,BigDecimal> bva_list;\n" \
                            "private static final String MsgName= MethodHandles.lookup().lookupClass().getSimpleName().substring(MethodHandles.lookup().lookupClass().getSimpleName().lastIndexOf(\"_Signals_\")+1);\n "
SIGNALS_ENUM_METHODS = """	@Override
	public int getBits() {
		return Bits;
	}

	@Override
	public double getFactor() {
		return Factor;
	}

	@Override
	public double getOffset() {
		return Offset;
	}

	@Override
	public BigDecimal getInitialVal() {
		return InitVal;
	}

	@Override
	public BigDecimal getMin() {
		return Min;
	}

	@Override
	public BigDecimal getMax() {
		return Max;
	}
	@Override
	public void setMin(final BigDecimal min) {
		Min = min;
	}

	@Override
	public void setMax(final BigDecimal max) {
		Max = max;
	}
	
	@Override
	public void setBva_Min(final BigDecimal bvaMin) {
		Bva_Min = bvaMin;
	}

	@Override
	public void setBva_Max(final BigDecimal bvaMax) {
		Bva_Max = bvaMax;
	}
    
    @Override
	public BigDecimal getBva_Min() {
		return Bva_Min;
	}
    
    @Override
	public BigDecimal getBva_Max() {
		return Bva_Max;
	}

	@Override
	public int getPrecision() {
		return precision;
	}

@Override
	public BigDecimal getMinDbc() {
		return MinDbc;
	}

	@Override
	public void setMinDbc(final String minDbc) {
		MinDbc = new BigDecimal(minDbc);
	}

	@Override
	public BigDecimal getMaxDbc() {
		return MaxDbc;
	}
	@Override
	public void setMaxDbc(final String maxDbc) {
		MaxDbc = new BigDecimal(maxDbc);
		}
    
	@Override
	public void setInitVal(final String initVal) {
		InitVal = new BigDecimal(initVal);

	}
	
	@Override
	public LinkedHashMap<String, BigDecimal> getBva_list() {
		return bva_list;
	}
	@Override
	public boolean isSigned_unsigned() {
		return Signed_unsigned;
	}

	@Override
	public void setSigned_unsigned(final boolean signed_unsigned) {
		Signed_unsigned = signed_unsigned;
	}

	@Override
	public void setBits(final int bits) {
		Bits = bits;
	}

	@Override
	public void setFactor(final double factor) {
		Factor = factor;
	}

	@Override
	public void setOffset(final double offset) {
		Offset = offset;
	}

	@Override
	public void setMinDbc(final BigDecimal minDbc) {
		MinDbc = minDbc;
	}

	@Override
	public void setMaxDbc(final BigDecimal maxDbc) {
		MaxDbc = maxDbc;
	}

	@Override
	public void setPrecision(final int precision) {
		this.precision = precision;
	}

	@Override
	public void setBva_list(final LinkedHashMap<String, BigDecimal> bva_list) {
		this.bva_list = bva_list;
	}
	
	public static String getMsgname() {
		return MsgName;
	}"""
""""Java Methods'  specified in Signal interface"""

SIGS_ENUM_CONSTRUCTOR = "{cl}(String Bits,String Signed_unsigned,String Factor,String offset,String MinDbc,String MaxDbc,String initialVal){{\n\
            init(Bits, Signed_unsigned, Factor, offset, MinDbc, MaxDbc, initialVal);\n\
	}}\n"
""""Formatted String referring to Signals enum constructor declaration. where cl should be assigned according to the 
desired enum name """

REGEX_EXT_SIGS_ATTS_FROM_BULK = r"SG_\s+(?P<Sig_Name>[\w_]+)(?:\sM\s|\sm\d+\s|\s+):\s+\d+\|(?P<Bits>\d+)@\d+(?P<Signed_unsigned>[+-])\s+\((?P<Factor>[\w\.-]+),(?P<Offset>[\w\.-]+).*?\[(?P<min>[-+0-9\.E]+)\|(?P<max>[-+0-9\.Ee]+)\]"
"""Used to extract each signal along with its attributes (signed,factor,offsett,number of Bits,minDBC,maxDBC)
for Ex:
SG_ IDAS_CHECKSUM_1A45AA23 : 59|4@0+ (1,0) [0|15] ""  TEL
"""
REGEX_SIGS_INIT_VAL = r"BA_\s+\"GenSigStartValue\"\s+SG_\s+(?P<Msg_ID>\d+)\s+(?P<Sig_Name>\w+)\s+(?P<InitVal>\d+)"
""""# used to extract signal init val from dbc according to attribute GenSigStartValue
# for Ex: BA_ "GenSigStartValue" SG_ 2588256803 IDAS_CHECKSUM_1A45AA23 0;
"""
SIG_FILE_HEADER = "package {pack};\nimport java.lang.invoke.MethodHandles;\nimport java.math.BigDecimal;\nimport java.util.LinkedHashMap;\nimport {parent_pack}.*;\npublic enum {cl} implements {base_class}{{\n"
"""Formatted string referencing the sigs file header till class decleration
    PlaceHolders:
        pack -> package name:
        cl -> enum name
        base_class -> parent enum name
"""
REGEX_MSG_ID_CYCLE_TIME = r"BA_\s+\"GenMsgCycleTime\"\s+BO_\s+(?P<Msg_ID>\d+)\s+(?P<Cycle_t>\d+)"
"""get msg cycle time with msg id mapping to be used to relate the msg name directly to cycle time"""
RAW_REGEX_MSG_ID_NAME_SENDING_NODE = r"BO_\s+(?P<Msg_ID>\d+)\s+(?P<Msg_Name>\w+):\s+\d+\s+(?P<Sending_Node>[A-Z]+)"
"""Used to relate Msg name to its cycle time and separate it into multiple hashmaps depending on Tx/Rx"""
ECU_NAMES_DBC = ["ADC", "HOST"]
"""List of Target ECU Names in different dbcs"""
MSG_CYCLE_TIME_ENTRY = "put(\"{msg}\",{cycle_t});\n"
"""
  Formatted String for each entry of Hashmap where key is msgName and the value is the cycle time.
"""
msgs_to_exclude_from_cycle_time = []
MSG_NAME_CYCLETIME_METHODS = """
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
"""
MSG_CYCLE_TIME_FILE_HEADER = "package {pack};\nimport java.util.LinkedHashMap;\npublic class {cl}{{\n"
MSG_CYCLE_TIME_HASHMAP_DEC = "\n@SuppressWarnings(\"serial\")\n public static LinkedHashMap<String, Integer> {name}= " \
                             "new LinkedHashMap<String, Integer>() {{{{\n "
CYCLE_TIME_HASHMAP_NAME_SUFFIX = "_Msg_Name_Cycle_Time_Map"
MSG_CYCLE_TIME_FILE_NAME = "Msg_cycle_time.java"
SIGS_FILE_NAMES = {"CAN2": "CAN2_Signals.java", "CAN1": "CAN1_Signals.java", "SPI": "SPI_Signals.java"}
DBC_PATHS = {"CAN2": r'CAN_dbc_2.dbc', "CAN1": r'CAN_dbc_1.dbc',
             "SPI": r'SPI_dbc.dbc'}
