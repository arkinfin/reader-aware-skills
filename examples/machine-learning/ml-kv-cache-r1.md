# KV cache: different details without a rated advantage

This is a fixed example chosen before scoring. Both outputs received overall comprehensibility 5/5 and no primary technical error flags; the A/C comparison was a tie.

Both connect causal masking to unchanged past hidden states and reusable per-layer keys and values. C explicitly anchors the induction in the first layer and defines the cache-storage dimensions. A additionally distinguishes per-step attention work from cumulative attention work. The primary judge noted these differences but found no overall comprehensibility advantage. The explanation concerns the stated fixed-parameter causal inference setting, not measured inference performance.

Task `ml-kv-cache`, repetition `1`. Generation and primary judging used GPT-6.1 Sol at medium reasoning effort. These are text ratings, not evidence of human learning or transfer. The Chinese outputs are reproduced in full without editing.

Sources: [task packet](../../evaluations/tasks/ml-kv-cache.json), [primary anonymous judgment](../../evaluations/judgments/Pd055d4bf9d38.json), [complete descriptive results](../../evaluations/summary.json).

| Condition | Overall comprehensibility | Primary correctness | Primary minor flags | Output length (characters) |
| --- | ---: | ---: | ---: | ---: |

| A | 5 | 5 | 0 | 1106 |

| C | 5 | 5 | 0 | 1188 |


Character counts include notation and markup. Length differences alone do not establish quality or efficiency.

## Original outputs

### A: Baseline

[Original output JSON](../../evaluations/outputs/ml-kv-cache-A-r1.json); primary anonymous text ID `T3482cb51e27e` in [judgment JSON](../../evaluations/judgments/Pd055d4bf9d38.json).

````markdown
语言模型逐 token 生成时，每一步都要利用已有上下文。KV cache 的作用，是保存过去位置在各层产生的 key（键）和 value（值），使下一步无需重新计算它们。这里讨论参数固定、关闭 dropout 的标准 decoder 自注意力推理；已有 token 的位置和上下文保持不变，缓存精确保存原值。

先看单层、单头。位置 \(i\) 的输入隐向量 \(h_i\) 经过三个投影：

\[
q_i=h_iW_Q,\qquad k_i=h_iW_K,\qquad v_i=h_iW_V.
\]

query 表示当前位置用于匹配的信息，key 用于计算匹配分数，value 则提供被汇总的内容。因果掩码只允许位置 \(t\) 访问自身及之前的位置，因此其注意力输出为：

\[
a_{t,i}=
\frac{\exp(q_tk_i^\top/\sqrt{d_k})}
{\sum_{j=1}^{t}\exp(q_tk_j^\top/\sqrt{d_k})},
\qquad
o_t=\sum_{i=1}^{t}a_{t,i}v_i.
\]

过去的 KV 为什么可以复用？关键在于因果依赖：过去位置看不到后来追加的 token，所以追加内容不会改变它原来的注意力输出。逐层来看，只要已有位置的输入不变，该层输出就不变，下一层的输入也不变。因此，在上述条件下，过去位置在各层的隐状态及其 K、V 都保持不变，可以直接使用缓存中的结果。

处理新位置时，每一层只需为当前位置计算新的 \(q_t,k_t,v_t\)，将 \(k_t,v_t\) 追加到该层缓存，再让 \(q_t\) 与截至当前位置的全部 key 计算分数，经过 softmax 后，对全部对应的 value 加权求和。过去的 query 无需参与当前输出的计算，因此通常不缓存；过去的注意力权重也不能直接复用，因为新的 query 会产生新的分数和权重。

相比每次把整个前缀重新做一遍前向计算，KV cache 省去了过去位置重复的 K、V 投影，以及为重新得到这些位置隐状态而进行的前向计算。不过，新位置仍需完成自身各层的计算，并读取全部历史 KV。在维度固定时，当前一步的注意力计算量仍随上下文长度线性增长；生成一段长序列时，各步注意力计算的总量仍呈二次增长。

代价是额外存储。单层单头保存 \(t\) 个位置，需要的 KV 元素数为：

\[
t(d_k+d_v).
\]

多层、多头时需汇总各层各头的缓存，所以存储量随上下文长度增长。KV cache 本质上是用空间换取较少的重复计算；它属于本次推理的状态，并不更新模型参数。
````

### C: Readability-only

[Original output JSON](../../evaluations/outputs/ml-kv-cache-C-r1.json); primary anonymous text ID `Tf5be20f1a7c3` in [judgment JSON](../../evaluations/judgments/Pd055d4bf9d38.json).

````markdown
KV cache是在逐token生成时，按层保存过去位置的key和value，供后续位置复用的推理状态。它利用了因果自注意力的一个性质：追加新token，不会改变过去位置已经算出的结果。这里讨论参数固定、关闭dropout，且已有token、位置及此前上下文都不改动的标准decoder推理，缓存精确保存原值。

先看单层单头。位置 \(i\) 的输入隐向量 \(h_i\) 经三次线性变换，得到query、key和value：

\[
q_i=h_iW_Q,\qquad k_i=h_iW_K,\qquad v_i=h_iW_V。
\]

query用于与各位置的key计算匹配分数，value则是被加权汇总的内容。因果掩码禁止位置 \(t\) 访问未来，因此它只能使用位置 \(1\) 到 \(t\)：

\[
a_{t,i}=
\frac{\exp(q_t\cdot k_i/\sqrt{d_k})}
{\sum_{j=1}^{t}\exp(q_t\cdot k_j/\sqrt{d_k})},
\qquad
o_t=\sum_{i=1}^{t}a_{t,i}v_i。
\]

为什么过去的KV能复用？在第一层，旧token及其位置没变，输入就没变；旧位置又无法关注后来追加的token，所以其注意力输出也没变。这个结论逐层成立：上一层的旧位置输出不变，下一层对应的输入、key和value也就不变。因而，新token到来时，无须重新计算旧位置的这些结果。

具体而言，每层先用当前位置的输入计算 \(q_t,k_t,v_t\)，把 \(k_t,v_t\) 追加到该层缓存，再用 \(q_t\) 与缓存中的全部key计算分数，经softmax得到权重，最后汇总全部对应value。各层分别维护缓存，因为同一位置在不同层的隐状态和投影参数不同。

节省的计算来自避免重复处理旧位置。如果每一步都对整个已有序列重新前向计算，就会反复计算旧位置的投影、注意力输出以及其他层内运算。使用缓存后，每层只需推进当前位置；过去的query也不必保留，因为生成当前输出只需要当前query。

但缓存不能省掉当前query对所有已有key的匹配，也不能省掉softmax和对全部value的加权。当前query通常与过去query不同，因此过去的注意力权重不能直接复用。序列越长，当前这一步仍需读取和处理越多KV；在维数固定时，这部分注意力计算量随已有长度线性增长。

代价是额外存储。单层单头缓存 \(t\) 个位置，需要保存的元素数为：

\[
t(d_k+d_v),
\]

其中 \(d_k,d_v\) 分别是key和value的维数；多层多头还要累计各层各头的缓存。因此，KV cache以随序列增长的存储，换取对历史计算结果的复用。它属于一次推理的状态，不涉及模型参数更新。
````
