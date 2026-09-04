#!/usr/bin/env python3
"""Live canvas QA for every Gravity Mode weapon tier and its gameplay contracts."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "space_weapons_i_v_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve()
    page_errors: list[str] = []
    console_errors: list[str] = []
    report: dict = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
        page = browser.new_page(viewport={"width": 1040, "height": 1120}, device_scale_factor=1)
        page.on("pageerror", lambda err: page_errors.append(str(err)))
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.goto(f"http://127.0.0.1:{server.server_address[1]}/index.html", wait_until="load", timeout=60_000)
        page.wait_for_function("() => typeof spaceLaserFire==='function' && typeof spaceVolleyLocks==='function'", timeout=60_000)
        page.wait_for_function("() => (window.__bofFrames|0)>4", timeout=45_000)
        page.evaluate("""() => {
          beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999999;
          player.x=worldWidth()/2;player.y=VH-82;snapCamToPlayer();
          enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
          stagePlan=[];waveIdx=999;boss=null;bossActive=false;subBoss=null;subBossActive=false;
          gravityModeRetain();gravityMode.phase='active';run.gravityShipReady=true;
          /* Freeze gameplay but keep the real renderer running. Mechanics below are advanced
             explicitly, one authored 60 Hz step at a time, so screenshots cannot race the loop. */
          window.__spaceQaUpdate=updatePlay;updatePlay=function(){};
        }""")
        page.wait_for_function("() => SPACE_ATLAS_FRAMES && XART.rdy('ngm_space_atlas')", timeout=45_000)
        canvas = page.locator("#screen")

        atlas = page.evaluate("""() => {
          const missing=[],tiers=[];
          for(let lv=1;lv<=5;lv++){
            const keys=['laser_icon_'+lv,'laser_'+lv+'_pulse_long','laser_'+lv+'_pulse_short',
              'shadow_icon_'+lv,'volley_icon_'+lv,'volley_'+lv+'_split'];
            for(let i=0;i<4;i++){keys.push('laser_'+lv+'_muzzle_'+i);keys.push('volley_'+lv+'_trail_'+i);}
            for(let i=0;i<3;i++){keys.push('shadow_'+lv+'_charge_'+i);keys.push('volley_'+lv+'_missile_'+i);}
            for(let i=0;i<4;i++)keys.push('laser_'+lv+'_impact_'+i);
            for(let i=0;i<6;i++){keys.push('shadow_'+lv+'_flight_'+i);
              keys.push('shadow_'+lv+'_impact_'+i);keys.push('volley_'+lv+'_impact_'+i);}
            const miss=keys.filter(k=>!spaceAtlasRect(k));missing.push(...miss);tiers.push({lv,count:keys.length,missing:miss});
          }
          return {tiers,missing};
        }""")

        # Render the exact 15 production icons from the one runtime atlas.
        page.evaluate("""() => {
          const old=document.getElementById('space-icon-proof');if(old)old.remove();
          const c=document.createElement('canvas');c.id='space-icon-proof';c.width=920;c.height=500;
          c.style.cssText='position:fixed;left:0;top:0;z-index:999999;background:#070b13';document.body.appendChild(c);
          const g=c.getContext('2d'),rows=[['LASER CANNON','space_laser_icon_'],['SHADOW ORB','space_shadow_icon_'],['VOLLEY MISSILES','space_volley_icon_']];
          g.imageSmoothingEnabled=false;g.fillStyle='#f1bd4e';g.font='bold 23px monospace';g.fillText('GRAVITY MODE SPACE ARMORY - PRODUCTION ATLAS',25,34);
          rows.forEach((row,ri)=>{const y=115+ri*135;g.fillStyle='#dce8ff';g.font='bold 18px monospace';g.textAlign='left';g.fillText(row[0],25,y+8);
            for(let lv=1;lv<=5;lv++){const x=285+(lv-1)*125;spaceAtlasIconBlit(g,row[1]+lv,x,y,82,true);
              g.fillStyle='#91a6c5';g.font='bold 14px monospace';g.textAlign='center';g.fillText(['I','II','III','IV','V'][lv-1],x,y+58);}});
        }""")
        page.locator("#space-icon-proof").screenshot(path=str(OUT / "01_space_weapon_icons_I_V.png"))
        page.evaluate("()=>document.getElementById('space-icon-proof').remove()")

        laser = page.evaluate("""() => {
          const tiers=[];enemies.length=0;boss=null;bossActive=false;subBoss=null;subBossActive=false;
          for(let lv=1;lv<=5;lv++){
            run.spaceWeapon=0;run.spaceLevels[0]=lv;run.wlevel=1;pBullets.length=0;spaceLaserFire();
            const born=pBullets.map(b=>({side:b.side,pulse:b.pulse,x:b.x,y:b.y,delay:b._launchDelay,mx:b._muzzleX,my:b._muzzleY}));
            pBullets.forEach(b=>spaceBulletTick(b,1/60));
            const left=pBullets.filter(b=>b.side<0).sort((a,b)=>a.pulse-b.pulse),right=pBullets.filter(b=>b.side>0).sort((a,b)=>a.pulse-b.pulse);
            tiers.push({lv,count:pBullets.length,damage:pBullets[0].dmg,speed:-pBullets[0].vy,
              icon:spaceWeaponIconKey(),hudLevel:spaceWeaponLevel(),born,
              leftY:left.map(b=>b.y),rightY:right.map(b=>b.y),
              leftGaps:left.slice(1).map((b,i)=>Math.abs(b.y-left[i].y)),
              rightGaps:right.slice(1).map((b,i)=>Math.abs(b.y-right[i].y))});
          }
          return {colors:SPACE_LASER_COL.slice(),tiers};
        }""")

        # Freeze a real Level-V burst after 12 explicit frames: two turret columns, six visible beats.
        page.evaluate("""() => {run.spaceWeapon=0;run.spaceLevels[0]=5;run.wlevel=1;pBullets.length=0;spaceLaserFire();
          for(let f=0;f<12;f++)for(const b of pBullets)spaceBulletTick(b,1/60);player._spaceMuzzle=0.09;}""")
        page.wait_for_timeout(80)
        canvas.screenshot(path=str(OUT / "02_laser_cannon_V_six_twin_beats.png"))

        shadow = page.evaluate("""() => {
          const tiers=[];enemies.length=0;pBullets.length=0;
          for(let lv=1;lv<=5;lv++){
            run.spaceWeapon=1;run.spaceLevels[1]=lv;run.wlevel=1;
            pBullets.length=0;spaceShadowRelease(0.18);const tap=pBullets[0];
            const t={size:tap.w,damage:tap.dmg,speed:-tap.vy,radius:tap.blastRad,pierceAt:tap.pierceAt,full:tap.full};
            pBullets.length=0;spaceShadowRelease(1.55);const full=pBullets[0];
            tiers.push({lv,icon:spaceWeaponIconKey(),hudLevel:spaceWeaponLevel(),tap:t,
              full:{size:full.w,damage:full.dmg,speed:-full.vy,radius:full.blastRad,pierceAt:full.pierceAt,full:full.full}});
          }
          return {tiers};
        }""")
        page.evaluate("""() => {run.spaceWeapon=1;run.spaceLevels[1]=5;run.wlevel=1;pBullets.length=0;
          run._spaceShadowCharge=1.55;run._spaceShadowHeld=true;}""")
        page.wait_for_timeout(80)
        canvas.screenshot(path=str(OUT / "03_shadow_orb_V_full_charge.png"))
        page.evaluate("""() => {run._spaceShadowCharge=0;run._spaceShadowHeld=false;spaceShadowRelease(1.55);
          for(let f=0;f<17;f++)spaceBulletTick(pBullets[0],1/60);}""")
        page.wait_for_timeout(80)
        canvas.screenshot(path=str(OUT / "04_shadow_orb_V_flight.png"))
        page.evaluate("""() => {const b=pBullets.find(q=>q.kind==='shadowOrb');if(b)spaceShadowBlast(b);}""")
        page.wait_for_timeout(80)
        canvas.screenshot(path=str(OUT / "05_shadow_orb_V_blast.png"))

        volley = page.evaluate("""() => {
          run.spaceWeapon=0;run.spaceLevels[2]=5;run.wlevel=1;pBullets.length=0;
          const ox=player.x,oy=player.y;
          enemies.length=0;
          enemies.push({qa:'left',x:ox-115,y:oy-330,w:1,h:1,hp:999,maxhp:999,dead:false},
                       {qa:'center',x:ox,y:oy-350,w:1,h:1,hp:999,maxhp:999,dead:false},
                       {qa:'right',x:ox+115,y:oy-330,w:1,h:1,hp:999,maxhp:999,dead:false});
          spaceVolleyFire();const seed=pBullets[0];for(let f=0;f<7;f++)spaceBulletTick(seed,1/60);
          const missiles=pBullets.filter(b=>b.kind==='spaceVolley');
          const tracks=missiles.map(b=>[{x:b.x,y:b.y}]);
          for(let f=0;f<24;f++)missiles.forEach((b,i)=>{spaceBulletTick(b,1/60);tracks[i].push({x:b.x,y:b.y});});
          return {count:missiles.length,icon:spaceVolleyIconKey(),hudLevel:spaceVolleyLevel(),
            locks:missiles.map(b=>b._target&&b._target.qa),phases:missiles.map(b=>b._phase),
            tracks:tracks.map((tr,i)=>({side:missiles[i].side,minX:Math.min(...tr.map(p=>p.x))-ox,
              maxX:Math.max(...tr.map(p=>p.x))-ox,startX:tr[0].x-ox,endX:tr[tr.length-1].x-ox})),
            finite:{near:!!spaceAcquire({x:ox,y:oy},440),behind:!!spaceAcquire({x:ox,y:oy-500},440)}};
        }""")
        page.evaluate("""() => {enemies.length=0;pBullets.length=0;run.spaceWeapon=0;run.spaceLevels[2]=5;spaceVolleyFire();
          const seed=pBullets[0];for(let f=0;f<7;f++)spaceBulletTick(seed,1/60);
          const m=pBullets.filter(b=>b.kind==='spaceVolley');for(let f=0;f<17;f++)m.forEach(b=>spaceBulletTick(b,1/60));}""")
        page.wait_for_timeout(80)
        canvas.screenshot(path=str(OUT / "06_volley_missiles_V_criss_cross.png"))

        pickups = page.evaluate("""() => {
          run.spaceWeapon=0;run.spaceLevels=[1,1,1];run.wlevel=1;
          const mapping=[],states=[];
          for(let wtype=0;wtype<6;wtype++){
            const p={kind:'weapon',wtype,x:player.x,y:player.y};mapping.push(spaceWeaponPickupIndex(p));applyPowerup(p);
            states.push({wtype,active:run.spaceWeapon,level:spaceWeaponLevel(),passive:spaceVolleyLevel(),levels:run.spaceLevels.slice(),name:spaceWeaponName(),icon:spaceWeaponIconKey()});
          }
          return {mapping,states};
        }""")

        hud = page.evaluate("""() => {run.spaceWeapon=1;run.spaceLevels[1]=4;run.wlevel=1;
          return {display:weaponDisplayName(run.weapon),icon:weaponIconKey(run.weapon,run.wlevel),level:spaceWeaponLevel(),rawGroundLevel:run.wlevel};}""")

        isolation = page.evaluate("""() => {
          special=null;run.stage=4;run.spaceMode=false;run._groundLoadout=null;
          run.weapon=4;run.wlevel=3;run.wlevels=[0,0,0,0,3,0];run.wvars=[null,null,null,null,'flamethrower',null];run.missileLevel=4;
          run.stage=5;spaceModeStage(5);const locked={space:spaceWeaponsActive(),weapon:run.weapon,missiles:run.missileLevel};
          run.spaceLevels=[5,4,3];run.spaceWeapon=1;run.wlevel=3;
          run.stage=6;spaceModeStage(6);const restored={space:run.spaceMode,weapon:run.weapon,wlevel:run.wlevel,missiles:run.missileLevel,variant:run.wvars[4]};
          run.stage=9;spaceModeStage(9);const retained={space:spaceWeaponsActive(),levels:run.spaceLevels.slice(),active:run.spaceWeapon,groundMissiles:run.missileLevel};
          return {locked,restored,retained};
        }""")

        specials = page.evaluate("""() => {
          run.stage=5;run.spaceMode=true;run.spaceWeapon=0;run.spaceLevels[0]=5;run.wlevel=5;
          run.pilot='maverick';special={pilot:'maverick',t:15,dur:15,mavCharging:false};pBullets.length=0;pShoot();
          const during=pBullets.map(b=>b.kind);special=null;pBullets.length=0;pShoot();const ordinary=pBullets.map(b=>b.kind);
          return {during,ordinary};
        }""")

        report = {
            "atlas": atlas,
            "laser": laser,
            "shadow": shadow,
            "volley": volley,
            "pickups": pickups,
            "hud": hud,
            "loadoutIsolation": isolation,
            "specialPrecedence": specials,
            "pageErrors": page_errors,
            "consoleErrors": console_errors,
        }
        browser.close()

    server.shutdown()
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    assert not page_errors and not console_errors
    assert not atlas["missing"]
    assert all(t["count"] == 12 and len(set(round(y, 4) for y in t["leftY"])) == 6 for t in laser["tiers"])
    assert all(min(t["leftGaps"] + t["rightGaps"]) > 0.5 for t in laser["tiers"])
    assert laser["colors"] == ["#ff972b", "#39a4ff", "#48e36c", "#f5f7ff", "#ff4848"]
    assert all(t["full"]["damage"] > t["tap"]["damage"] and t["full"]["radius"] > t["tap"]["radius"] for t in shadow["tiers"])
    assert all(shadow["tiers"][i]["full"]["damage"] < shadow["tiers"][i + 1]["full"]["damage"] for i in range(4))
    assert volley["count"] == 3 and len(set(volley["locks"])) == 3
    assert volley["locks"] == ["right", "center", "left"]
    assert volley["tracks"][0]["minX"] < 0 < volley["tracks"][0]["maxX"]
    assert volley["tracks"][2]["minX"] < 0 < volley["tracks"][2]["maxX"]
    assert volley["finite"] == {"near": True, "behind": False}
    assert pickups["mapping"] == [0, 1, 2, 0, 1, 2]
    assert hud == {"display": "SHADOW ORB", "icon": "space_shadow_icon_4", "level": 4, "rawGroundLevel": 1}
    assert isolation["locked"] == {"space": True, "weapon": 0, "missiles": 0}
    assert isolation["restored"] == {"space": False, "weapon": 4, "wlevel": 3, "missiles": 4, "variant": "flamethrower"}
    assert isolation["retained"] == {"space": True, "levels": [5, 4, 3], "active": 1, "groundMissiles": 0}
    assert specials["during"] == ["venomx"] and specials["ordinary"] == ["spaceLaser"] * 12


if __name__ == "__main__":
    main()
