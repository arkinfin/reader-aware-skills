# State space and transfer functions: a local preference

This example was selected after scoring because it is the only A/C pair with a primary preference for C across the 21 A/C comparisons. It is not one of the three fixed examples. A received overall comprehensibility 4/5; C received 5/5. This selected local preference must not be read as an aggregate treatment benefit.

C explains the roles of the state-space matrices and explicitly states the initial-condition requirement in the hidden-mode example. A says that only a zero initial state gives Y(s)=G(s)U(s); that is too strong. The initial-state output term can vanish even for a nonzero state, as it does for the example's unobservable second state. The primary judge flagged this as minor, and separate technical adjudication accepted that local flag. The zero-state definition of a transfer function and the main derivation remain intact. The original wording below is preserved, not silently corrected.

Task `control-state-transfer`, repetition `3`. Generation and primary judging used GPT-6.1 Sol at medium reasoning effort. These are text ratings, not evidence of human learning or transfer. The Chinese outputs are reproduced in full without editing.

Sources: [task packet](../../evaluations/tasks/control-state-transfer.json), [primary anonymous judgment](../../evaluations/judgments/P00dbd37432b3.json), [complete descriptive results](../../evaluations/summary.json).

Separate technical review: [technical adjudication](../../evaluations/technical-adjudication.json). Its verdicts are distinct from the primary ratings.

| Condition | Overall comprehensibility | Primary correctness | Primary minor flags | Output length (characters) |
| --- | ---: | ---: | ---: | ---: |

| A | 4 | 4 | 1 | 1285 |

| C | 5 | 5 | 0 | 1364 |


Character counts include notation and markup. Length differences alone do not establish quality or efficiency.

## Primary technical flag, unchanged

```json
[
  {
    "severity": "minor",
    "quote": "只有在 \\(x_0=0\\) 时，才直接得到",
    "reason": "将零初始状态说成输出满足Y(s)=G(s)U(s)的必要条件，表述过强。实际只需初值对应的输出项为零；本例中即使x2(0)非零，只要x1(0)=0，该关系仍成立。这不影响传递函数按零初始状态定义的核心结论。"
  }
]
```

## Original outputs

### A: Baseline

[Original output JSON](../../evaluations/outputs/control-state-transfer-A-r3.json); primary anonymous text ID `T8e8b81adba16` in [judgment JSON](../../evaluations/judgments/P00dbd37432b3.json).

````markdown
状态空间与传递函数描述同一个系统，但关注的层面不同。状态空间描述“内部状态怎样演化，以及怎样形成输出”；传递函数描述“零初始状态下，输入怎样影响输出”。两者可以联系起来，却不能无条件互相替代。

连续时间有限维线性时不变系统的状态空间形式为
\[
\dot x=Ax+Bu,\qquad y=Cx+Du,\qquad x(0)=x_0。
\]
这里，状态 \(x\) 是预测系统后续演化所需的内部信息。给定初始状态和此后的输入，状态方程决定状态轨迹，输出方程再决定输出。因此，即使输入为零，非零初值仍可能引起系统运动。

对状态方程作拉普拉斯变换，有
\[
(sI-A)X(s)=x_0+BU(s)。
\]
在逆矩阵存在处，代入输出方程可得
\[
Y(s)=\underbrace{\left[C(sI-A)^{-1}B+D\right]}_{G(s)}U(s)
+C(sI-A)^{-1}x_0。
\]
这个式子将输出分成输入引起的响应和初始状态引起的响应。只有在 \(x_0=0\) 时，才直接得到
\[
Y(s)=G(s)U(s)。
\]
所以，传递函数刻画的是零状态输入—输出关系；初值项不包含在其中，不能仅凭传递函数确定任意初值下的响应。

考虑下面的两状态系统：
\[
A=\begin{bmatrix}-1&0\\0&1\end{bmatrix},\quad
B=\begin{bmatrix}1\\0\end{bmatrix},\quad
C=\begin{bmatrix}1&0\end{bmatrix},\quad D=0。
\]
也就是
\[
\dot x_1=-x_1+u,\qquad \dot x_2=x_2,\qquad y=x_1。
\]
输入只作用于 \(x_1\)，输出也只读取 \(x_1\)，因此
\[
G(s)=
\begin{bmatrix}1&0\end{bmatrix}
\begin{bmatrix}(s+1)^{-1}&0\\0&(s-1)^{-1}\end{bmatrix}
\begin{bmatrix}1\\0\end{bmatrix}
=\frac1{s+1}。
\]
从传递函数看，它具有稳定一阶系统的输入—输出表现。然而，当 \(u=0\)、\(x_2(0)\ne0\) 时，
\[
x_2(t)=e^t x_2(0)，
\]
内部状态仍会指数增长。这个动态既不能由输入激发，也不能从输出中观察到，所以没有出现在传递函数中。由此可见，零状态输入—输出稳定，并不保证所有内部状态都随时间衰减。

还要区分“状态坐标不同”和“内部动态遗漏”。作可逆变换 \(z=T^{-1}x\)，有
\[
A_z=T^{-1}AT,\quad B_z=T^{-1}B,\quad C_z=CT,\quad D_z=D。
\]
新旧状态空间只是用不同坐标描述相同动态，传递函数保持不变。这说明状态空间表示并不唯一；但上例中，传递函数未呈现第二个状态的动态，并非坐标选择造成的。判断系统内部行为时，仍需考察状态方程及其初始条件。
````

### C: Readability-only

[Original output JSON](../../evaluations/outputs/control-state-transfer-C-r3.json); primary anonymous text ID `T997ef7df8bf6` in [judgment JSON](../../evaluations/judgments/P00dbd37432b3.json).

````markdown
状态空间与传递函数可以描述同一个线性时不变系统，但保留的信息不同。状态空间描述内部状态怎样随输入和初值演化；传递函数描述零初始状态下，输入怎样影响输出。因此，输出响应看起来稳定，并不保证所有内部状态都稳定。

连续时间有限维线性时不变系统的状态空间形式为
\[
\dot x=Ax+Bu,\qquad y=Cx+Du,\qquad x(0)=x_0。
\]
其中，\(x\)是状态向量，\(u\)是输入，\(y\)是输出。给定输入和初值，就能由状态方程求出状态轨迹，再由输出方程得到输出。矩阵\(A\)描述状态自身的演化及相互作用，\(B\)描述输入如何作用于状态，\(C\)决定哪些状态组合进入输出，\(D\)表示输入对输出的直接作用。

两种表示的联系，可以从熟悉的拉普拉斯变换得到。利用导数的变换公式，
\[
sX(s)-x_0=AX(s)+BU(s),
\]
所以，在\(sI-A\)可逆处，
\[
Y(s)=\underbrace{\left[C(sI-A)^{-1}B+D\right]U(s)}_{\text{零初始状态下的输入响应}}
+\underbrace{C(sI-A)^{-1}x_0}_{\text{初始状态引起的响应}}。
\]
令\(x_0=0\)，便得到传递函数
\[
G(s)=C(sI-A)^{-1}B+D。
\]
这说明，传递函数提取的是输入到输出的关系；初始状态引起的响应需要另行计算，不能直接包含在\(G(s)U(s)\)中。

考虑两状态系统
\[
A=\begin{pmatrix}-1&0\\0&1\end{pmatrix},\quad
B=\begin{pmatrix}1\\0\end{pmatrix},\quad
C=\begin{pmatrix}1&0\end{pmatrix},\quad D=0，
\]
也就是
\[
\dot x_1=-x_1+u,\qquad \dot x_2=x_2,\qquad y=x_1。
\]
输入只作用于\(x_1\)，输出也只读取\(x_1\)，故
\[
G(s)=
\begin{pmatrix}1&0\end{pmatrix}
\begin{pmatrix}(s+1)^{-1}&0\\0&(s-1)^{-1}\end{pmatrix}
\begin{pmatrix}1\\0\end{pmatrix}
=\frac1{s+1}。
\]
它与稳定的一阶系统具有相同的零状态输入输出关系。然而，当\(u=0\)且\(x_2(0)\ne0\)时，
\[
x_2(t)=e^t x_2(0)，
\]
内部状态会无限增长。若同时\(x_1(0)=0\)，输出却始终为零。原因是第二个状态既不受输入驱动，也不影响输出，它的增长不会出现在传递函数中。因此，仅凭这里的传递函数，无法判断整个内部系统是否稳定。

此外，状态变量的选法也不唯一。作可逆变换\(z=T^{-1}x\)，有
\[
A_z=T^{-1}AT,\quad B_z=T^{-1}B,\quad C_z=CT,\quad D_z=D。
\]
这些矩阵仍给出相同的零状态传递函数。坐标变换只是换一种方式记录状态；本例中遗漏第二个状态，则说明输入输出关系本身未必呈现全部内部动态。
````
