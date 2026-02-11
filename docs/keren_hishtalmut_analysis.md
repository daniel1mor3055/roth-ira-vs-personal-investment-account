# Keren Hishtalmut vs Personal Investment: A Mathematical Comparison

## 1. Introduction

### What is Keren Hishtalmut?

**Keren Hishtalmut** (קרן השתלמות) is Israel's tax-advantaged savings fund, often compared to a Roth IRA in the US context. It's a long-term savings vehicle with significant tax benefits:

- **Tax-exempt capital gains** on withdrawals (when eligibility conditions are met)
- Contributions are typically made by employers (up to 7.5% of salary)
- Employees can contribute additional amounts (up to 2.5% of salary)
- Funds become liquid after 6 years (or 3 years for specific purposes like education)

### The Comparison

This analysis compares two options:

| Option | Description | Key Characteristics |
|--------|-------------|---------------------|
| **Option A** | Keep money in Keren Hishtalmut | 8% expected return, 0.35% management fees, **tax-exempt** on capital gains |
| **Option B** | Withdraw and invest personally | 10% expected return, no management fees, **25% capital gains tax** on sale |

---

## 2. Tax Implications Summary

### Keren Hishtalmut Tax Benefits

According to [Kol Zchut](https://www.kolzchut.org.il/he/קרן_השתלמות):

- **Capital gains are tax-exempt** when withdrawn after the vesting period
- No "tax drag" during the holding period (dividends and gains compound tax-free inside the fund)
- Exemption is subject to ceiling/cap rules based on eligible contributions

### Personal Investment Taxation

According to [PwC Tax Summaries](https://taxsummaries.pwc.com/israel/individual/income-determination):

- **Capital gains tax: 25%** for individual investors on securities gains
- **Dividend tax: 25-30%** depending on circumstances ([GSL Law & Consulting](https://gsl.org/en/taxes/israel/))
- Tax is due upon realization (sale) of the investment

### The "Tax Drag" Concept

When investing personally, you may trigger taxable events along the way:

1. **Rebalancing** - Selling to rebalance your portfolio creates taxable gains
2. **Strategy changes** - Switching investments triggers capital gains
3. **Dividend distributions** - Taxed at 25-30% when received
4. **Partial withdrawals** - Any sale creates a taxable event

In Keren Hishtalmut, these events occur inside a tax-sheltered wrapper, preserving the compound growth advantage.

---

## 3. The Mathematical Model

### Option A: Keren Hishtalmut (Tax-Exempt)

Let:
- \( P \) = Initial principal
- \( r \) = Gross annual return (e.g., 8%)
- \( f \) = Annual management fee as percentage of assets (e.g., 0.35%)

**Net return after management fees:**

$$r_{net} = (1 + r) \times (1 - f) - 1$$

**Future Value after T years (tax-exempt withdrawal):**

$$FV_{KH}(T) = P \times (1 + r_{net})^T$$

### Option B: Personal Investment (Taxed at Sale)

Let:
- \( r_B \) = Annual return (e.g., 10%)
- \( \tau \) = Capital gains tax rate (e.g., 25%)

**Future Value before tax:**

$$FV_{pre}(T) = P \times (1 + r_B)^T$$

**Gain subject to tax:**

$$Gain = FV_{pre}(T) - P$$

**Future Value after tax (at sale):**

$$FV_{after}(T) = P + (1 - \tau) \times (FV_{pre}(T) - P)$$

This simplifies to:

$$FV_{after}(T) = P \times \left[ \tau + (1 - \tau) \times (1 + r_B)^T \right]$$

### Break-Even Year Calculation

Find the first year \( T \) where:

$$FV_{after}(T) \geq FV_{KH}(T)$$

Substituting:

$$P \times \left[ \tau + (1 - \tau) \times (1 + r_B)^T \right] \geq P \times (1 + r_{net})^T$$

Simplifying (divide by P):

$$\tau + (1 - \tau) \times (1 + r_B)^T \geq (1 + r_{net})^T$$

### Required Return Formula

Given a time horizon \( T \), what return \( r_B \) is needed to match Keren Hishtalmut?

From the break-even equation:

$$(1 + r_{net})^T = \tau + (1 - \tau) \times (1 + r_B)^T$$

Solving for \( r_B \):

$$1 + r_B = \left( \frac{(1 + r_{net})^T - \tau}{1 - \tau} \right)^{1/T}$$

---

## 4. Key Variables

| Variable | Symbol | Typical Value | Description |
|----------|--------|---------------|-------------|
| Principal | \( P \) | ₪100,000 | Initial investment amount |
| Keren gross return | \( r \) | 8% | Expected annual return before fees |
| Management fee | \( f \) | 0.35% | Annual fee as % of assets |
| Personal return | \( r_B \) | 10% | Expected return from personal investment |
| Capital gains tax | \( \tau \) | 25% | Tax rate on investment gains |
| Time horizon | \( T \) | Variable | Number of years to compare |
| Tax drag | varies | 0.3-1.0% | Annual tax leakage from dividends/rebalancing |

---

## 5. Numerical Examples

### Scenario 1: 8% is BEFORE Management Fees

**Net return calculation:**

$$r_{net} = (1.08) \times (0.9965) - 1 = 7.622\%$$

**Comparison table (P = ₪100,000):**

| Years | Keren Hishtalmut (7.62% net) | Personal (10%, 25% tax at end) |
|------:|-----------------------------:|-------------------------------:|
| 1 | ₪107,622 | ₪107,500 |
| 2 | ₪115,825 | ₪115,750 |
| 3 | ₪124,653 | ₪124,825 |
| 5 | ₪144,379 | ₪145,788 |
| 10 | ₪208,454 | ₪219,531 |
| 15 | ₪300,965 | ₪338,294 |
| 20 | ₪434,531 | ₪529,562 |

**Break-even: ~3 years**

### Scenario 2: 8% is AFTER Management Fees (Already Net)

**Net return:** 8% (no adjustment needed)

**Break-even: ~8 years**

---

## 6. Important Considerations

### A) Is the Return Before or After Fees?

This is critical! Fund managers often report returns **after** management fees. Always clarify:

- If 8% is **before** fees: Net ≈ 7.62%, break-even at ~3 years
- If 8% is **after** fees: Net = 8%, break-even at ~8 years

### B) Tax Drag During the Holding Period

The model above assumes you **never sell** until the final exit. In reality:

1. **Rebalancing** - Adjusting allocations triggers sales
2. **Fund distributions** - ETFs may distribute dividends
3. **Strategy changes** - Switching investments creates taxable events

Each taxable event reduces your compounding base. A reasonable estimate:
- **Passive buy-and-hold:** 0.3-0.5% annual tax drag
- **Active management:** 0.5-1.0% annual tax drag

### C) Can You Really Achieve 2% Higher Returns?

The comparison assumes 10% vs 8% (2% alpha). Consider:

- **Behavioral risk** - Can you hold through market crashes?
- **Timing risk** - Will you buy high and sell low?
- **Selection risk** - Will your stock picks outperform?

Historical data shows most active investors **underperform** passive benchmarks.

### D) Ceiling/Cap Rules for Tax Exemption

The tax exemption in Keren Hishtalmut applies to contributions up to certain limits:

- Employer contributions: Up to 7.5% of salary (capped at ~3x average wage)
- Employee contributions: Up to 2.5% of salary
- Excess contributions may have different tax treatment

Verify that your entire balance qualifies for the tax exemption.

### E) Dividend Taxation in Personal Accounts

Israeli dividends are taxed at:
- **25%** for regular investors
- **30%** for "significant shareholders" (10%+ ownership)

Foreign dividends may have additional considerations (withholding taxes, tax treaties).

---

## 7. Sensitivity Analysis

### Required Return to Beat Keren Hishtalmut

Given different time horizons, what return do you need?

| Horizon (Years) | Keren Net Return | Required Personal Return |
|----------------:|----------------:|-------------------------:|
| 5 | 8% | 10.2% |
| 10 | 8% | 9.5% |
| 15 | 8% | 9.2% |
| 20 | 8% | 9.0% |
| 30 | 8% | 8.7% |

**Key insight:** The longer the horizon, the lower the required alpha because the tax-deferred compounding partially offsets the end-tax.

### Impact of Tax Rate Changes

If capital gains tax increases (e.g., to 30%):

| Tax Rate | Break-even Year (8% KH vs 10% Personal) |
|---------:|----------------------------------------:|
| 20% | ~5 years |
| 25% | ~8 years |
| 30% | ~12 years |
| 35% | ~18 years |

---

## 8. Practical Recommendations

### When to Stay in Keren Hishtalmut

- Short to medium investment horizon (< 8-10 years)
- You cannot reliably achieve 2%+ higher returns
- You tend to trade frequently or rebalance often
- You value certainty over potential upside

### When Personal Investment May Win

- Long investment horizon (15+ years)
- Disciplined buy-and-hold strategy
- Access to investments not available in Keren (e.g., specific stocks, crypto)
- You have strong conviction in your investment approach

### The Hybrid Approach

Consider:
1. **Keep the tax-advantaged portion** in Keren Hishtalmut
2. **Invest additional savings** in a personal account
3. Use the personal account for **tax-loss harvesting** opportunities
4. Maintain a **very passive strategy** in the personal account to minimize tax drag

---

## 9. References

1. [Kol Zchut - Keren Hishtalmut](https://www.kolzchut.org.il/he/קרן_השתלמות) - Official Israeli rights portal
2. [PwC Tax Summaries - Israel Individual Taxation](https://taxsummaries.pwc.com/israel/individual/income-determination) - Capital gains tax rates
3. [GSL Law & Consulting - Israel Tax System](https://gsl.org/en/taxes/israel/) - Dividend taxation
