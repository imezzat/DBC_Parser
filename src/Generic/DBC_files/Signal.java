package Generic.DBC_files;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.LinkedHashMap;

public interface Signal {
	default void init(final String Bits, final String Signed_unsigned, final String Factor,
			final String offset, final String MinDbc, final String MaxDbc,
			final String initialVal) {
		setBits(Integer.parseInt(Bits));
		setSigned_unsigned(Signed_unsigned.equals("-"));
		setFactor(Double.parseDouble(Factor));
		setOffset(Double.parseDouble(offset));
		final int length_digits_before_E = Factor.matches("\\d\\.\\d+E.*")
				? Factor.substring(Factor.indexOf(".") + 1, Factor.indexOf("E")).length()
				: 0;
		setPrecision(length_digits_before_E + (Factor.contains("E")
				? Integer.parseInt(Factor.substring(Factor.indexOf("E") + 2))
				: Factor.substring(Factor.indexOf('.') + 1).length()));
		final double max_raw_val = Math.pow(2, isSigned_unsigned() ? getBits() - 1 : getBits()) - 1;
		setMax(BigDecimal.valueOf(max_raw_val).multiply(new BigDecimal(Factor))
				.setScale(getPrecision(), RoundingMode.HALF_UP).add(new BigDecimal(getOffset()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		setMin((isSigned_unsigned() ? BigDecimal.valueOf(Math.pow(2, getBits() - 1) * -1)
				.multiply(new BigDecimal(Factor)).setScale(getPrecision(), RoundingMode.HALF_UP)
				.add(new BigDecimal(getOffset())) : new BigDecimal(getOffset()))
						.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		setInitVal((new BigDecimal(initialVal).compareTo(new BigDecimal(max_raw_val)) < 1
				? new BigDecimal(initialVal)
						.multiply(new BigDecimal(Factor).setScale(getPrecision(),
								RoundingMode.HALF_UP))
						.add(new BigDecimal(getOffset()))
						.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros()
						.max(getMin()).min(getMax())
				: new BigDecimal(getOffset()).stripTrailingZeros()).toString());
		setBva_Max(getMax().subtract(new BigDecimal(getFactor()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		setBva_Min(getMin().add(new BigDecimal(getFactor()))
				.setScale(getPrecision(), RoundingMode.HALF_UP).stripTrailingZeros());
		setBva_list(new LinkedHashMap<>());
		getBva_list().put("min", getMin());
		if (getBva_Min().compareTo(getMax()) == -1)
			getBva_list().put("minb", getBva_Min());
		getBva_list().put("mid", null);
		if (getBva_Max().compareTo(getMin()) == 1)
			getBva_list().put("maxb", getBva_Max());
		getBva_list().put("max", getMax());
		setMinDbc(new BigDecimal(MinDbc));
		setMaxDbc(new BigDecimal(MaxDbc));
	}

	default String getSig_Name() {
		return toString();
	}

	default String getMsg_Name() {
		return
				getClass().getClass().getSimpleName()
						.substring(
								getClass().getClass().getSimpleName()
										.lastIndexOf(
								getClass().getPackage().getName()
										.substring(getClass().getPackage().getName().lastIndexOf('.') + 1)
										+ "_Signals_")+1);
	}

	default void set_Factor(final double Factor) {
		setFactor(Factor);
		setPrecision(
				String.valueOf(Factor).substring(String.valueOf(Factor).indexOf('.') + 1).length());

	}

	public int getBits();

	public double getFactor();

	public BigDecimal getInitialVal();

	public double getOffset();

	public BigDecimal getMin();

	public BigDecimal getMax();

	public void set_Max(String max);

	public void set_Min(String min);

	public void setMax(BigDecimal max);

	public void setMin(BigDecimal min);

	public void setMaxDbc(String maxDbc);

	public void setMinDbc(String minDbc);

	public BigDecimal getMaxDbc();

	public BigDecimal getMinDbc();

	public LinkedHashMap<String, BigDecimal> get_Bva_list();

	public void addToBvaList(String key, String val);

	public int getPrecision();

	public void setInitVal(String initVal);

	BigDecimal getBva_Min();

	BigDecimal getBva_Max();

	LinkedHashMap<String, BigDecimal> getBva_list();

	void setBva_Min(BigDecimal bvaMin);

	void setBva_Max(BigDecimal bvaMax);

	boolean isSigned_unsigned();

	void setSigned_unsigned(boolean signed_unsigned);

	void setBits(int bits);

	void setFactor(double factor);

	void setOffset(double offset);

	void setMinDbc(BigDecimal minDbc);

	void setMaxDbc(BigDecimal maxDbc);

	void setPrecision(int precision);

	void setBva_list(LinkedHashMap<String, BigDecimal> bva_list);
}
