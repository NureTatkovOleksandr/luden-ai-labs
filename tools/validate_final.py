"""Check final documentation against preserved primary sources, without live services."""
from pathlib import Path
import csv,json,re,hashlib,html,sys
from urllib.parse import unquote
BASE=Path(__file__).resolve().parents[1];DOC=BASE/'docs';VER=BASE/'verification'
def read(p):return p.read_text(encoding='utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
def check(n,ok,detail):results.append(dict(check=n,status='PASS' if ok else 'FAIL',detail=detail))
documents={p:read(p) for p in [BASE/'README.md',*DOC.glob('*.md')]}
req=read(DOC/'requirements.md');tests=read(DOC/'test-cases.md')
index=json.loads(read(VER/'contracts-index.json'));prov=json.loads(read(VER/'ac-provenance.json'))
evidence=json.loads(read(VER/'evidence-index.json'));ai=json.loads(read(VER/'api-index.json'));hist=json.loads(read(VER/'source-history.json'))
source_acs={};stories={}
for line in read(BASE/'sources/input-pack-initial.txt').splitlines():
    c=[x.strip() for x in line.strip().strip('|').split('|')]
    if len(c)!=4 or not re.fullmatch(r'US-\d{2}',c[0]):continue
    stories[c[0]]=c[1];pieces=re.split(r'(AC-\d{2}\.\d+)\s+',c[2])
    for n in range(1,len(pieces),2):source_acs[pieces[n]]=pieces[n+1].strip()
actual={}
for line in req.splitlines():
    c=[html.unescape(x.strip()) for x in line.strip().strip('|').split('|')]
    if len(c)>1 and re.fullmatch(r'AC-0[1-8]\.\d+',c[0]):actual[c[0]]=c[1]
check('Primary 33 AC exact source meaning',len(source_acs)==33 and actual==source_acs,{'count':len(actual),'missing':sorted(set(source_acs)-set(actual)),'changed':[k for k in source_acs.keys()&actual.keys() if actual[k]!=source_acs[k]]})
check('Original 8 stories',len(stories)==8 and all(s in req for s in stories.values()),list(stories))
check('Per-AC historical provenance',len(prov['records'])==33 and all(r['text']==source_acs[r['id']] and r['baseline_text'] and r['current_text'] and r['previous_lr1'] for r in prov['records']),{'initial':prov['initial'],'baseline':prov['baseline'],'current':prov['current']})
def block(tc):
    m=re.search(r'^### '+re.escape(tc)+r'[^\n]*\n(.*?)(?=^### |^## |\Z)',tests,re.M|re.S)
    return m.group(1) if m else ''
semantic=[]
for r in prov['records']:
    if r['text'] not in block(r['test']):semantic.append(r['id'])
for tc,terms in {'TC-02-04':['password','type=text/password'],'TC-06-03':['Порожній кошик','недоступна'],'TC-06-04':['останню','порожній'],'TC-07-05':['Скасувати','збережені'],'TC-08-01':['профілю','бібліотеку'],'TC-08-04':['бібліотеки','магазину']}.items():
    if not all(t in block(tc) for t in terms):semantic.append(tc)
check('Semantic regressions and test oracles',not semantic,{'errors':semantic,'scope':'source equality plus password toggle, cancel, empty/block and navigation; not a new human review'})
tcids=set(re.findall(r'^### (TC-[A-Z0-9-]+)',tests,re.M))|{f'TC-NFR-0{i}' for i in range(1,5)}
acs=set(source_acs)|{'AC-09.1','AC-09.2'};exts={x[0] for x in index['extensions']};brs=set(index['business_rules'])
apiids={x['id'] for x in ai['operations']}|set(ai['proposed'])
with (DOC/'traceability.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
errors=[]
for r in rows:
    if None in r or any(v is None for v in r.values()):errors.append('row width');continue
    if r['scope']=='DEFERRED':
        if r['test_status']!='NOT DEFINED':errors.append('deferred test')
        continue
    if r['acceptance_criterion'] not in acs|exts|{f'NFR-0{i}' for i in range(1,5)}:errors.append('criterion')
    if r['test_case'] not in tcids or r['test_status']!='NOT RUN':errors.append('test')
    if r['api']!='NOT APPLICABLE' and any(x not in apiids for x in r['api'].split(';')):errors.append('API')
    if any(x not in brs for x in r['business_rule'].split(';')):errors.append('BR')
    if r['criterion_kind']=='ORIGINAL_AC' and r['source_commit']!=prov['initial']:errors.append('source version')
check('CSV syntax, references and status',not errors,{'rows':len(rows),'errors':errors})
check('Original AC documentary coverage',{r['acceptance_criterion'] for r in rows if r['criterion_kind']=='ORIGINAL_AC'}==set(source_acs),{'original_ac':'33/33','original_src':'5/6','candidate_src':'6/6 with proposed US09','code_coverage':'NOT MEASURED'})
check('56 future tests all traced',len(tcids)==56 and tcids=={r['test_case'] for r in rows if r['scope']=='CURRENT'},{'defined':len(tcids),'executed':0,'status':'NOT RUN'})
check('Extensions not relabeled original AC',exts=={r['acceptance_criterion'] for r in rows if r['criterion_kind']=='PROPOSED_EXTENSION'},{'extensions':len(exts)})
broken=[];invalid=[];links=0;pins=0;syntax=[];json_count=0
repomap={'Ramseer24/Luden-Back-End':'backend','Timbuhtuk/Luden-Front-End':'frontend','NureTatkovOleksandr/luden-ux-ui':'ux_ui'}
for p,text in documents.items():
    for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
        if target.startswith('http'):
            m=re.fullmatch(r'https://github.com/([^/]+/[^/]+)/blob/([a-f0-9]{40})/(.+)#L(\d+)',target)
            if m:
                pins+=1;repo,commit,name,line=m.groups();s=evidence.get(repomap.get(repo),{})
                files=s.get('files',{}) if s.get('commit')==commit else s.get('historical_snapshots',{}).get(commit,{})
                meta=files.get(unquote(name))
                if not meta or not 1<=int(line)<=meta['lines']:invalid.append(target)
            continue
        if target.startswith(('#','mailto:')):continue
        links+=1
        if not (p.parent/unquote(target.split('#')[0])).exists():broken.append([p.name,target])
    for b in re.findall(r'```json\s*\n(.*?)\n```',text,re.S):
        json_count+=1
        try:json.loads(b)
        except ValueError as e:syntax.append(p.name+': '+str(e))
    fence=False;width=None
    for n,line in enumerate(text.splitlines(),1):
        if line.startswith('```'):fence=not fence;width=None;continue
        if fence:continue
        if line.startswith('|'):
            count=len(line.split('|'))-2
            if width is None:width=count
            elif count!=width:syntax.append(f'{p.name}:{n}:table width')
        else:width=None
    if fence:syntax.append(p.name+':fence')
check('Moved Markdown links',not broken,{'checked':links,'broken':broken})
check('Pinned GitHub paths and lines',not invalid,{'checked':pins,'invalid':invalid})
check('Markdown and JSON syntax',not syntax,{'json_blocks':json_count,'errors':syntax})
ex=json.loads(read(VER/'api-examples.json'))
check('Per-operation API examples',len(ex)==22 and {x['id'] for x in ex}==apiids,'18 implemented +4 proposed; synthetic NOT RUN; multipart fields are a representation, not JSON wire')
model=json.loads(read(VER/'domain-properties.json'));missing=[]
for entity,props in model.items():
    seg=re.search(r'### 4\.\d+\. '+entity+r'\n(.*?)(?=\n### |\n## |\Z)',req,re.S)
    for prop in props:
        name=prop['name'];camel=name[0].lower()+name[1:]
        if prop['json_ignore']:
            if '| '+entity+'.'+name+' |' not in req:missing.append(entity+'.'+name)
        elif camel in ['id','createdAt','updatedAt']:
            if '| '+camel+' |' not in req:missing.append(name)
        elif not seg or '| '+camel+' |' not in seg.group(1):missing.append(entity+'.'+name)
check('Actual model field coverage',not missing,{'entities':len(model),'properties':sum(len(x) for x in model.values()),'missing':missing})
matrix=[[x.strip() for x in l.strip('|').split('|')][1:] for l in req.splitlines() if re.match(r'^\| (PENDING|PROCESSING|DECLINED|PAID|COMPLETED) \|',l)]
check('Full state matrix',matrix==[['Т','Д','Н','Н','Н'],['Н','Т','Д','Д','Н'],['Н','Д','Т','Н','Н'],['Н','Н','Н','Т','Д'],['Н','Н','Н','Н','Т']],{'states':5,'cells':25})
check('PATCH null/missing and atomic rules','nullable releaseDate може очищатися' in req and 'releaseDate:null' in block('TC-09-01') and 'без будь-якої зміни' in block('TC-09-01'),'Nullable clear distinct from missing; nonnullable null/mixed invalid do not persist')
decision=read(DOC/'decision-log.md')
check('P01-P08 and version conflicts explicit',all(f'P-0{i}' in decision for i in range(1,9)) and all(x in decision for x in ['profile','quantity','PROPOSED']),'No blanket acceptance of P proposals from team review')
check('Confirmed four-person team review',hist['review_confirmation']=='USER_CONFIRMED' and len(hist['review_participants'])==4 and all(n in read(DOC/'lab-01.md') for n in hist['review_participants']),{'participants':hist['review_participants'],'basis':'direct user confirmation','review_date':None,'individual_findings':'not fabricated'})
stale=[]
for p,text in documents.items():
    if p.name in ['ai-log.md','ac-reconciliation.md']:continue
    for phrase in ['Первинного Input Pack немає','Input Pack і Test_Cases відсутні','людське рев’ю ще не проведено','первинний текст NOT VERIFIED']:
        if phrase in text:stale.append([p.name,phrase])
check('No obsolete active blockers',not stale,stale)
check('Clean current repository snapshots',all(x['clean'] for x in evidence.values()),{k:v['commit'] for k,v in evidence.items()})
check('PDF matches current Markdown',sha(DOC/'lab-01.md')==read(VER/'pdf-source.sha256').split()[0],'Current source hash')
from pypdf import PdfReader
pdf=PdfReader(DOC/'lab-01.pdf');txt='\n'.join(p.extract_text() for p in pdf.pages)
check('Short Ukrainian report PDF',2<=len(pdf.pages)<=3 and 'Паламарчук' in txt and 'Висновки' in txt,{'pages':len(pdf.pages),'Ukrainian_text':True})
visual=json.loads(read(VER/'pdf-visual-review.json')) if (VER/'pdf-visual-review.json').exists() else {}
check('Final PDF visual inspection',visual.get('pdf_sha256')==sha(DOC/'lab-01.pdf') and visual.get('status')=='PASS',visual or 'Pending visual inspection')
mm=json.loads(read(VER/'mermaid-validation.json'))
check('Actual Mermaid parser',mm['architecture_sha256']==sha(DOC/'architecture.md') and len(mm['diagrams'])==4 and all(d['status']=='PASS' for d in mm['diagrams']),mm)
payload={'date':'2026-11-20','checks':results,'product_tests':{'defined':56,'executed':0,'status':'NOT RUN'},'human_review':'CONFIRMED_BY_USER_FOUR_PARTICIPANTS','P_approval':'NOT PROVIDED'}
(VER/'validation-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
content='''# Фактично виконані перевірки фіналу

20.11.2026. Документаційні, джерельні та статичні перевірки; це не продуктове тестування. [Машинний протокол](../verification/validation-results.json), [валідатор](../tools/validate.py). Командне review чотирьох підтверджене користувачем; наведені перевірки — окрема робота AI, а не вигадане незалежне людське review.

| Перевірка | Результат | Підстава |
| --- | --- | --- |
'''
for r in results:
    d=json.dumps(r['detail'],ensure_ascii=False) if not isinstance(r['detail'],str) else r['detail']
    content+='| '+r['check']+' | '+r['status']+' | '+d.replace('|','/').replace('\n',' ')+' |\n'
content+='''
## Змістова перевірка й межі

Кожен із 33 первинних текстів порівняно окремим парсером із джерелом. Перевірено видимість пароля, cancel, empty/block, profile/library/store та quantity/destination/create-trigger конфлікти. Змістовий аналіз кожної версії — у [ac-reconciliation.md](ac-reconciliation.md). Евристика не є повною автоматичною перевіркою природної мови; рішення не приписано іншому рецензенту.

56 продуктових TC — NOT RUN. Backend/frontend/Android build, зовнішні Firebase/Stripe, runtime ownership/security/concurrency, restart та WCAG-вимірювання не запускались. F-T01–F-T07 — історичні записи UX Present, не нові тести агента. Повторний fetch та читання важливих code paths підтвердили незмінні актуальні BE/FE.

У двох Firebase config-файлах лишаються [потенційні секрети](../verification/secret-scan.json); значення й активність не перевіряли та не розкривали. Raw-token console log і unsalted SHA-256 — CONFIRMED факти коду. Жоден дефект продукту не закрито самим редагуванням документації.

Новий meaningful commit/tag, перевірка bundle й ZIP checksum фіксуються в [VERSION.txt](../VERSION.txt) та протоколі пакування після фінальної перевірки. Попередній commit/tag і архіви збережені. Версія GitHub-здавання — lab01-spec-published; факт публікації перевіряється окремим зовнішнім протоколом.
'''
(DOC/'validation.md').write_text(content,encoding='utf-8')
for r in results:print(r['status'],r['check'])
sys.exit(1 if any(r['status']=='FAIL' for r in results) else 0)
