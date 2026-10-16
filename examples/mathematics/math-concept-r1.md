# Differentiability, differentials, and continuity

This is a fixed example chosen before scoring. Both outputs received overall comprehensibility 5/5; the primary A/C comparison was a tie. Neither received a primary technical error flag.

A defines differentiability as a linear decomposition and then proves equivalence with the derivative. C builds that decomposition directly from the derivative limit using an explicit vanishing error, then returns to the differential and approximation. The primary judge noted A's distinction between a numerical derivative and a differential, and C's distinction between an exact decomposition and an approximation. These are different explanatory routes, with no measured advantage in this pair.

Task `math-concept`, repetition `1`. Generation and primary judging used GPT-6.1 Sol at medium reasoning effort. These are text ratings, not evidence of human learning or transfer. The Chinese outputs are reproduced in full without editing.

Sources: [task packet](../../evaluations/tasks/math-concept.json), [primary anonymous judgment](../../evaluations/judgments/P741985557667.json), [complete descriptive results](../../evaluations/summary.json).

| Condition | Overall comprehensibility | Primary correctness | Primary minor flags | Output length (characters) |
| --- | ---: | ---: | ---: | ---: |

| A | 5 | 5 | 0 | 1240 |

| C | 5 | 5 | 0 | 1304 |


Character counts include notation and markup. Length differences alone do not establish quality or efficiency.

## Original outputs

### A: Baseline

[Original output JSON](../../evaluations/outputs/math-concept-A-r1.json); primary anonymous text ID `T090c9b0b6026` in [judgment JSON](../../evaluations/judgments/P741985557667.json).

````markdown
对一元实函数，**增量是函数值的实际变化，微分是其中关于自变量增量的线性部分**。可导、可微与连续的联系，就建立在这两种变化的比较上。

设 \(f\) 在内点 \(x_0\) 的一个邻域内有定义，自变量从 \(x_0\) 变为 \(x_0+h\)，实际增量为
\[
\Delta y=f(x_0+h)-f(x_0).
\]
连续只要求当 \(h\to0\) 时，\(\Delta y\to0\)，即自变量变化趋于零，函数值的变化也趋于零。它并未要求二者的比值有极限。

可导进一步要求变化率趋于一个有限值：
\[
f'(x_0)=\lim_{h\to0}\frac{\Delta y}{h}.
\]
这里 \(h\) 可以从正、负两个方向趋于零，两侧必须得到同一个有限极限。

可微则从“能否用线性部分描述实际变化”的角度提出要求：存在与 \(h\) 无关的实数 \(a\)，使
\[
\Delta y=ah+r(h),\qquad \frac{r(h)}h\to0.
\]
余项记作 \(o(h)\)。它不仅趋于零，而且相对于 \(h\) 也可以忽略。令 \(dx=h\)，便把线性部分定义为微分：
\[
dy=a\,dx.
\]
因此，微分不是实际增量的另一种记号；两者相差余项 \(r(h)\)。

**一元函数在内点处，可导与可微等价。** 若可导，令 \(a=f'(x_0)\)，则
\[
\frac{\Delta y-ah}{h}=\frac{\Delta y}{h}-a\to0,
\]
恰好得到可微所要求的余项。反过来，若可微，将分解式除以非零的 \(h\)，就有
\[
\frac{\Delta y}{h}=a+\frac{r(h)}h\to a.
\]
所以导数存在，且 \(a=f'(x_0)\)。导数是一个数，微分则是这个数乘以自变量增量。

例如 \(f(x)=x^2\)，在 \(x_0\) 处，
\[
\Delta y=2x_0h+h^2,\qquad dy=2x_0h.
\]
实际增量包含 \(h^2\)，微分只保留线性项。由于 \(h^2/h\to0\)，当 \(h\) 很小时，可用 \(dy\) 近似 \(\Delta y\)，相应地，
\[
f(x_0+h)\approx f(x_0)+f'(x_0)h.
\]
这是线性近似，不是一般成立的精确等式。特别在 \(x_0=0\) 时，\(dy=0\)，而 \(\Delta y=h^2\)：微分为零，并不表示实际变化为零。

由可微的分解式可知，线性项和余项都趋于零，故可导必连续。但连续不能反推可导或可微：\(f(x)=|x|\) 在零点连续，左导数为 \(-1\)，右导数为 \(1\)，无法得到统一的线性系数。因此关系是
\[
\boxed{\text{可导}\iff\text{可微}\ \Longrightarrow\ \text{连续}},
\]
其中最后一个箭头不能反向。
````

### C: Readability-only

[Original output JSON](../../evaluations/outputs/math-concept-C-r1.json); primary anonymous text ID `Tea30e8e73556` in [judgment JSON](../../evaluations/judgments/P741985557667.json).

````markdown
对一元实函数，在定义域内点处，**可导与可微等价，二者都蕴含连续；连续却不一定可导、可微。**理解这些关系，关键是区分实际增量、变化率与线性部分。

设 \(f\) 在内点 \(x_0\) 的一个邻域内有定义。自变量从 \(x_0\) 变到 \(x_0+h\) 时，函数的实际增量为
\[
\Delta y=f(x_0+h)-f(x_0).
\]
连续只要求：当 \(h\to0\) 时，\(\Delta y\to0\)。它关心函数值的变化能否趋于零，并未要求变化量与 \(h\) 的比值趋于某个数。

可导则要求变化率具有确定的有限极限：
\[
f'(x_0)=\lim_{h\to0}\frac{\Delta y}{h}.
\]
若这个极限为 \(a\)，就可以写成
\[
\frac{\Delta y}{h}=a+\varepsilon(h),\qquad \varepsilon(h)\to0,
\]
于是
\[
\Delta y=ah+h\varepsilon(h)=ah+o(h).
\]
这正是可微的定义：实际增量可以分解为关于 \(h\) 的线性部分 \(ah\)，以及相对于 \(h\) 可以忽略的余项。这里 \(a\) 与 \(h\) 无关；\(o(h)\) 表示余项除以 \(h\) 后趋于零，并非仅仅表示余项本身趋于零。

反过来，若可微，即
\[
\Delta y=ah+r(h),\qquad \frac{r(h)}h\to0,
\]
那么对 \(h\ne0\)，两边除以 \(h\)，便有
\[
\frac{\Delta y}{h}=a+\frac{r(h)}h\to a.
\]
因此可导，且 \(f'(x_0)=a\)。这说明，在这里，可导与可微是同一局部性质的两种表达：前者看变化率的极限，后者看增量能否作线性分解。又因为 \(ah\to0\)、\(r(h)\to0\)，所以 \(\Delta y\to0\)，从而连续。

令 \(dx=h\)，把线性部分定义为微分：
\[
dy=f'(x_0)\,dx=f'(x_0)h.
\]
**微分不是实际增量，而是实际增量的线性部分。**等式 \(\Delta y=dy+o(h)\) 是精确的分解；写成 \(\Delta y\approx dy\)，才是在用微分作近似。这里保证的是误差相对于 \(h\) 趋于零，并不一概保证误差相对于 \(\Delta y\) 趋于零。

例如 \(f(x)=x^2\)，在 \(x_0\) 处，
\[
\Delta y=2x_0h+h^2,\qquad dy=2x_0h.
\]
二者相差 \(h^2\)，且 \(h^2/h\to0\)。特别地，在 \(x_0=0\) 时，\(dy=0\)，而非零 \(h\) 对应的实际增量为 \(h^2\)，并不为零。

最后，\(f(x)=|x|\) 在零点满足 \(\Delta y=|h|\to0\)，所以连续；但左导数为 \(-1\)，右导数为 \(1\)，导数不存在，因此也不可微。这表明，连续只控制增量趋零，不能保证存在统一的线性部分。
````
