package Generic.DBC_files;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.LinkedHashMap;

public interface SPI_Signal extends Signal {
	@Override
	public default void addToBvaList(final String key, final String val) {
		getBva_list().put(key, new BigDecimal(val));
		if (VHC_DLM_helper.is_sig_float(this))
			return;
		BigDecimal value;
		if (SPI_CAN_Mapping.SPI_CAN_Sigs_Mapping.get(this) != null)
			for (CAN_Signal can_sig : SPI_CAN_Mapping.SPI_CAN_Sigs_Mapping.get(this)) {
				value = new BigDecimal(
						new BigDecimal(val).subtract(new BigDecimal(can_sig.getOffset()))
								.divide(new BigDecimal(can_sig.getFactor()), 2,
										RoundingMode.HALF_EVEN)
								.toBigInteger()).multiply(new BigDecimal(can_sig.getFactor()))
										.setScale(can_sig.getPrecision(), RoundingMode.HALF_UP)
										.add(new BigDecimal(can_sig.getOffset()))
										.setScale(can_sig.getPrecision(), RoundingMode.HALF_UP)
										.stripTrailingZeros();
				can_sig.addToBvaList(key, value.toString());
				if (key.equals("max") && value.compareTo(can_sig.getMax()) == 1)
					can_sig.set_Max(can_sig.getMax().toString());

				if (key.equals("min") && value.compareTo(can_sig.getMin()) == -1)
					can_sig.set_Min(can_sig.getMin().toString());

				if (value.compareTo(can_sig.getMax()) == 1 && !key.equals("max")
						|| value.compareTo(can_sig.getMin()) == -1 && !key.equals("min"))
					System.err.println("key " + key + " Value " + value + " is out of range ("
							+ can_sig.getMin() + "," + can_sig.getMax() + ") for mapped signal "
							+ can_sig);
				if (VHC_DLM_helper.is_diff_precision(this, can_sig))
					can_sig.get_Bva_list().entrySet()
							.removeIf(entries -> entries.getKey().contains("b"));
			}
	}

	@Override
	public default LinkedHashMap<String, BigDecimal> get_Bva_list() {
		if (!VHC_DLM_helper.is_sig_float(this)) {
			addToBvaList("min", getMin().toString());
			if (getBva_Min().compareTo(getMax()) == -1)
				getBva_list().put("minb", getBva_Min());
			if (getBva_Max().compareTo(getMin()) == 1)
				getBva_list().put("maxb", getBva_Max());
			addToBvaList("max", getMax().toString());
		}
		return getBva_list();
	}

	@Override
	public default void set_Min(final String min) {
		setMin(new BigDecimal(min));
		getBva_list().put("min", getMin());
		if (VHC_DLM_helper.is_sig_float(this))
			set_Factor(min.lastIndexOf(".") == -1 ? 1
					: Math.pow(10, -1 * min.substring(min.lastIndexOf(".") + 1).length()));
//		if (!VHC_DLM_helper.is_sig_float(this)) {
		setBva_Min(getMin().add(new BigDecimal(getFactor())
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros()));
		getBva_list().put("minb", getBva_Min());
//		}
	}

	@Override
	public default void set_Max(final String max) {
		setMax(new BigDecimal(max));
		getBva_list().put("max", getMax());
//		if (!VHC_DLM_helper.is_sig_float(this)) {
		setBva_Max(getMax().subtract(new BigDecimal(getFactor()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		getBva_list().put("maxb", getBva_Max());
//		}
	}

}