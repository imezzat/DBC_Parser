package Generic.DBC_files;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.LinkedHashMap;

public interface CAN_Signal extends Signal {
	@Override
	public default LinkedHashMap<String, BigDecimal> get_Bva_list() {
		getBva_list().entrySet().removeIf(entries -> entries.getValue() == null);
		return getBva_list();
	}

	@Override
	public default void addToBvaList(final String key, final String val) {
		getBva_list().put(key, new BigDecimal(val));
	}

	@Override
	public default void set_Min(final String min) {
		setMin(new BigDecimal(min));
		getBva_list().put("min", getMin());
		setBva_Min(getMin().add(new BigDecimal(getFactor()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		getBva_list().put("minb", getBva_Min());
	}

	@Override
	public default void set_Max(final String max) {
		setMax(new BigDecimal(max));
		getBva_list().put("max", getMax());
		setBva_Max(getMax().subtract(new BigDecimal(getFactor()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		getBva_list().put("maxb", getBva_Max());
	}
}