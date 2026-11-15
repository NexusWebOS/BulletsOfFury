"""Structural checks only; cannot approve artwork or combat feel."""
import argparse,json
from pathlib import Path

def check(plan):
    assert plan['body_unit']>0 and len(plan['root'])==2,'Missing calibration'
    moves=plan['moves'];ids=[m['id'] for m in moves]
    assert len(ids)==len(set(ids)),'Duplicate IDs'
    report=[]
    for m in moves:
        total=0;active=False
        assert m['frames'],'Empty move'
        for f in m['frames']:
            ms=f['duration_ms'];assert isinstance(ms,int) and ms>0,'Positive integer milliseconds required'
            total+=ms;phase=f['phase'];assert phase in ('startup','active','recovery'),'Unknown phase'
            boxes=f.get('hitboxes',[])
            assert not boxes or phase=='active','Hitbox outside active phase'
            if phase=='active':active=True;assert boxes,'Active frame without hitbox'
            for b in boxes:
                assert b['id'] and b['damage']>0,'Hit ID/damage required'
                assert len(b['rect'])==4 and min(b['rect'][2:])>0,'Invalid box'
        assert active,'Move has no active phase'
        c=m.get('cancel')
        if c:
            assert 0<=c['from_ms']<c['to_ms']<=total,'Cancel outside move'
            assert c['next'] and all(n in ids for n in c['next']),'Unknown successor'
        report.append({'id':m['id'],'drawings':len(m['frames']),'total_ms':total})
    return {'moves':report,'visual_and_runtime_review_required':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('plan',type=Path);a=p.parse_args()
    print(json.dumps(check(json.loads(a.plan.read_text(encoding='utf-8'))),indent=2))
