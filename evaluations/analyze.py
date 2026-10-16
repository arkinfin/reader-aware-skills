#!/usr/bin/env python3
"""Analyze the complete frozen experiment; stop before deblinding incomplete data.

Standard library only. This script never changes inputs, outputs or judgments.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import sys

DIMENSIONS = ('correctness', 'prior_knowledge_alignment', 'conceptual_sequencing',
              'motivation', 'explanatory_coherence', 'cognitive_load',
              'transfer_support', 'overall_comprehensibility')
COMPARISONS = (('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'))
FIXED_EXAMPLES = ('math-concept', 'control-crossover', 'ml-kv-cache')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def files(directory, suffix):
    return {p.stem: p for p in directory.glob('*' + suffix)}


def safe_path(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), 'Hash path escapes root')
    return path


def verify_hashes(root, hashes):
    require(isinstance(hashes, dict) and hashes, 'Missing frozen hashes')
    for relative, expected in hashes.items():
        require(sha(safe_path(root, relative)) == expected, 'Frozen hash mismatch: ' + relative)


def validate_judgment(data, packet):
    require(set(data) == {'texts', 'pairs'}, 'Unexpected judgment schema')
    texts = {t['id']: t['text'] for t in packet['texts']}
    require(len(texts) == len(packet['texts']), 'Duplicate packet alias')
    ids = [t['id'] for t in data['texts']]
    require(len(ids) == len(set(ids)) and set(ids) == set(texts), 'Judgment text IDs mismatch')
    for item in data['texts']:
        require(set(item['scores']) == set(DIMENSIONS), 'Score dimensions mismatch')
        require(all(type(v) is int and 1 <= v <= 5 for v in item['scores'].values()), 'Invalid score')
        require(len(item['evidence']) >= 2, 'Insufficient evidence')
        for evidence in item['evidence'] + item['errors']:
            require(isinstance(evidence['quote'], str) and evidence['quote'] and
                    evidence['quote'] in texts[item['id']], 'Invalid verbatim evidence')
            require(isinstance(evidence['reason'], str) and evidence['reason'].strip(), 'Missing evidence reason')
        require(all(e['severity'] in ('major', 'minor') for e in item['errors']), 'Invalid error severity')
        require(all(e['dimension'] in DIMENSIONS for e in item['evidence']), 'Invalid evidence dimension')
        redundancy = item['redundancy']
        require(type(redundancy['score']) is int and 1 <= redundancy['score'] <= 5, 'Invalid redundancy score')
        require(isinstance(redundancy['reason'], str) and redundancy['reason'].strip(), 'Missing redundancy reason')
        require(isinstance(redundancy['quote'], str) and
                (not redundancy['quote'] or redundancy['quote'] in texts[item['id']]), 'Invalid redundancy quote')
        require(redundancy['score'] == 1 or bool(redundancy['quote'].strip()),
                'Redundancy above 1 requires a nonempty verbatim quote')
    expected = [(p['left'], p['right']) for p in packet['pairs']]
    actual = [(p['left'], p['right']) for p in data['pairs']]
    require(len(expected) == len(set(expected)) and len(actual) == len(set(actual)) and
            set(actual) == set(expected), 'Pair IDs mismatch or duplicated')
    for pair in data['pairs']:
        require(pair['winner'] in ('left', 'right', 'tie'), 'Invalid pair winner')
        for side in ('left', 'right'):
            quote = pair[side + '_quote']
            require(isinstance(quote, str) and quote and quote in texts[pair[side]], 'Invalid pair quote')
        require(isinstance(pair['reason'], str) and pair['reason'].strip(), 'Missing comparison reason')


def usage_totals(records):
    totals = defaultdict(float)
    reported = 0
    def collect(value, prefix=''):
        if isinstance(value, dict):
            for key, sub in value.items():
                collect(sub, prefix + '.' + key if prefix else key)
        elif finite(value):
            require(value >= 0, 'Negative usage value')
            totals[prefix] += value
    for record in records:
        usage = record.get('usage')
        if isinstance(usage, dict) and usage:
            reported += 1
            collect(usage)
    return {'calls': len(records), 'calls_with_nonempty_usage': reported,
            'reported_field_sums': dict(sorted(totals.items())),
            'interpretation': 'Reported fields retain their names; nested/cached fields may overlap. No billing estimate.'}


def validate_successful_attempt(run, key, record, cell):
    number = record['attempt']
    require(type(number) is int and 1 <= number <= 2, 'Invalid output attempt number')
    attempt = read(run/'attempts'/key/f'{number:02d}.json')
    require(attempt['key'] == key and attempt['attempt'] == number and
            attempt['status'] == 'completed', 'Output does not reference its successful attempt')
    expected = {**cell, **{k: v for k, v in attempt.items() if k != 'transport'}}
    require(record == expected, 'Output text or metadata differs from successful attempt: ' + key)


def validate_judge_attempt(run, key, record):
    metadata = record['metadata']
    number = metadata['attempt']
    require(type(number) is int and 1 <= number <= 2, 'Invalid judge attempt number')
    attempt = read(run/'attempts'/key/f'{number:02d}.json')
    require(attempt['key'] == key and attempt['attempt'] == number and
            attempt['status'] == 'completed', 'Judgment does not reference its successful attempt')
    expected = {k: v for k, v in attempt.items() if k not in ('transport', 'text')}
    require(metadata == expected, 'Judgment metadata differs from successful attempt: ' + key)
    raw = attempt['text'].strip()
    if raw.startswith('```'):
        raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw)
    parsed = json.loads(raw, object_pairs_hook=unique_object)
    require(parsed == record['judgment'], 'Judgment differs from raw successful response: ' + key)


def validate_infrastructure_amendment(root, run, manifest):
    amendment = manifest.get('infrastructure_amendment')
    if amendment is None:
        return
    original_path = safe_path(run, amendment['original_manifest_path'])
    generation_runner = safe_path(run, amendment['generation_runner_path'])
    require(sha(original_path) == amendment['original_manifest_sha256'], 'Original manifest hash mismatch')
    require(sha(generation_runner) == amendment['generation_runner_sha256'], 'Original generation runner hash mismatch')
    original = read(original_path)
    require('infrastructure_amendment' not in original, 'Nested infrastructure amendments are unsupported')
    require({k: v for k, v in original.items() if k != 'input_hashes'} ==
            {k: v for k, v in manifest.items() if k not in ('input_hashes', 'infrastructure_amendment')},
            'Amendment changed generation cells, config or other manifest fields')
    runner_key = 'evaluations/run.py'
    require({k: v for k, v in original['input_hashes'].items() if k != runner_key} ==
            {k: v for k, v in manifest['input_hashes'].items() if k != runner_key},
            'Amendment changed non-runner input hashes')
    require(original['input_hashes'][runner_key] == amendment['generation_runner_sha256'],
            'Generation runner differs from original frozen runner')
    require(manifest['input_hashes'][runner_key] == amendment['evaluation_runner_sha256'] == sha(root/runner_key),
            'Evaluation runner hash mismatch')
    require(isinstance(amendment['reason'], str) and amendment['reason'].strip() and
            isinstance(amendment['applied_utc'], str) and amendment['applied_utc'].strip(),
            'Amendment must disclose its reason and time')


def aggregate(rows):
    require(rows, 'Empty aggregation')
    result = {'n': len(rows), 'score_means': {d: statistics.mean(r['scores'][d] for r in rows) for d in DIMENSIONS}}
    for field in ('redundancy', 'chars', 'han_chars', 'elapsed_seconds'):
        values = [r[field] for r in rows]
        result[field] = {'mean': statistics.mean(values), 'min': min(values), 'max': max(values), 'sum': sum(values)}
    result['judge_flagged_errors'] = {s: sum(r['errors'][s] for r in rows) for s in ('major', 'minor')}
    result['texts_with_major_flags'] = sum(r['errors']['major'] > 0 for r in rows)
    return result


def factorial(rows):
    groups = {g: aggregate([r for r in rows if r['group'] == g]) for g in 'ABCD'}
    contrasts = {}
    for dimension in DIMENSIONS:
        a, b, c, d = (groups[g]['score_means'][dimension] for g in 'ABCD')
        contrasts[dimension] = {'delta_R': ((b-a)+(d-c))/2, 'delta_C': ((c-a)+(d-b))/2,
                                'interaction': d-b-c+a}
    return {'groups': groups, 'contrasts': contrasts}


def cross_contrast(rows):
    groups = {g: aggregate([r for r in rows if r['group'] == g]) for g in 'AC'}
    return {'groups': groups, 'C_minus_A': {d: groups['C']['score_means'][d]-groups['A']['score_means'][d] for d in DIMENSIONS}}


def analyze(root, evidence_dir=None):
    root = Path(root)
    ev = root/'evaluations'
    private_run = root/'.workflow/experiment-v1'
    run = (Path(evidence_dir) if evidence_dir is not None else
           private_run if private_run.exists() else ev/'records')
    manifest = read(run/'manifest.json')
    verify_hashes(root, manifest['input_hashes'])
    validate_infrastructure_amendment(root, run, manifest)
    protocol = read(ev/'protocol.json')
    require(protocol['input_hashes'] == manifest['input_hashes'] and protocol['seed'] == manifest['seed'], 'Protocol differs from manifest')
    cells = manifest['cells']
    require(len(cells) == 60 and len({c['id'] for c in cells}) == 60, 'Need 60 unique manifest cells')
    cell_index = {c['id']: c for c in cells}
    task_files = files(ev/'tasks', '.json')
    tasks = {key: read(path) for key, path in task_files.items()}
    require(len(tasks) == 7 and sum(t['domain'] == 'mathematics' for t in tasks.values()) == 3, 'Task design mismatch')
    require(Counter(t['domain'] for t in tasks.values()) == {'mathematics': 3, 'control-theory': 2, 'machine-learning': 2}, 'Domain design mismatch')
    expected_cells = {(task, g, rep) for task,t in tasks.items() for g in ('ABCD' if t['domain']=='mathematics' else 'AC') for rep in (1,2,3)}
    require({(c['task'],c['group'],c['repeat']) for c in cells} == expected_cells, 'Unbalanced manifest')
    output_files, judgment_files = files(ev/'outputs', '.json'), files(ev/'judgments', '.json')
    order = read(run/'judge-order.json')
    require(len(order) == 21 and len(set(order)) == 21, 'Need 21 unique judgment packets')
    require(set(output_files) == set(cell_index), 'Missing or unexpected outputs; do not deblind')
    require(set(judgment_files) == set(order), 'Missing or unexpected judgments; do not deblind')
    packet_files, prompt_files = files(run/'blind-packets', '.json'), files(run/'judge-prompts', '.txt')
    require(set(packet_files) == set(order) == set(prompt_files), 'Packet/prompt set mismatch')
    freeze = read(run/'blind-freeze.json')
    expected_frozen = {str(p.relative_to(run)) for p in [*packet_files.values(),*prompt_files.values(),run/'blind-map.json',run/'judge-order.json']}
    require(set(freeze['hashes']) == expected_frozen, 'Blind freeze file set mismatch')
    verify_hashes(run, freeze['hashes'])  # Hash bytes only; map remains unparsed.
    outputs = {}
    for key, path in output_files.items():
        record = read(path)
        cell = cell_index[key]
        validate_successful_attempt(run, key, record, cell)
        require(record['status'] == 'completed', 'Incomplete output: ' + key)
        require(all(record[k] == v for k,v in cell.items()), 'Output cell metadata changed: ' + key)
        require(record['key'] == key and record['requested_model'] == manifest['config']['generation_model'] and
                record['reasoning_effort'] == manifest['config']['generation_effort'], 'Generation conditions changed')
        require(record.get('tool_items') == [], 'Output tool protocol violation')
        require(sha(run/'generation-prompts'/f'{key}.txt') == cell['prompt_sha256'], 'Generation prompt changed')
        text = record['text']
        require(isinstance(text, str) and text.strip(), 'Empty generation')
        require(record['chars'] == len(text) and record['han_chars'] == len(re.findall(r'[\u3400-\u9fff]', text)), 'Output lengths changed')
        require(finite(record['elapsed_seconds']) and record['elapsed_seconds'] >= 0, 'Invalid elapsed time')
        outputs[key] = record
    judgments, packets, aliases, blocks = {}, {}, set(), set()
    judge_module = (ev/'prompts/judge.txt').read_text()
    for key in order:
        packet, record = read(packet_files[key]), read(judgment_files[key])
        require(record['id'] == key and record['status'] == 'validated', 'Judgment not validated')
        validate_judge_attempt(run, key, record)
        require(packet['task'] == tasks[packet['task']['id']], 'Packet task differs from frozen input')
        expected_prompt = judge_module+'\n\n'+json.dumps(packet,ensure_ascii=False,indent=2)
        require(prompt_files[key].read_text() == expected_prompt, 'Judge prompt differs from packet')
        metadata = record['metadata']
        require(metadata['status'] == 'completed' and metadata['key'] == key and
                metadata['prompt_sha256'] == hashlib.sha256(expected_prompt.encode()).hexdigest(), 'Judgment metadata mismatch')
        require(metadata['requested_model'] == manifest['config']['judge_model'] and
                metadata['reasoning_effort'] == manifest['config']['judge_effort'], 'Judge conditions changed')
        require(metadata.get('tool_items') == [] and finite(metadata['elapsed_seconds']) and metadata['elapsed_seconds'] >= 0, 'Judge protocol/time mismatch')
        validate_judgment(record['judgment'], packet)
        current = {t['id'] for t in packet['texts']}
        require(not aliases.intersection(current), 'Alias reused across packets')
        aliases.update(current)
        judgments[key], packets[key] = record, packet
    require(len(aliases) == 60, 'Need 60 unique validated anonymous text scores')
    # All 60 outputs and 21 validated judgments have passed before this join.
    mapping = read(run/'blind-map.json')
    require(set(mapping) == aliases and len(set(mapping.values())) == 60 and set(mapping.values()) == set(cell_index), 'Blind mapping is not a bijection')
    rows, pairs = [], []
    for key in order:
        packet, judgment = packets[key], judgments[key]['judgment']
        mapped = [cell_index[mapping[t['id']]] for t in packet['texts']]
        task, rep = mapped[0]['task'], mapped[0]['repeat']
        require(all(c['task'] == task and c['repeat'] == rep for c in mapped), 'Mixed packet block')
        require(packet['task']['id'] == task, 'Packet task mapping mismatch')
        require((task, rep) not in blocks, 'Duplicate task/repetition packet')
        blocks.add((task, rep))
        groups = 'ABCD' if tasks[task]['domain'] == 'mathematics' else 'AC'
        require({c['group'] for c in mapped} == set(groups), 'Incomplete packet groups')
        for item in packet['texts']:
            require(item['text'] == outputs[mapping[item['id']]]['text'], 'Blind text differs from original output')
        expected_pairs = set(COMPARISONS if groups == 'ABCD' else (('A','C'),))
        found = set()
        for pair in judgment['pairs']:
            left, right = (cell_index[mapping[pair[s]]] for s in ('left','right'))
            first, second = sorted((left['group'], right['group']))
            require((first,second) in expected_pairs, 'Unexpected condition comparison')
            found.add((first,second))
            winning_group = 'tie' if pair['winner']=='tie' else (left if pair['winner']=='left' else right)['group']
            pairs.append({'packet':key,'task':task,'domain':tasks[task]['domain'],'repeat':rep,
                          'first':first,'second':second,'winner':winning_group})
        require(found == expected_pairs and len(judgment['pairs']) == len(found), 'Missing/duplicate comparison')
        for item in judgment['texts']:
            output = outputs[mapping[item['id']]]
            rows.append({**cell_index[output['id']], 'packet':key, 'anonymous_id':item['id'],
                         'scores':item['scores'], 'redundancy':item['redundancy']['score'],
                         'errors':{severity:sum(e['severity']==severity for e in item['errors']) for severity in ('major','minor')},
                         **{k:output[k] for k in ('chars','han_chars','elapsed_seconds')}})
    require(len(rows)==60 and len(pairs)==48 and len(blocks)==21, 'Final design count mismatch')
    rows.sort(key=lambda r:(r['task'],r['repeat'],r['group']))
    math_rows = [r for r in rows if r['domain']=='mathematics']
    pair_counts = {}
    for domain in ('mathematics','control-theory','machine-learning'):
        for first,second in COMPARISONS if domain=='mathematics' else (('A','C'),):
            sample = [p for p in pairs if p['domain']==domain and (p['first'],p['second'])==(first,second)]
            pair_counts[f'{domain}:{first}_vs_{second}'] = {'n':len(sample),'first_wins':sum(p['winner']==first for p in sample),
                'ties':sum(p['winner']=='tie' for p in sample),'second_wins':sum(p['winner']==second for p in sample)}
    index = {(r['task'],r['repeat'],r['group']):r for r in rows}
    ac = []
    for task,rep in sorted(blocks):
        a,c = index[task,rep,'A'],index[task,rep,'C']
        ac.append({'task':task,'repeat':rep,'A':a['id'],'C':c['id'],
                   'overall_C_minus_A':c['scores']['overall_comprehensibility']-a['scores']['overall_comprehensibility']})
    weakest = min(ac,key=lambda p:(p['overall_C_minus_A'],p['task'],p['repeat']))
    limitations = ['Exploratory single-model-family study; no population causal or statistical significance claim.',
        'Scores are ordinal. Means and factorial contrasts are descriptive only; within-packet observations are correlated.',
        'LLM judgments may favor model style; quotes establish traceability, not semantic correctness.',
        'Error counts are judge flags pending independent technical adjudication, not accepted findings.',
        'No human learning gain, retention or actual transfer has been measured.',
        'Reported duration is successful-call elapsed time, not total wall-clock or full retry cost; usage sums exclude failed attempts and preflight.',
        'Generation/skill prompt salience, residual shared platform instructions and unexposed backend revision limit generalization.']
    return {'run_id':manifest['run_id'],'infrastructure_amendment':manifest.get('infrastructure_amendment'),
        'generation_config':{k:manifest['config'][k] for k in ('generation_model','generation_effort','judge_model','judge_effort')},
        'integrity':{'status':'pass','outputs':60,'validated_packets':21,'pairs':48,'manifest_sha256':sha(run/'manifest.json'),
                     'blind_freeze_sha256':sha(run/'blind-freeze.json'),'judgment_sha256':{k:sha(p) for k,p in sorted(judgment_files.items())},
                     'output_sha256':{k:sha(p) for k,p in sorted(output_files.items())}},
        'limitations':limitations,'per_text':rows,'mathematics':factorial(math_rows),
        'mathematics_by_task':{task:factorial([r for r in math_rows if r['task']==task]) for task in sorted({r['task'] for r in math_rows})},
        'mathematics_by_repeat':{str(rep):factorial([r for r in math_rows if r['repeat']==rep]) for rep in (1,2,3)},
        'cross_domain':{domain:cross_contrast([r for r in rows if r['domain']==domain]) for domain in ('control-theory','machine-learning')},
        'cross_by_task':{task:cross_contrast([r for r in rows if r['task']==task]) for task,t in sorted(tasks.items()) if t['domain']!='mathematics'},
        'pair_counts':pair_counts,'pairs':pairs,'usage':{'generation_successful_calls':usage_totals(list(outputs.values())),
           'judgment_successful_calls':usage_totals([j['metadata'] for j in judgments.values()])},
        'judge_elapsed_seconds_sum':sum(j['metadata']['elapsed_seconds'] for j in judgments.values()),
        'examples':{'fixed_before_scoring':[next(x for x in ac if x['task']==task and x['repeat']==1) for task in FIXED_EXAMPLES],
                    'weakest_overall_AC':weakest,'selection_rule':'minimum C-A overall score, then task ID, then repeat; no output excerpts generated'},
        'all_AC_differences':ac}


def markdown(summary):
    lines = ['# Descriptive evaluation data', '',
             '60 outputs; 21 validated anonymous packets; 48 comparisons. All integrity checks passed before deblinding.', '',
             'These are descriptive ordinal scores, not validated population effects or human learning gains.', '',
             '## Mathematics: means and factorial contrasts', '',
             '| Dimension | A | B | C | D | ΔR | ΔC | I |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    m = summary['mathematics']
    for d in DIMENSIONS:
        vals = [m['groups'][g]['score_means'][d] for g in 'ABCD'] + list(m['contrasts'][d].values())
        lines.append('| '+d+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
    lines += ['', 'ΔR=((B−A)+(D−C))/2; ΔC=((C−A)+(D−B))/2; I=D−B−C+A.', '',
              '## Cross-domain contrasts', '', '| Domain/task | Dimension | A | C | C−A |', '|---|---|---:|---:|---:|']
    for label, block in {**summary['cross_domain'], **summary['cross_by_task']}.items():
        for d in DIMENSIONS:
            vals=[block['groups'][g]['score_means'][d] for g in 'AC']+[block['C_minus_A'][d]]
            lines.append('| '+label+' | '+d+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
    lines += ['', '## Pair comparisons', '', '| Domain: first vs second | n | First wins | Ties | Second wins |', '|---|---:|---:|---:|---:|']
    for label,c in summary['pair_counts'].items():
        lines.append(f"| {label} | {c['n']} | {c['first_wins']} | {c['ties']} | {c['second_wins']} |")
    lines += ['', '## Every task, repetition and condition', '',
              'Scores: correctness (Corr), prior knowledge (PK), sequencing (Seq), motivation (Mot), coherence (Coh), cognitive load (Load), transfer support (Tr), overall (Overall). Redundancy: 1=none, 5=severe. Errors are unadjudicated judge flags.', '',
              '| Task | Rep | Group | Corr | PK | Seq | Mot | Coh | Load | Tr | Overall | Redundancy | Major | Minor | Chars | Han | Seconds |',
              '|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in summary['per_text']:
        values=[row['task'],row['repeat'],row['group'],*(row['scores'][d] for d in DIMENSIONS),row['redundancy'],row['errors']['major'],row['errors']['minor'],row['chars'],row['han_chars'],row['elapsed_seconds']]
        lines.append('| '+' | '.join(map(str,values))+' |')
    lines += ['', 'Per-task and per-repetition factorial tables, length/duration summaries, raw numeric usage field sums and exact file hashes are in `summary.json`.', '',
              '## Successful-call usage', '', '```json', json.dumps(summary['usage'],ensure_ascii=False,indent=2), '```', '',
              '## Example selection', '', '```json', json.dumps(summary['examples'],ensure_ascii=False,indent=2), '```', '', '## Limits', '']
    if summary.get('infrastructure_amendment'):
        lines += ['Runner validation code was amended between generation and evaluation. The original manifest and generation runner hashes were verified; task, prompt and generation configuration hashes are unchanged. The amendment record is reproduced in `summary.json`.', '']
    lines.extend('- '+text for text in summary['limitations'])
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--evidence-dir',type=Path,
                        help='Frozen evidence directory; defaults to private run if present, otherwise evaluations/records')
    args=parser.parse_args()
    try:
        summary=analyze(args.root.resolve(), args.evidence_dir)
        data=json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
        report=markdown(summary)
        # No result files are written until every gate and calculation has passed.
        for name,content in (('summary.json',data),('results-data.md',report)):
            path=args.root/'evaluations'/name
            temp=path.with_suffix(path.suffix+'.tmp')
            temp.write_text(content)
            temp.replace(path)
        print('Validated 60 outputs, 21 judgments and 48 pairs; wrote summary.json and results-data.md.')
        return 0
    except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
        print('Analysis refused: '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
