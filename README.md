## Bond Portfolio Optimization with Python
Optimize a portfolio of bond funds (ETFs) with linear programming. Given a set of funds, maximize the yield to maturity (YTM) with credit quality, duration, and sector constraints.

### Required packages
* pandas - Data manipulation and analysis.
* PuLP - A high-level linear programming modeler.

### Dataset
```
|name                    |ticker|price |credit|credit_num|duration|govt  |mbs   |corp  |ytm   |coupon|expense |non_benchmark|
|------------------------|------|------|------|----------|--------|------|------|------|------|------|--------|-------------|
|Money Market            |SPAXX |1     |AAA   |1         |0.1     |1     |0     |0     |0.001 |0.001 |0.000042|0            |
|iShares:US Treasury Bond|GOVT  |27.965|AAA   |1         |6.6     |1     |0     |0     |0.0052|0.0211|0.0015  |0            |
|iShares:Lng-Trm Corp Bd |IGLB  |71.25 |BBB   |4         |13.95   |0.04  |0     |0.96  |0.0366|0.0477|0.0006  |0            |
|iShares:MBS ETF         |MBB   |110.33|A     |3         |2.5     |0     |1     |0     |0.0261|0.0408|0.0006  |0            |
|iShares:1-3 Trs Bd ETF  |SHY   |86.485|AAA   |1         |1.84    |1     |0     |0     |0.016 |0.0175|0.0015  |0            |
|SPDR Bbg Barc ST Hi Yld |SJNK  |25.99 |BB    |5         |1.99    |0     |0     |1     |0.0629|0.0641|0.004   |1            |
|SPDR Ptf Aggregate Bond |SPAB  |30.86 |AAA   |1         |6.09    |0.449 |0.268 |0.266 |0.0114|0.0297|0.0004  |0            |
|Vanguard ST Corp Bd;ETF |VCSH  |82.96 |A     |3         |2.8     |0     |0     |1     |0.01  |0.033 |0.0005  |0            |
|iShares:TIPS Bd ETF     |TIP   |126.51|AAA   |1         |7.46    |1     |0     |0     |0.0186|0.0068|0.0019  |1            |
|Vanguard Tot Bd;ETF     |BND   |88.42 |A     |3         |6.01    |0.4815|0.2022|0.3163|0.0097|0.0239|0.0004  |0            |
```
#### Variables
| Variable        | Description                                           |
|-----------------|-------------------------------------------------------|
| `name`          | Bond fund name.                                       |
| `ticker`        | Ticker symbol.                                        |
| `price`         | Price per share (USD, not updated).                   |
| `credit`        | S&P credit rating.                                    |
| `credit_num`    | S&P credit rating converted to numerical values.      |
| `duration`      | Bond fund duration.                                   |
| `govt`          | Exposure in government or government-related sectors. |
| `mbs`           | Exposure in mortgage-backed sector.                   |
| `corp`          | Exposure in corporate sector.                         |
| `coupon`        | Average coupon.                                       |
| `expense`       | Expense ratio.                                        |
| `ytm`           | Yield to maturity.                                    |
| `non_benchmark` | Non-benchmark identifier.                             |

#### Decision variables
Weights to assign to each bond fund.

#### Objective
Maximize portfolio YTM.

#### Constraints
* Portfolio weights must sum to 1 (100%).
* Portfolio `credit_num` must be between 1 (AAA) and 3 (A).
* Portfolio `duration` limited to ± 20% the benchmark duration.
* Portfolio sector exposures (`govt`, `mbs`, `corp`) limited to ± 25% the benchmark equivalent.
* Non-benchmark funds must not exceed 10% combined weight.

#### Benchmark
The benchmark is the Bloomberg Barclays US Aggregate Bond Index, proxied by the `SPAB` fund.

### Code
Refer to [optimization.py](https://github.com/shenlim/portfolio-optimization/blob/master/optimization.py).
