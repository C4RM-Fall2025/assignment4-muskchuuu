
# Identify yourself for grading
def WhoAmI():
    return 'tc3394'

# ---------------- Bond Pricing (flat yield) ----------------
def getBondPrice(y, face, couponRate, m, ppy=1):
    """Price a plain-vanilla coupon bond under a flat yield y.
    y: annual yield to maturity (e.g., 0.03)
    face: face value
    couponRate: annual coupon rate (e.g., 0.04)
    m: years to maturity
    ppy: payments per year (default 1)
    """
    c = face * couponRate / ppy
    n = int(m * ppy)
    r = y / ppy

    pv_coupons = 0.0
    for t in range(1, n + 1):
        pv_coupons += c / ((1.0 + r) ** t)

    pv_face = face / ((1.0 + r) ** n)
    bondPrice = pv_coupons + pv_face
    return bondPrice

# ---------------- Macaulay Duration (years) ----------------
def getBondDuration(y, face, couponRate, m, ppy=1):
    """Macaulay duration in YEARS under a flat yield y."""
    c = face * couponRate / ppy
    n = int(m * ppy)
    r = y / ppy

    # price for weights
    price = getBondPrice(y, face, couponRate, m, ppy)

    # sum of t * PV(CF_t)
    sum_t_pvcf = 0.0
    for t in range(1, n + 1):
        cf_t = c if t < n else c + face
        pvcf_t = cf_t / ((1.0 + r) ** t)
        sum_t_pvcf += t * pvcf_t

    duration_periods = sum_t_pvcf / price  # in periods
    duration_years = duration_periods / ppy
    return duration_years

# ---------------- Term-structure pricing (enumerate) ----------------
def getBondPrice_E(face, couponRate, m, yc):
    """Price using a list of annual spot rates yc (one per year).
    Uses enumerate to get (t, r_t).
    Assumes annual coupon payments and len(yc) == m.
    """
    if len(yc) != m:
        raise ValueError("yc must have one spot rate per year (len(yc)==m).")

    c = face * couponRate
    price = 0.0
    for t, r_t in enumerate(yc, start=1):
        cf_t = c if t < m else c + face
        price += cf_t / ((1.0 + r_t) ** t)
    return price

# ---------------- Irregular times & term-structure (zip) ----------------
def getBondPrice_Z(face, couponRate, times, yc):
    """Price using irregular cashflow times and matching spot rates.
    - times: list of times in YEARS when cashflows occur (e.g., [1, 1.5, 3, 4, 7])
    - yc:    list of spot rates for each corresponding time (same length as times)
    Uses zip(times, yc) to iterate.
    Assumes coupon paid at every time in `times` and face repaid at the LAST time.
    """
    if len(times) != len(yc):
        raise ValueError("times and yc must be the same length.")

    c = face * couponRate  # annual coupon amount; paid at each listed time
    price = 0.0
    last_time = times[-1] if times else 0.0

    for t, r_t in zip(times, yc):
        cf_t = c + (face if t == last_time else 0.0)
        price += cf_t / ((1.0 + r_t) ** t)
    return price

# ---------------- FizzBuzz ----------------
def FizzBuzz(start, finish):
    """Return a list from start..finish (inclusive) with FizzBuzz rules.
    - multiples of 3 -> 'fizz'
    - multiples of 5 -> 'buzz'
    - multiples of 15 -> 'fizzbuzz'
    Otherwise, keep the number.
    """
    outlist = []
    step = 1 if finish >= start else -1
    for n in range(start, finish + step, step):
        s = ""
        if n % 3 == 0: s += "fizz"
        if n % 5 == 0: s += "buzz"
        outlist.append(s if s else n)
    return outlist

if __name__ == "__main__":
    # quick sanity checks that roughly align with your screenshots

    # Flat yield price & duration example
    p = getBondPrice(0.03, 2_000_000, 0.04, 10, ppy=1)
    d = getBondDuration(0.03, 2_000_000, 0.04, 10, ppy=1)
    print("Price (flat y=3%, m=10):", round(p, 2))
    print("Duration (years):", round(d, 2))

    # Term-structure with enumerate (m=5)
    yc = [0.010, 0.015, 0.020, 0.025, 0.030]
    p_enum = getBondPrice_E(2_000_000, 0.04, 5, yc)
    print("Price (enumerate, m=5):", round(p_enum, 2))

    # Irregular times with zip
    times = [1.0, 1.5, 3.0, 4.0, 7.0]
    yc_zip = [0.010, 0.015, 0.020, 0.025, 0.030]
    p_zip = getBondPrice_Z(2_000_000, 0.04, times, yc_zip)
    print("Price (zip, irregular):", round(p_zip, 2))

    # FizzBuzz demo
    print("FizzBuzz(1, 15):", FizzBuzz(1, 15))
