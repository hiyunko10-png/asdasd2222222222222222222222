import json
import threading
import uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
import streamlit as st

st.set_page_config(page_title='우리집',page_icon='🏠',layout='centered',initial_sidebar_state='collapsed')
st.markdown("""<style>
:root{color-scheme:light;--text-color:#252525;--background-color:#e8edf2;--secondary-background-color:#ffffff;--primary-color:#26465b;}
html,body,.stApp,[data-testid="stAppViewContainer"],section.main{height:100dvh!important;overflow:hidden!important;background:#e8edf2!important;color:#252525!important;}
[data-testid="stMain"]{height:100dvh!important;overflow:hidden!important;}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stSidebar"],[data-testid="collapsedControl"],footer{display:none!important;}
.block-container{max-width:540px!important;padding:16px 19px 88px!important;height:100dvh!important;overflow:hidden!important;}
[data-testid="stVerticalBlock"]{gap:8px!important;}
h1,h2,h3,p,label,span,li{color:#252525;}
[data-testid="stMarkdownContainer"] p,[data-testid="stWidgetLabel"] p{color:#252525!important;}
[data-testid="stCaptionContainer"] p{color:#676b70!important;font-size:12px!important;}
h3{font-size:20px!important;padding:4px 0!important;}
input,textarea,[data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="select"]>div{background:#fff!important;color:#252525!important;-webkit-text-fill-color:#252525!important;border-color:#d9dce0!important;border-radius:12px!important;}
input::placeholder{color:#7a7e83!important;-webkit-text-fill-color:#7a7e83!important;}
[data-baseweb="select"] div,[data-baseweb="select"] span{color:#252525!important;}
[data-baseweb="popover"],[role="listbox"],[role="option"],[data-baseweb="menu"]{background:#fff!important;color:#252525!important;}
[data-baseweb="select"] svg{fill:#50545a!important;}
button{min-height:40px!important;border-radius:13px!important;background:#fff!important;border:1px solid #d9dce0!important;color:#252525!important;box-shadow:none!important;}
button p,button span{color:inherit!important;font-size:13px!important;}
button[kind="primary"],button[kind="primaryFormSubmit"]{background:#26465b!important;color:#252525!important;border-color:#26465b!important;}
button:hover{border-color:#6e91a8!important;}
button:disabled{opacity:.4!important;}
[data-testid="stForm"]{border:0!important;padding:0!important;}
[data-testid="stAlert"]{padding:8px!important;background:#fff4c7!important;color:#252525!important;border-radius:12px;}
[data-testid="stAlert"] p{font-size:12px!important;color:#403a28!important;}
.brand{font-size:12px;letter-spacing:1px;color:#4a4b4e;font-weight:750;margin-bottom:6px;}
.heading{font-size:27px;letter-spacing:-1.3px;font-weight:800;line-height:1.25;margin:4px 0 10px;}
.panel{background:#fff;border:1px solid #e2e3e5;border-radius:22px;padding:19px;margin:3px 0 6px;box-shadow:0 5px 15px #25252504;}
.panel .small{color:#64666c;font-size:12px;line-height:1.6;}
.panel .big{font-size:30px;font-weight:800;letter-spacing:-1px;margin:8px 0;color:#252525;}
.task-title{font-size:21px;line-height:1.35;font-weight:700;overflow-wrap:anywhere;color:#252525;}
.reward{display:inline-block;font-size:27px;font-weight:800;color:#252525;margin:12px 0 9px;background:#fff1b4;border-radius:10px;padding:3px 10px;}
.st-key-nav{position:fixed!important;bottom:0;left:0;right:0;z-index:999;background:#fff;padding:9px max(12px,calc((100vw - 505px)/2)) calc(10px + env(safe-area-inset-bottom));border-top:1px solid #e2e3e5;}
.st-key-nav [data-testid="stHorizontalBlock"]{gap:5px!important;flex-wrap:nowrap!important;}
.st-key-nav [data-testid="stColumn"]{width:auto!important;min-width:0!important;flex:1 1 0!important;}
.st-key-nav button{width:100%;border:0!important;font-size:12px!important;background:#fff!important;color:#6e7278!important;}
.st-key-nav button[kind="primary"]{background:#d5e4ee!important;color:#252525!important;}
[data-testid="stHorizontalBlock"]{gap:8px!important;flex-wrap:nowrap!important;}
[data-testid="stColumn"]{min-width:0!important;}
[data-testid="stFileUploaderDropzone"]{background:#fff!important;color:#252525!important;}
[data-baseweb="radio"]>div:first-child{border-color:#6e91a8!important;}
@media(max-height:720px){.block-container{padding-top:9px!important;}[data-testid="stVerticalBlock"]{gap:5px!important;}.panel{padding:12px;margin:0;}.heading{font-size:23px;margin:2px 0 5px;}.reward{margin:6px 0;font-size:24px;}label p{font-size:12px!important;}button{min-height:35px!important;}}

/* Quiet editorial layout: slate hero, warm paper, restrained blue. */
.brand{font-size:10px;letter-spacing:2px;color:#677783;font-weight:700;margin:2px 0 12px;}
.heading{font-size:28px;letter-spacing:-1.5px;color:#1c3547;font-weight:750;margin:6px 0 16px;}
.panel{background:#203b4e;border:0;border-radius:24px;padding:22px;box-shadow:0 9px 24px #203b4e12;}
.panel .small{color:#c5d4df!important;}.panel .big,.panel .task-title{color:#f4f6f8!important;}
.panel .big{font-size:29px;letter-spacing:-1px;}.task-title{margin-top:10px;font-size:23px;}
button[kind="primary"],button[kind="primaryFormSubmit"]{background:#26465b!important;border-color:#26465b!important;color:#fff!important;}
button[kind="primary"] p,button[kind="primaryFormSubmit"] p{color:#fff!important;}
.st-key-nav{background:#e8edf2!important;border-color:#d0dbe3!important;}
.st-key-nav button{background:transparent!important;border-radius:15px!important;color:#607383!important;}
.st-key-nav button[kind="primary"]{background:#26465b!important;color:#fff!important;}
.st-key-nav button[kind="primary"] p{color:#fff!important;}
.eventbadge{display:inline-block;background:#c9deeb;color:#203b4e;font-weight:750;font-size:11px;letter-spacing:1px;border-radius:8px;padding:5px 9px;margin:9px 0 0;}
@media(max-height:740px){.brand{margin-bottom:4px}.heading{font-size:24px;margin:3px 0 8px}.panel{padding:14px}.panel .big{font-size:25px}.task-title{font-size:20px}.block-container{padding-top:8px!important;}}
</style>""",unsafe_allow_html=True)
FILE=Path('home_today.json')
@st.cache_resource
def mutex():return threading.Lock()
def blank():return {'members':[],'days':{},'tasks':[]}
def disk():
 return json.loads(FILE.read_text(encoding='utf-8')) if FILE.exists() else {'revision':0,'data':blank()}
def save():
 try:
  with mutex():
   if disk()['revision']!=rev:
    st.error('다른 가족이 수정했어요. 하단 메뉴를 눌러 갱신 후 다시 시도하세요.');st.stop()
   temp=FILE.with_suffix('.tmp');temp.write_text(json.dumps({'revision':rev+1,'data':d},ensure_ascii=False),encoding='utf-8');temp.replace(FILE)
 except (OSError,ValueError):st.error('저장하지 못했어요. 다시 시도해주세요.');st.stop()
 st.rerun()
try:
 with mutex():row=disk()
 d=row['data'];rev=row['revision']
except (OSError,ValueError,KeyError):st.error('저장 파일을 읽지 못했어요.');st.stop()
# 기존 버전의 완료·보상 상태를 현재 형식으로 정규화합니다.
for t in d['tasks']:
 try:t['reward']=max(0,min(1000000,int(t.get('reward',0))))
 except (TypeError,ValueError):t['reward']=0
 t.setdefault('paid',False)
 if t.get('status') not in ['open','claimed','submitted','approved','done']:
  t['status']='approved' if t.get('done') else ('claimed' if t.get('owner') else 'open')
 if t['status']=='done':t['status']='approved'
 t.setdefault('owner','');t.setdefault('created','')
for key,val in [('page','오늘'),('compose',False),('idx',0),('settings','가족')]:
 if key not in st.session_state:st.session_state[key]=val
with st.container(key='nav'):
 cols=st.columns(4)
 for c,label in zip(cols,['오늘','부탁','일정','설정']):
  if c.button(label,type='primary' if st.session_state.page==label else 'secondary',use_container_width=True):
   st.session_state.page=label;st.session_state.compose=False;st.session_state.idx=0;st.rerun()
if st.session_state.page not in ['오늘','부탁','일정','설정']:st.session_state.page='오늘'
page=st.session_state.page
d.setdefault('events',[])
st.markdown('<div class="brand">OUR DAYS / 우리집</div>',unsafe_allow_html=True)
from html import escape
def panel(title,body):
 st.markdown('<div class="panel"><div class="small">'+escape(title)+'</div>'+body+'</div>',unsafe_allow_html=True)
def pager(items,key):
 if not items:st.caption('아직 등록된 내용이 없어요.');return None
 i=min(st.session_state.idx,len(items)-1);st.session_state.idx=i
 x,y,z=st.columns([1,2,1])
 if x.button('←',key=key+'prev',disabled=i==0):st.session_state.idx=i-1;st.rerun()
 y.caption(f'{i+1} / {len(items)}')
 if z.button('→',key=key+'next',disabled=i==len(items)-1):st.session_state.idx=i+1;st.rerun()
 return items[i]
if page=='설정' or not d['members']:
 st.markdown('<div class="heading">우리 가족 설정</div>',unsafe_allow_html=True)
 mode=st.radio('설정 메뉴',['가족','백업'],horizontal=True,label_visibility='collapsed')
 if mode=='가족':
  with st.form('member',clear_on_submit=True):
   n=st.text_input('가족 별명',max_chars=16,placeholder='이름 대신 별명으로').strip()
   if st.form_submit_button('가족 추가',type='primary',use_container_width=True):
    if n and n not in d['members']:d['members'].append(n);save()
    else:st.caption('다른 별명을 입력해주세요.')
  panel('함께하는 가족','<div style="line-height:1.7;overflow-wrap:anywhere">'+escape(' · '.join(d['members'][:12]) or '첫 가족을 등록해주세요.')+'</div>')
  if len(d['members'])>12:st.caption(f'외 {len(d["members"])-12}명')
 else:
  st.download_button('전체 데이터 백업',json.dumps(d,ensure_ascii=False,indent=2),'home_backup.json','application/json',use_container_width=True)
  f=st.file_uploader('백업 복원',type=['json'])
  agree=st.checkbox('현재 데이터를 백업으로 교체합니다')
  if st.button('복원',disabled=not agree or f is None):
   try:
    v=json.load(f);assert isinstance(v,dict)
    assert isinstance(v['members'],list) and all(isinstance(n,str) and n for n in v['members'])
    assert isinstance(v['days'],dict) and isinstance(v['tasks'],list)
    for day,entries in v['days'].items():
     assert isinstance(day,str) and isinstance(entries,dict)
     for e in entries.values():assert isinstance(e,dict) and isinstance(e.get('meal'),str) and isinstance(e.get('arrival'),str)
    assert isinstance(v.get('events',[]),list)
    for ev in v.get('events',[]):
     assert all(isinstance(ev.get(k),str) for k in ['id','title','date','who'])
     datetime.fromisoformat(ev['date'])
     assert isinstance(ev.get('items',[]),list)
     for item in ev.get('items',[]):assert isinstance(item.get('text'),str) and isinstance(item.get('done'),bool)
    ids=[]
    for t in v['tasks']:
     assert all(isinstance(t.get(k),str) for k in ['id','title','owner','created'])
     assert type(t.get('reward',0)) is int and 0<=t.get('reward',0)<=1000000
     assert t.get('status','open') in ['open','claimed','submitted','approved','done']
     assert isinstance(t.get('paid',False),bool)
     ids.append(t['id'])
    assert len(ids)==len(set(ids))
   except (ValueError,TypeError,AssertionError,KeyError):st.error('올바른 백업 파일이 아닙니다.')
   else:d=v;save()
 st.caption('공용 공간: 주소를 아는 사람은 열람·수정 가능해요. 서버 초기화 시 데이터가 사라질 수 있으니 백업해주세요.')
 st.stop()
actor=st.selectbox('사용자',d['members'],label_visibility='collapsed',key='active_member',on_change=lambda:st.session_state.update(idx=0))
now=datetime.now(timezone(timedelta(hours=9)));day=now.date().isoformat()
if page=='오늘':
 st.markdown('<div class="heading">오늘, 우리집은</div>',unsafe_allow_html=True)
 entries=d['days'].get(day,{})
 count=sum(entries.get(n,{}).get('meal')=='먹어요' for n in d['members'])
 unknown=sum(entries.get(n,{}).get('meal') not in ['먹어요','안 먹어요'] for n in d['members'])
 today_events=[e for e in d['events'] if e['date']==day]
 panel(now.strftime('%m월 %d일')+f' · 일정 {len(today_events)}개 · 저녁 식사',f'<div class="big">{count}명 함께 먹어요</div><div class="small">미정·미응답 {unknown}명</div>')
 current=entries.get(actor,{})
 with st.form('meal'):
  opts=['아직 몰라요','먹어요','안 먹어요'];old=current.get('meal','아직 몰라요')
  meal=st.radio('오늘 저녁',opts,index=opts.index(old) if old in opts else 0,horizontal=True)
  times=['미정','집에 있어요']+[f'{h:02d}:{m:02d}' for h in range(24) for m in [0,30]]
  oldtime=current.get('arrival','미정')
  arrival=st.selectbox('귀가',times,index=times.index(oldtime) if oldtime in times else 0)
  if st.form_submit_button('내 상태 저장',type='primary',use_container_width=True):d['days'].setdefault(day,{})[actor]={'meal':meal,'arrival':arrival};save()
 n=pager(d['members'],'family')
 if n:
  e=entries.get(n,{});st.caption(f"{n} · 저녁 {e.get('meal','미응답')} · 귀가 {e.get('arrival','미정')}")
elif page=='부탁':
 st.markdown('<div class="heading">오는 길에, 부탁해</div>',unsafe_allow_html=True)
 if st.session_state.compose:
  with st.form('new'):
   title=st.text_input('어떤 부탁인가요?',max_chars=70,placeholder='우유 1개 사다 주기')
   st.caption('작은 부탁도 나누면 가벼워져요.')
   if st.form_submit_button('부탁 등록하기',type='primary',use_container_width=True):
    if title.strip():
     d['tasks'].append({'id':uuid.uuid4().hex,'title':title.strip(),'owner':'','created':actor,'reward':0,'status':'open','paid':False,'done':False,'due':day,'category':'부탁'});st.session_state.compose=False;save()
    else:st.caption('부탁할 내용을 적어주세요.')
  if st.button('취소',use_container_width=True):st.session_state.compose=False;st.rerun()
 else:
  if st.button('+ 새로운 부탁',type='primary',use_container_width=True):st.session_state.compose=True;st.rerun()
  filt=st.radio('목록',['진행 중','승인 대기','완료'],horizontal=True,label_visibility='collapsed',on_change=lambda:st.session_state.update(idx=0))
  tasks=[t for t in d['tasks'] if (t['status'] in ['open','claimed'] if filt=='진행 중' else t['status']=='submitted' if filt=='승인 대기' else t['status'] in ['approved','done'])]
  t=pager(list(reversed(tasks)),'task')
  if t:
   labels={'open':'참여 가능','claimed':'수행 중','submitted':'확인 기다리는 중','approved':'승인 완료','done':'이전 완료 기록'}
   panel(t['created']+'의 부탁 · '+labels[t['status']],'<div class="task-title">'+escape(t['title'])+'</div><div class="small" style="margin-top:18px">담당: '+escape(t['owner'] or '아직 없어요')+'</div>')
   if t['status']=='open':
    if t['created']!=actor:
     if st.button('내가 할게',type='primary',use_container_width=True):t['owner']=actor;t['status']='claimed';save()
    else:st.caption('다른 가족이 맡을 때까지 기다려주세요.')
   if t['status']=='claimed' and t['owner']==actor:
    a,b=st.columns(2)
    if a.button('완료했어요',type='primary',use_container_width=True):t['status']='submitted';save()
    if b.button('맡기 취소',use_container_width=True):t['owner']='';t['status']='open';save()
   if t['status']=='submitted' and t['created']==actor:
    a,b=st.columns(2)
    if a.button('승인',type='primary',use_container_width=True):t['status']='approved';t['done']=True;save()
    if b.button('다시 부탁',use_container_width=True):t['status']='claimed';save()
elif page=='일정':
 st.markdown('<div class="heading">함께 챙기는 날들</div>',unsafe_allow_html=True)
 if st.session_state.compose:
  with st.form('event_new'):
   title=st.text_input('일정 이름',max_chars=50,placeholder='현장학습 · 병원 · 가족 저녁')
   a,b=st.columns(2)
   when=a.date_input('날짜',value=now.date())
   who=b.selectbox('누구의 일정', ['가족 모두']+d['members'])
   time=st.text_input('시간 · 장소',max_chars=60,placeholder='오전 9시 · 학교 앞')
   prep=st.text_input('준비물',max_chars=120,placeholder='도시락, 물, 체육복 (쉼표로 구분)')
   if st.form_submit_button('일정 저장',type='primary',use_container_width=True):
    if title.strip():
     d['events'].append({'id':uuid.uuid4().hex,'title':title.strip(),'date':when.isoformat(),'who':who,'time':time.strip(),'items':[{'text':x.strip(),'done':False} for x in prep.split(',') if x.strip()]});st.session_state.compose=False;save()
    else:st.caption('일정 이름을 적어주세요.')
  if st.button('취소',use_container_width=True):st.session_state.compose=False;st.rerun()
 else:
  if st.button('+ 일정 추가',type='primary',use_container_width=True):st.session_state.compose=True;st.rerun()
  filt=st.radio('기간',['오늘','내일','이번 주','전체'],horizontal=True,label_visibility='collapsed',on_change=lambda:st.session_state.update(idx=0))
  tomorrow=(now.date()+timedelta(days=1)).isoformat();end=(now.date()+timedelta(days=6-now.weekday())).isoformat()
  events=sorted([e for e in d['events'] if (e['date']==day if filt=='오늘' else e['date']==tomorrow if filt=='내일' else day<=e['date']<=end if filt=='이번 주' else True)],key=lambda e:(e['date'],e.get('time','')))
  e=pager(events,'events')
  if e:
   delta=(datetime.fromisoformat(e['date']).date()-now.date()).days
   badge='TODAY' if delta==0 else f'D−{delta}' if delta>0 else f'{-delta}일 전'
   panel(e['date']+' · '+e['who'], '<div class="eventbadge">'+badge+'</div><div class="task-title">'+escape(e['title'])+'</div><div class="small" style="margin-top:10px">'+escape(e.get('time') or '시간·장소 미정')+'</div>')
   items=e.get('items',[])
   if items:
    j=st.number_input('준비물 번호',min_value=1,max_value=len(items),value=1,step=1,key='item_'+e['id'])-1
    item=items[j]
    checked=st.checkbox(item['text'],value=item['done'],key=e['id']+str(j))
    if checked!=item['done']:item['done']=checked;save()
    if st.button('이 준비물 부탁하기',use_container_width=True):
     link=e['id']+':'+str(j)
     if not any(t.get('event_link')==link for t in d['tasks']):
      d['tasks'].append({'id':uuid.uuid4().hex,'title':item['text']+' 챙기기 · '+e['title'],'owner':'','created':actor,'reward':0,'paid':False,'status':'open','done':False,'event_link':link,'due':e['date']});save()
     else:st.caption('이미 부탁에 등록되어 있어요.')
   if st.button('일정 삭제',key='delete_'+e['id']):st.session_state.delete_event=e['id']
   if st.session_state.get('delete_event')==e['id']:
    if st.button('삭제 확정',type='primary'):d['events']=[x for x in d['events'] if x['id']!=e['id']];st.session_state.pop('delete_event',None);save()
