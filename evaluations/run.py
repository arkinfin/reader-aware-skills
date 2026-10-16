#!/usr/bin/env python3
"""Bounded local evaluation runner. No API credentials, fallback, or global edits."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import random
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'evaluations'
RUN = ROOT / '.workflow/experiment-v1'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def read(path):
    return json.loads(path.read_text())


def adapter(config):
    sys.path.insert(0, str(Path(config['workspace']) / 'workflow'))
    from src.adapters.codex_cli import CodexCliAdapter
    from src.workflow.config import load_settings

    class IsolatedAdapter(CodexCliAdapter):
        def _run(self, command, prompt, workdir):
            command[2:2] = ['--ignore-user-config', '--skip-git-repo-check', '--strict-config']
            return super()._run(command, prompt, workdir)

    return IsolatedAdapter(load_settings())


def isolation():
    skill_paths = sorted(Path('/home/samsa/.codex/skills').rglob('SKILL.md'))
    overrides = {
        'project_doc_max_bytes': '0',
        'web_search': '"disabled"',
        'features.skip_host_skill_discovery': 'true',
        'features.skill_search': 'false',
        'features.plugins': 'false',
        'features.apps': 'false',
        'features.multi_agent': 'false',
        'features.shell_tool': 'false',
        'features.unified_exec': 'false',
        'features.code_mode_host': 'false',
        'features.browser_use': 'false',
        'features.computer_use': 'false',
        'features.image_generation': 'false',
        'features.hooks': 'false',
        'features.view_image': 'false',
        'skills.config': '[' + ','.join('{path='+json.dumps(str(p.parent))+',enabled=false}' for p in skill_paths) + ']',
    }
    return overrides


def call(prompt, key, role='pdf_writer'):
    config = (read(RUN/'manifest.json')['config'] if (RUN/'manifest.json').exists()
              else read(RUN/'config.json'))
    client = adapter(config)
    model = config['generation_model'] if role == 'pdf_writer' else config['judge_model']
    effort = config['generation_effort'] if role == 'pdf_writer' else config['judge_effort']
    # Preserve actual command/event evidence; adapter still performs error classification.
    original_run = client._run
    capture = {}

    def recorded(command, text, workdir):
        result = original_run(command, text, workdir)
        capture.update(stdout=result.stdout, stderr=result.stderr, returncode=result.returncode,
                       command=command)
        return result

    client._run = recorded
    started = now()
    t0 = time.monotonic()
    attempt_dir = RUN / 'attempts' / key
    attempt_dir.mkdir(parents=True, exist_ok=True)
    attempt_number = len(list(attempt_dir.glob('*.json'))) + 1
    result = {'key': key, 'attempt': attempt_number, 'started_utc': started,
              'requested_model': model, 'reasoning_effort': effort,
              'prompt_sha256': sha(prompt.encode()), 'prompt_chars': len(prompt)}
    try:
        with tempfile.TemporaryDirectory(prefix='reader-aware-isolated-') as cwd:
            response = client.complete(
                prompt, role=role, model=model, reasoning_effort=effort,
                escalation_reason='Uniform technical explanation experiment requires dependency and derivation reasoning.',
                config_overrides=config['isolation_overrides'], sandbox='read-only', workdir=cwd)
        events = []
        for line in capture.get('stdout', '').splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        forbidden = []
        for event in events:
            item = event.get('item', {})
            kind = item.get('type', '')
            if kind == 'error':
                message=item.get('message','')
                allowed=('Under-development features enabled: skip_host_skill_discovery.',
                         'Code Mode is unavailable because code-mode host is disabled.')
                if not any(message.startswith(prefix) for prefix in allowed):
                    forbidden.append('unrecognized_error_item')
            if kind and kind not in {'agent_message', 'reasoning', 'error'}:
                forbidden.append(kind)
        if forbidden:
            raise RuntimeError('Protocol violation: tool/event items ' + repr(forbidden))
        result.update(status='completed', text=response.text, usage=response.usage,
                      adapter_model_label=response.model, server_model_identity='not independently exposed by CLI',
                      model_revision='not exposed by CLI',
                      chars=len(response.text), han_chars=len(re.findall(r'[\u3400-\u9fff]', response.text)),
                      tool_items=forbidden)
    except Exception as exc:
        result.update(status='failed', error_type=type(exc).__name__, error=str(exc))
    result.update(finished_utc=now(), elapsed_seconds=round(time.monotonic()-t0, 3),
                  transport=capture)
    write(attempt_dir / f'{attempt_number:02d}.json', result)
    return result


def preflight():
    if (RUN/'manifest.json').exists():
        raise SystemExit('Frozen run exists; preflight cannot alter its configuration.')
    if not (RUN / 'config.json').exists():
        workspace = str(ROOT.parents[1])
        sys.path.insert(0, str(Path(workspace) / 'workflow'))
        from src.workflow.config import load_settings
        settings = load_settings()
        writer = settings.models.roles['pdf_writer']
        judge = settings.models.roles['technical_guard']
        write(RUN / 'config.json', {
            'workspace': workspace,
            'generation_model': settings.env(writer['model_env']) or writer['default_model'],
            'generation_effort': 'medium',
            'generation_escalation_reason': 'Uniform technical tasks include nontrivial derivations and knowledge dependencies.',
            'judge_model': settings.env(judge['model_env']) or judge['default_model'],
            'judge_effort': judge['reasoning_effort'],
            'source_registry_sha256': sha((Path(workspace)/'workflow/config/models.example.yaml').read_bytes()),
            'cli_version': subprocess.check_output(['codex', '--version'], text=True).strip(),
            'temperature': 'not controllable', 'sampling_seed': 'not controllable',
            'fallback': 'disabled', 'isolation_overrides': isolation(),
        })
    config=read(RUN/'config.json')
    config['isolation_overrides']=isolation()
    write(RUN/'config.json',config)
    prompt = ('这是传输预检，不是写作实验。只返回JSON，列出当前实际提供给你的工具名称tools、'
              '可用Skill名称skills、是否收到AGENTS项目指导has_project_guidance。'
              '若没有则空列表或false。不调用工具，不披露系统或开发者指令正文。')
    outcome = call(prompt, 'preflight')
    write(RUN / 'preflight.json', outcome)
    print(json.dumps({k: outcome.get(k) for k in ['status', 'text', 'error', 'elapsed_seconds']}, ensure_ascii=False), flush=True)
    return 0 if outcome['status'] == 'completed' else 1


def prepare():
    if (RUN / 'manifest.json').exists():
        raise SystemExit('Frozen run already exists; use resume commands, do not overwrite.')
    if any((EVAL/'outputs').glob('*.json')) or any((EVAL/'judgments').glob('*.json')):
        raise SystemExit('Fresh study requires empty output/judgment directories; do not reuse prior results.')
    tasks = [read(p) for p in sorted((EVAL / 'tasks').glob('*.json'))]
    assert len(tasks) == 7
    assert sum(t['domain'] == 'mathematics' for t in tasks) == 3
    seed = 20261016
    rng = random.Random(seed)
    modules = {name: (EVAL/'prompts'/f'{name}.txt').read_text() for name in ['common', 'rigor', 'judge']}
    modules['readability'] = (ROOT/'skills/reader-aware-writing/SKILL.md').read_text()
    cells = []
    for rep in range(1,4):
        batch = []
        for task in tasks:
            for group in ('ABCD' if task['domain']=='mathematics' else 'AC'):
                key = f"{task['id']}-{group}-r{rep}"
                sections = [modules['common'], json.dumps(task, ensure_ascii=False, indent=2)]
                if group in 'BD':
                    sections.append(modules['rigor'])
                if group in 'CD':
                    sections.append(modules['readability'])
                prompt = '\n\n'.join(sections)
                path = RUN/'generation-prompts'/f'{key}.txt'
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(prompt)
                batch.append({'id':key,'task':task['id'],'domain':task['domain'],
                              'group':group,'repeat':rep,'prompt_sha256':sha(prompt.encode())})
        rng.shuffle(batch)
        cells.extend(batch)
    paths = [*sorted((EVAL/'tasks').glob('*.json')), *sorted((EVAL/'prompts').glob('*.txt')),
             ROOT/'skills/reader-aware-writing/SKILL.md', Path(__file__)]
    write(RUN/'manifest.json', {'run_id':'experiment-v1','frozen_utc':now(),'seed':seed,
                              'cells':cells,'config':read(RUN/'config.json'),
                              'input_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}})
    write(EVAL/'protocol.json', {'run_id':'experiment-v1','seed':seed,'frozen_utc':now(),
                               'planned_outputs':60,'batches':3,'config':{k:v for k,v in read(RUN/'config.json').items() if k!='workspace'},
                               'input_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}})
    print('Frozen 60 generation calls in three balanced batches.', flush=True)


def verify_frozen():
    manifest = read(RUN/'manifest.json')
    for relative, expected in manifest['input_hashes'].items():
        assert sha((ROOT/relative).read_bytes()) == expected, f'Frozen input changed: {relative}'
    return manifest


def bounded_call(prompt, key, role='pdf_writer'):
    # At most two attempts total; only transport errors are eligible, never poor content.
    existing = sorted((RUN/'attempts'/key).glob('*.json')) if (RUN/'attempts'/key).exists() else []
    for p in existing:
        prior = read(p)
        if prior['status']=='completed':
            return prior
        if prior.get('error_type')!='TransientToolError':
            return prior
    for _ in range(len(existing), 2):
        outcome = call(prompt, key, role)
        if outcome['status']=='completed':
            return outcome
        if outcome.get('error_type') != 'TransientToolError':
            break
    return outcome if 'outcome' in locals() else read(sorted(existing)[-1])


def generate(workers):
    manifest = verify_frozen()
    assert read(RUN/'isolation-accepted.json')['accepted'] is True
    for rep in range(1,4):
        cells = [c for c in manifest['cells'] if c['repeat']==rep]
        stop=threading.Event()
        def work(cell):
            key = cell['id']
            path = EVAL/'outputs'/f'{key}.json'
            if path.exists():
                existing=read(path)
                validate_output(existing,cell)
                return existing
            if stop.is_set():
                return {'status':'not_started_after_batch_failure'}
            prompt = (RUN/'generation-prompts'/f'{key}.txt').read_text()
            assert sha(prompt.encode())==cell['prompt_sha256']
            outcome = bounded_call(prompt,key)
            public = {**cell, **{k:v for k,v in outcome.items() if k!='transport'}}
            if outcome['status']=='completed':
                write(path,public)
            else:
                stop.set()
            print(f"{key}: {outcome['status']}",flush=True)
            return outcome
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(work,cells))
        write(RUN/f'batch-{rep}.json',{'repeat':rep,'completed':sum(r['status']=='completed' for r in results),'total':20,'finished_utc':now()})
        if any(r['status']!='completed' for r in results):
            raise SystemExit(f'Batch {rep} incomplete. Saved all attempts; resume without changing conditions.')


def validate_output(record,cell):
    assert record['status']=='completed' and record['key']==cell['id']
    assert all(record[k]==v for k,v in cell.items())
    source=read(RUN/'attempts'/cell['id']/f"{record['attempt']:02d}.json")
    assert source['status']=='completed'
    assert record=={**cell,**{k:v for k,v in source.items() if k!='transport'}}, 'Output differs from successful attempt'
    assert record['prompt_sha256']==sha((RUN/'generation-prompts'/f"{cell['id']}.txt").read_bytes())


def blind():
    manifest = verify_frozen()
    files={p.stem:p for p in (EVAL/'outputs').glob('*.json')}
    assert set(files)=={c['id'] for c in manifest['cells']}
    for cell in manifest['cells']:
        validate_output(read(files[cell['id']]),cell)
    if (RUN/'blind-map.json').exists():
        for relative,expected in read(RUN/'blind-freeze.json')['hashes'].items():
            assert sha((RUN/relative).read_bytes())==expected
        return
    write(RUN/'output-freeze.json',{'frozen_utc':now(),'hashes':{key:sha(path.read_bytes()) for key,path in sorted(files.items())}})
    rng = random.Random(manifest['seed'] + 1)
    tasks = {read(p)['id']:read(p) for p in (EVAL/'tasks').glob('*.json')}
    packets, mapping = [], {}
    for rep in range(1,4):
        for taskid,task in sorted(tasks.items()):
            cells = [c for c in manifest['cells'] if c['repeat']==rep and c['task']==taskid]
            rng.shuffle(cells)
            texts=[]
            aliases={}
            for cell in cells:
                alias='T'+''.join(rng.choices('0123456789abcdef',k=12))
                assert alias not in mapping
                mapping[alias]=cell['id']
                aliases[cell['group']]=alias
                texts.append({'id':alias,'text':read(EVAL/'outputs'/f"{cell['id']}.json")['text']})
            pairs=[]
            for a,b in ([('A','B'),('A','C'),('B','D'),('C','D')] if task['domain']=='mathematics' else [('A','C')]):
                pair=[aliases[a],aliases[b]]
                rng.shuffle(pair)
                pairs.append({'left':pair[0],'right':pair[1]})
            rng.shuffle(pairs)
            packet={'task':task,'texts':texts,'pairs':pairs}
            packetid='P'+''.join(rng.choices('0123456789abcdef',k=12))
            write(RUN/'blind-packets'/f'{packetid}.json',packet)
            prompt=(EVAL/'prompts/judge.txt').read_text()+'\n\n'+json.dumps(packet,ensure_ascii=False,indent=2)
            (RUN/'judge-prompts').mkdir(exist_ok=True)
            (RUN/'judge-prompts'/f'{packetid}.txt').write_text(prompt)
            packets.append(packetid)
    rng.shuffle(packets)
    write(RUN/'blind-map.json',mapping)
    write(RUN/'judge-order.json',packets)
    files=[*sorted((RUN/'blind-packets').glob('*.json')),*sorted((RUN/'judge-prompts').glob('*.txt')),
           RUN/'blind-map.json',RUN/'judge-order.json']
    write(RUN/'blind-freeze.json',{'frozen_utc':now(),'hashes':{str(p.relative_to(RUN)):sha(p.read_bytes()) for p in files}})
    print('Prepared 21 blinded packets / 48 randomized comparisons.',flush=True)


DIMENSIONS = ['correctness','prior_knowledge_alignment','conceptual_sequencing','motivation',
              'explanatory_coherence','cognitive_load','transfer_support','overall_comprehensibility']


def validate_judgment(data,packet):
    assert set(data)=={'texts','pairs'}
    texts={t['id']:t['text'] for t in packet['texts']}
    assert {t['id'] for t in data['texts']}==set(texts)
    assert len(data['texts'])==len(texts)
    for item in data['texts']:
        text=texts[item['id']]
        assert set(item['scores'])==set(DIMENSIONS)
        assert all(type(v) is int and 1<=v<=5 for v in item['scores'].values())
        assert len(item['evidence'])>=2
        for ev in item['errors']+item['evidence']:
            assert ev['quote'] and ev['quote'] in text, 'Non-verbatim evidence'
            assert ev['reason'].strip()
        assert all(e['dimension'] in DIMENSIONS for e in item['evidence'])
        assert all(e['severity'] in {'major','minor'} for e in item['errors'])
        redundant=item['redundancy']
        assert type(redundant['score']) is int and 1<=redundant['score']<=5
        assert redundant['reason'].strip()
        if redundant['score']>1:
            assert redundant['quote'].strip(), 'Redundancy problem needs verbatim evidence'
        assert not redundant['quote'] or redundant['quote'] in text
    expected={(p['left'],p['right']) for p in packet['pairs']}
    assert {(p['left'],p['right']) for p in data['pairs']}==expected
    assert len(data['pairs'])==len(expected)
    for pair in data['pairs']:
        assert pair['winner'] in {'left','right','tie'}
        assert pair['left_quote'] and pair['left_quote'] in texts[pair['left']]
        assert pair['right_quote'] and pair['right_quote'] in texts[pair['right']]
        assert pair['reason']


def evaluate(workers):
    verify_frozen()
    for relative,expected in read(RUN/'blind-freeze.json')['hashes'].items():
        assert sha((RUN/relative).read_bytes())==expected, 'Changed blind input: '+relative
    for key,expected in read(RUN/'output-freeze.json')['hashes'].items():
        assert sha((EVAL/'outputs'/f'{key}.json').read_bytes())==expected
    def work(key):
        path=EVAL/'judgments'/f'{key}.json'
        if path.exists():
            record=read(path)
            assert record['status']=='validated' and record['id']==key
            validate_judgment(record['judgment'],read(RUN/'blind-packets'/f'{key}.json'))
            meta=record['metadata']
            source=read(RUN/'attempts'/key/f"{meta['attempt']:02d}.json")
            assert meta=={k:v for k,v in source.items() if k not in {'transport','text'}}
            assert source['status']=='completed'
            raw=source['text'].strip()
            if raw.startswith('```'):
                raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw)
            assert record['judgment']==json.loads(raw)
            return 'validated'
        outcome=bounded_call((RUN/'judge-prompts'/f'{key}.txt').read_text(),key,'technical_guard')
        if outcome['status']!='completed':
            print(f'{key}: failed transport',flush=True)
            return 'failed'
        try:
            raw=outcome['text'].strip()
            if raw.startswith('```'):
                raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw)
            parsed=json.loads(raw)
            validate_judgment(parsed,read(RUN/'blind-packets'/f'{key}.json'))
            write(path,{'id':key,'status':'validated','judgment':parsed,
                        'metadata':{k:v for k,v in outcome.items() if k not in {'transport','text'}}})
            print(f'{key}: validated',flush=True)
            return 'validated'
        except Exception as exc:
            write(RUN/'invalid-judgments'/f'{key}.json',{'id':key,'error':str(exc),'raw':outcome['text']})
            print(f'{key}: invalid {exc}',flush=True)
            return 'invalid'
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        statuses=list(pool.map(work,read(RUN/'judge-order.json')))
    if any(s!='validated' for s in statuses):
        raise SystemExit('Some judgments failed deterministic validation. No selective regeneration.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['preflight','prepare','generate','blind','evaluate'])
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    assert 1<=args.workers<=3
    RUN.mkdir(parents=True,exist_ok=True)
    if args.stage=='preflight': return preflight()
    if args.stage=='prepare': prepare()
    if args.stage=='generate': generate(args.workers)
    if args.stage=='blind': blind()
    if args.stage=='evaluate': evaluate(args.workers)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
