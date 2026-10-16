# Gain crossover and phase margin: a tied comparison

This is a fixed example chosen before scoring. Both outputs received overall comprehensibility 5/5 and no primary technical error flags; the A/C comparison was a tie. It is also the case selected by the preregistered weakest-A/C rule: minimum C−A overall score, then task ID, then repeat. The minimum was zero, shared by many pairs. This is not a uniquely bad treatment example.

Both explain that phase margin is evaluated at a crossover frequency that moves when gain changes. A emphasizes moving the phase-reading location along an unchanged curve. C adds an explicit crossover formula and notes that the old frequency now has gain above one. Both include numerical comparisons, distinguish reduced margin from instability, and restrict the direction-of-change claim to the stated system. The primary judge found neither organization sufficiently better to select a winner.

Task `control-crossover`, repetition `1`. Generation and primary judging used GPT-6.1 Sol at medium reasoning effort. These are text ratings, not evidence of human learning or transfer. The Chinese outputs are reproduced in full without editing.

Sources: [task packet](../../evaluations/tasks/control-crossover.json), [primary anonymous judgment](../../evaluations/judgments/Pc587fc356541.json), [complete descriptive results](../../evaluations/summary.json).

| Condition | Overall comprehensibility | Primary correctness | Primary minor flags | Output length (characters) |
| --- | ---: | ---: | ---: | ---: |

| A | 5 | 5 | 0 | 1294 |

| C | 5 | 5 | 0 | 1305 |


Character counts include notation and markup. Length differences alone do not establish quality or efficiency.

## Original outputs

### A: Baseline

[Original output JSON](../../evaluations/outputs/control-crossover-A-r1.json); primary anonymous text ID `T021e88cfd97f` in [judgment JSON](../../evaluations/judgments/Pc587fc356541.json).

````markdown
正比例增益不改变各个固定频率上的开环相位，却能改变相位裕度，关键在于：**相位裕度取的是增益截止频率处的相位，而截止频率本身会随增益移动。** 因此，“某个频率上的相位不变”与“相位裕度不变”是两件不同的事。

对于连续时间、单输入单输出、单位负反馈系统

\[
L(s)=\frac{K}{s(s+1)},\qquad K>0,
\]

在任意固定的正频率上，有

\[
|L(j\omega)|=\frac{K}{\omega\sqrt{1+\omega^2}},
\qquad
\arg L(j\omega)=-90^\circ-\arctan\omega.
\]

正实数 \(K\) 的幅角为零，所以调整它只改变幅值，不改变该频率处的相位。在Bode图上，增大 \(K\) 会使幅频曲线整体上移，相频曲线则保持原样。

但相位裕度并不是在任意指定频率处测量的。必须先找到幅值等于1，即幅频曲线穿过 \(0\,\mathrm{dB}\) 的增益截止频率，再读取那里的相位：

\[
|L(j\omega_c)|=1
\quad\Longleftrightarrow\quad
K=\omega_c\sqrt{1+\omega_c^2},
\]

\[
PM=180^\circ+\arg L(j\omega_c)
=90^\circ-\arctan\omega_c.
\]

本系统中，\(\omega\sqrt{1+\omega^2}\) 随正频率严格增大，所以截止频率唯一，并且 \(K\) 越大，\(\omega_c\) 越高。与此同时，相频曲线随频率升高而下降。因此，增大增益后，读取相位的位置向右移动，读到的相位更负，与 \(-180^\circ\) 的距离更小，相位裕度便减小了。

两组参数可以直接比较。当 \(K=\sqrt2\) 时，

\[
\omega_c=1,\qquad
\arg L(j\omega_c)=-135^\circ,\qquad PM=45^\circ.
\]

当 \(K=\sqrt{20}\) 时，

\[
\omega_c=2,\qquad
\arg L(j\omega_c)
=-90^\circ-\arctan2\approx-153.43^\circ,
\qquad PM\approx26.57^\circ.
\]

例如在固定频率 \(\omega=1\) 处，两种增益下的相位仍然都是 \(-135^\circ\)；只是第二种增益下，这里已不是截止频率，不能再用这里的相位计算相位裕度。

还要区分“裕度减小”和“闭环失稳”。本系统闭环特征多项式为

\[
s^2+s+K.
\]

对所有 \(K>0\)，其根的实部均为负，闭环都稳定。因此，上述比较说明相位裕度减小，并不表示第二个系统已经失稳。

这种变化方向依赖于本系统幅值随频率单调下降、相位也随频率下降的特点。对其他系统，幅频曲线可能不单调，还可能存在多个截止频率，不能无条件断言增大正增益必然使截止频率升高、相位裕度减小；应重新确定截止位置，并检查相应相位。
````

### C: Readability-only

[Original output JSON](../../evaluations/outputs/control-crossover-C-r1.json); primary anonymous text ID `T69224ec2d520` in [judgment JSON](../../evaluations/judgments/Pc587fc356541.json).

````markdown
正比例增益不改变固定频率处的开环相位，却能改变相位裕度，关键在于：**相位裕度取的是增益截止频率处的相位，而这个频率会随增益移动。**

对单位负反馈系统
\[
L(s)=\frac{K}{s(s+1)},\qquad K>0,
\]
在任意固定的正频率处，有
\[
|L(j\omega)|=\frac{K}{\omega\sqrt{1+\omega^2}},
\qquad
\arg L(j\omega)=-90^\circ-\arctan\omega.
\]
正实数 \(K\) 的幅角为零，因此增大 \(K\) 只会放大开环幅值，不会改变该频率处的相位。在 Bode 图上，幅频曲线整体上移，相频曲线保持原样。

但相位裕度并不是在某个预先固定的频率处测量的。首先要找到幅值等于 1，即幅频曲线穿过 \(0\,\mathrm{dB}\) 的增益截止频率 \(\omega_c\)，再读取那里距离 \(-180^\circ\) 还有多少相位余量：
\[
\mathrm{PM}=180^\circ+\arg L(j\omega_c)
=90^\circ-\arctan\omega_c.
\]
所以，即使相频曲线没变，只要读取相位的位置变了，相位裕度就可能改变。

本系统的截止条件为
\[
\omega_c\sqrt{1+\omega_c^2}=K,
\]
也可写成
\[
\omega_c^2=\frac{\sqrt{1+4K^2}-1}{2}.
\]
对正频率，左侧的 \(\omega\sqrt{1+\omega^2}\) 严格递增，因此截止频率唯一，而且 \(K\) 越大，\(\omega_c\) 越高。与此同时，相位随频率升高而变得更负，因此相位裕度减小。

具体比较两个增益。当 \(K=\sqrt2\) 时，
\[
\omega_c=1,\qquad
\arg L(j\omega_c)=-135^\circ,\qquad
\mathrm{PM}=45^\circ.
\]
当 \(K=\sqrt{20}\) 时，
\[
\omega_c=2,\qquad
\arg L(j\omega_c)=-90^\circ-\arctan2
\approx-153.43^\circ,
\]
\[
\mathrm{PM}\approx26.57^\circ.
\]
例如，在固定频率 \(\omega=1\) 处，两种增益的相位始终都是 \(-135^\circ\)；只是第二种增益下，该频率处的幅值已超过 1，不能再用这里的相位计算相位裕度。新的截止点移到了 \(\omega=2\)。

相位裕度减小也不等于闭环已经失稳。本系统闭环特征多项式为
\[
s^2+s+K.
\]
对所有 \(K>0\)，其根的实部均为负，闭环仍然稳定。

上述“增益增大、截止频率升高、相位裕度减小”的联系，依赖本系统幅值随频率严格下降、相位也随频率下降的性质。对其他系统，正增益仍不改变固定频率处的相位，但幅频曲线可能不单调，甚至存在多个截止频率，因此必须重新确定截止点及其相位，不能无条件照搬这里的变化结论。
````
