# Equivalent infinitesimals: four conditions and disputed error flags

This four-condition case is included after scoring to expose method-boundary problems and disagreement in technical evaluation, not as a success showcase. A is baseline, B rigor-only, C reader-aware-writing only, and D combines the two experimental modules. D does not load the full teaching skill. All four received overall comprehensibility 5/5, and all four planned pair comparisons were ties.

A tries an exact algebraic transformation before Taylor expansion. B, C, and D begin with Taylor-based error control, and C/D use x³=o(x) to show why first-order information can be insufficient. All compute the two requested limits correctly according to the primary review. That does not validate every general method recommendation.

The primary judge flagged B, C, and D for overgeneralizing the search for a first nonzero term. Those original flags are reproduced verbatim below. In a separate fresh-context technical adjudication, C's explicit necessity claim was accepted as minor, D's general advice was classified as a wording caution, and B's flag was rejected because its text says the expansion is optional (“可以”). These later verdicts do not replace or rewrite the primary scores. Once the numerator is already o(x³), dividing by x³ gives zero without finding a nonzero term.

Task `math-method`, repetition `1`. Generation and primary judging used GPT-6.1 Sol at medium reasoning effort. These are text ratings, not evidence of human learning or transfer. The Chinese outputs are reproduced in full without editing.

Sources: [task packet](../../evaluations/tasks/math-method.json), [primary anonymous judgment](../../evaluations/judgments/P9e472b536526.json), [complete descriptive results](../../evaluations/summary.json).

Separate technical review: [technical adjudication](../../evaluations/technical-adjudication.json). Its verdicts are distinct from the primary ratings.

| Condition | Overall comprehensibility | Primary correctness | Primary minor flags | Output length (characters) |
| --- | ---: | ---: | ---: | ---: |

| A | 5 | 5 | 0 | 1245 |

| B | 5 | 4 | 1 | 1442 |

| C | 5 | 4 | 1 | 1268 |

| D | 5 | 4 | 1 | 1389 |


Character counts include notation and markup. Length differences alone do not establish quality or efficiency.

## Primary technical flags, unchanged

A had no primary error flag. The following JSON reproduces each B/C/D primary error entry without altering its quote or reason.

Condition B:

```json
[
  {
    "severity": "minor",
    "quote": "抵消后，可以继续展开，直到找出首个非零项且余项除以分母趋于零",
    "reason": "把找到首个非零项设为继续展开的终点条件过强。若分子已是分母的高阶无穷小，极限即可确定为0，无须再展开。此问题仅涉及方法推广，不影响本题结果。"
  }
]
```

Condition C:

```json
[
  {
    "severity": "minor",
    "quote": "若它也抵消，就需要继续寻找更高阶的首个非零项。",
    "reason": "这一推广过强。对于分母为x³的极限，若三次项也抵消且余项已是o(x³)，就可直接得到极限为0，无须继续寻找更高阶非零项。此问题不影响本题两个极限的计算。"
  }
]
```

Condition D:

```json
[
  {
    "severity": "minor",
    "quote": "加减中若主项抵消，应继续寻找首个非零项，并核实余项相对于分母足够小",
    "reason": "将寻找首个非零项表述为抵消后的普遍要求，边界不够准确。若已证明分子相对于分母为高阶无穷小，就可直接得到极限为0，不必找到非零项。两个给定极限的计算正确。"
  }
]
```

## Original outputs

### A: Baseline

[Original output JSON](../../evaluations/outputs/math-method-A-r1.json); primary anonymous text ID `T089e538cdc31` in [judgment JSON](../../evaluations/judgments/P9e472b536526.json).

````markdown
这两个极限的关键区别，在于一阶主项是否发生抵消。判断能否用等价无穷小替换时，不能只看“每一项都与谁等价”，还要看运算后需要保留到什么阶。

等价关系的含义是
\[
\alpha(x)\sim\beta(x)
\quad\Longleftrightarrow\quad
\frac{\alpha(x)}{\beta(x)}\to1,
\]
其中分母在去心邻域内非零。因此，\(\sin x\sim x\)也可以写成
\[
\sin x=x+o(x).
\]
它保证误差除以\(x\)趋于零，却不保证误差除以\(x^3\)也趋于零。

对第一个极限，分母恰好是\(x\)，一阶信息已经足够：
\[
L_1=\lim_{x\to0}\frac{\sin x}{x}
=\lim_{x\to0}\frac{x+o(x)}x=1.
\]
这里没有相减抵消，替换误差经分母归一化后趋于零，所以直接使用\(\sin x\sim x\)即可。

对第二个极限，若把\(\tan x\)和\(\sin x\)分别替换成\(x\)，便得到\(x-x=0\)，但这只能说明一阶主项消失，不能说明原分子为零。仅凭两者都等价于\(x\)，只能知道
\[
\tan x-\sin x=o(x),
\]
还不足以确定它除以\(x^3\)后的极限。此时应继续寻找抵消后留下的首个非零项。

本题可先用恒等变形，把差式转为乘除形式：
\[
\tan x-\sin x=\frac{\sin x(1-\cos x)}{\cos x}.
\]
于是
\[
L_2=\lim_{x\to0}
\left(\frac{\sin x}{x}\right)
\left(\frac{1-\cos x}{x^2}\right)
\frac1{\cos x}
=1\cdot\frac12\cdot1=\frac12.
\]
取\(0<|x|\)足够小时，\(\cos x\ne0\)，上述变形成立。这里可以使用等价替换，是因为相关量已成为整体乘除因子，且各因子的极限明确。

若没有看出恒等式，也可用泰勒公式。由于一阶项抵消，而分母为\(x^3\)，将两项展开到三阶，并让余项为\(o(x^3)\)，便足以计算：
\[
\begin{aligned}
\tan x-\sin x
&=\left(x+\frac{x^3}{3}+o(x^3)\right)
-\left(x-\frac{x^3}{6}+o(x^3)\right)\\
&=\frac{x^3}{2}+o(x^3).
\end{aligned}
\]
除以\(x^3\)，同样得到\(L_2=\frac12\)。

实际判断时，先检查最低阶项会不会抵消，再看剩余误差相对于分母是否可忽略。加减式并非一律不能替换；关键是替换误差除以分母后须趋于零。分母的阶提示所需精度，但不能保证展开到该阶就一定出现非零项：若仍抵消，就需继续分析。对本题，三阶项已经非零，因此计算到这里即可。
````

### B: Rigor-only

[Original output JSON](../../evaluations/outputs/math-method-B-r1.json); primary anonymous text ID `Tc481633d6e8e` in [judgment JSON](../../evaluations/judgments/P9e472b536526.json).

````markdown
判断一阶等价替换是否足够，关键是看：替换丢掉的误差，会不会影响所求极限，尤其要留意加减后低阶项是否抵消。以下都取 \(0<|x|\) 足够小，使各分母非零。

等价无穷小的定义是
\[
\alpha(x)\sim\beta(x)
\quad\Longleftrightarrow\quad
\frac{\alpha(x)}{\beta(x)}\to1.
\]
因此，\(\sin x\sim x\) 表示两者的比值趋于 \(1\)，也可以写成
\[
\sin x=x+o(x).
\]
这里的误差除以 \(x\) 趋于零，但并未说明误差除以 \(x^3\) 后怎样变化。“一阶等价”不能直接当作精确相等使用。

对第一个极限，
\[
L_1=\lim_{x\to0}\frac{\sin x}{x}=1,
\]
这正是 \(\sin x\sim x\) 的定义所给出的结论。也可以将上面的误差表达式代入：
\[
\frac{\sin x}{x}=1+\frac{o(x)}x\to1.
\]
分母是一阶的 \(x\)，一阶等价已能控制所需误差，无须展开更多项。

第二个极限则不同：
\[
L_2=\lim_{x\to0}\frac{\tan x-\sin x}{x^3}.
\]
虽然 \(\tan x\sim x\)、\(\sin x\sim x\)，但分别替换后得到 \(x-x=0\)，只是把共同的一阶项消掉了，并没有确定原差值的大小。仅由这两个等价关系，我们只能推出
\[
\tan x-\sin x=o(x),
\]
而 \(o(x)/x^3\) 未必趋于零，所以不能据此判定 \(L_2=0\)。

若用泰勒公式，应保留到三次项，使相减后的余项仍能被分母控制：
\[
\begin{aligned}
\tan x-\sin x
&=\left(x+\frac{x^3}{3}+o(x^3)\right)
-\left(x-\frac{x^3}{6}+o(x^3)\right)\\
&=\frac{x^3}{2}+o(x^3).
\end{aligned}
\]
两个 \(o(x^3)\) 的差仍是 \(o(x^3)\)，因为除以 \(x^3\) 后，两者都趋于零。于是
\[
L_2=\lim_{x\to0}\left(\frac12+\frac{o(x^3)}{x^3}\right)
=\frac12.
\]

本题还有更简便的办法：先用恒等式把差改写成乘积，
\[
\tan x-\sin x=\frac{\sin x(1-\cos x)}{\cos x},
\]
从而
\[
\frac{\tan x-\sin x}{x^3}
=\frac{\sin x}{x}\cdot\frac{1-\cos x}{x^2}
\cdot\frac1{\cos x}
\longrightarrow1\cdot\frac12\cdot1=\frac12.
\]
这里使用了 \(1-\cos x\sim x^2/2\) 和 \(\cos x\to1\)；后者也保证了附近的 \(\cos x\ne0\)。

因此，选方法时先看结构：整体乘除中的因子可作等价替换；遇到加减，先检查首项是否抵消。抵消后，可以继续展开，直到找出首个非零项且余项除以分母趋于零；也可以先恒等变形，转成便于取极限的乘积。“本题展开到三次即可”来自分母与抵消情况，并不意味着所有差式都只需保留三次项。
````

### C: Readability-only

[Original output JSON](../../evaluations/outputs/math-method-C-r1.json); primary anonymous text ID `T71265177cdaa` in [judgment JSON](../../evaluations/judgments/P9e472b536526.json).

````markdown
判断一阶等价替换是否足够，关键是看：替换时略去的误差，会不会影响所求极限。尤其遇到加减，先检查低阶项是否抵消；一旦抵消，原来可以忽略的高阶项就可能决定答案。

等价关系的含义是
\[
\alpha(x)\sim\beta(x)
\quad\Longleftrightarrow\quad
\frac{\alpha(x)}{\beta(x)}\to1,
\]
其中分母在去心邻域内非零。因此，对第一个极限，
\[
L_1=\lim_{x\to0}\frac{\sin x}{x}=1.
\]
这正是 \(\sin x\sim x\) 的含义，无须展开到三次项。用误差来理解，就是 \(\sin x=x+o(x)\)，除以 \(x\) 后误差趋于零，所以一阶信息已经足够。

第二个极限则要先看分子：
\[
L_2=\lim_{x\to0}\frac{\tan x-\sin x}{x^3}.
\]
虽然 \(\tan x\sim x\)、\(\sin x\sim x\)，却不能分别替换后，把分子算成 \(x-x=0\)。两者的一阶项恰好抵消，差的大小取决于被略去的部分。仅凭一阶等价，我们只能写出
\[
\tan x-\sin x=(x+o(x))-(x+o(x))=o(x).
\]
但 \(o(x)\) 除以 \(x^3\) 后未必趋于零。例如，\(x^3\) 本身就是 \(o(x)\)，除以 \(x^3\) 却等于 \(1\)。所以，一阶信息不足以确定这个极限。

分母是 \(x^3\)，我们需要把分子确定到三次项，并使余项除以 \(x^3\) 后趋于零。使用已知展开：
\[
\sin x=x-\frac{x^3}{6}+o(x^3),\qquad
\tan x=x+\frac{x^3}{3}+o(x^3).
\]
相减得到
\[
\tan x-\sin x
=\left(\frac13+\frac16\right)x^3+o(x^3)
=\frac{x^3}{2}+o(x^3),
\]
于是
\[
L_2=\frac12.
\]
这里保留到三次项就够了，因为相减后三次项系数非零；若它也抵消，就需要继续寻找更高阶的首个非零项。

本题还可以先用恒等式，把减法改写成乘除：
\[
\frac{\tan x-\sin x}{x^3}
=\frac{\sin x}{x}\,
\frac{1-\cos x}{x^2}\,
\frac1{\cos x}
\longrightarrow
1\cdot\frac12\cdot1=\frac12.
\]
取 \(0<|x|\) 足够小时，各分母均非零。此时等价替换作用于整体因子，便可以分别使用 \(\sin x\sim x\)、\(1-\cos x\sim x^2/2\)。

因此，选方法时先看结构：整体乘除中的等价因子可以替换；加减中的各项则要先检查抵消。泰勒法通过保留足够阶数控制误差，恒等变形则可能直接显露决定极限的因子。不能把“一阶项相同”理解为“作差后可以忽略”。
````

### D: Combined

[Original output JSON](../../evaluations/outputs/math-method-D-r1.json); primary anonymous text ID `Tbdd62cf5bf42` in [judgment JSON](../../evaluations/judgments/P9e472b536526.json).

````markdown
判断一阶等价替换是否够用，关键是看：替换误差除以分母后是否趋于零，尤其要留意加减中的抵消。以下均取 \(0<|x|\) 足够小，使所用分母非零。

等价关系 \(\alpha(x)\sim\beta(x)\) 的含义是
\[
\frac{\alpha(x)}{\beta(x)}\to1.
\]
因此，\(\sin x\sim x\) 直接给出
\[
L_1=\lim_{x\to0}\frac{\sin x}{x}=1.
\]
也可以从误差看：\(\sin x=x+o(x)\)，其中 \(o(x)\) 表示除以 \(x\) 后趋于零的余项。于是
\[
\frac{\sin x}{x}=1+\frac{o(x)}x\to1.
\]
这里分母就是 \(x\)，一阶近似的误差已足够小，无需展开更多项。

对第二个极限，若把 \(\tan x\) 和 \(\sin x\) 分别换成 \(x\)，分子就成了 \(x-x=0\)。这不能推出极限为零，因为被舍去的误差可能正是决定结果的部分。一阶等价只告诉我们
\[
\tan x=x+o(x),\qquad \sin x=x+o(x),
\]
所以两者之差是 \(o(x)\)。但 \(o(x)\) 除以 \(x^3\) 未必趋于零：例如 \(x^3=o(x)\)，而 \(x^3/x^3=1\)。因此，一阶信息不足以确定 \(L_2\)。

选择泰勒展开时，要让相减后保留的项能够确定分子与 \(x^3\) 的比例，同时让余项除以 \(x^3\) 后趋于零。利用
\[
\sin x=x-\frac{x^3}{6}+o(x^3),\qquad
\tan x=x+\frac{x^3}{3}+o(x^3),
\]
相减得
\[
\tan x-\sin x
=\left(\frac13+\frac16\right)x^3+o(x^3)
=\frac12x^3+o(x^3).
\]
两个 \(o(x^3)\) 之差仍是 \(o(x^3)\)，因而
\[
L_2=\lim_{x\to0}\left(\frac12+\frac{o(x^3)}{x^3}\right)=\frac12.
\]
这里保留到三次项已经足够，因为三次项系数非零，且余项满足所需条件。

本题还可先用恒等式消除作差结构：
\[
\tan x-\sin x
=\frac{\sin x(1-\cos x)}{\cos x},
\]
于是
\[
\frac{\tan x-\sin x}{x^3}
=\frac{\sin x}{x}\cdot\frac{1-\cos x}{x^2}\cdot\frac1{\cos x}
\longrightarrow1\cdot\frac12\cdot1=\frac12.
\]
这里分别用了 \(\sin x\sim x\)、\(1-\cos x\sim x^2/2\) 和 \(\cos x\to1\)；最后一个关系也保证附近的 \(\cos x\) 非零。

方法的边界是：等价替换适用于整体乘除因子，不能仅凭各项等价就逐项替换后作差。加减中若主项抵消，应继续寻找首个非零项，并核实余项相对于分母足够小；若能先恒等变形为乘除结构，也可直接使用等价关系。本题的三次展开足够，但不能据此认为所有相减的极限都只需保留到三次项。
````
