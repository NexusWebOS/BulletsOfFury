"""Open the standalone Overdrive server in the user's fullscreen browser window."""
from pathlib import Path
import os, shutil, subprocess, sys, time

def browser_path():
    roots=[os.environ.get('PROGRAMFILES',''),os.environ.get('PROGRAMFILES(X86)',''),os.environ.get('LOCALAPPDATA','')]
    for suffix in ['Microsoft/Edge/Application/msedge.exe','Google/Chrome/Application/chrome.exe']:
        for directory in roots:
            candidate=Path(directory)/suffix
            if directory and candidate.is_file():return str(candidate)
    return shutil.which('msedge') or shutil.which('chrome')

def command(port):
    assert 1<=port<=65535
    url=f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=1&build=overdrive1013-yuri-motion-r1'
    browser=browser_path()
    return ([browser,'--new-window','--start-fullscreen',url] if browser else None),url

if __name__=='__main__':
    port=int(next((a for a in sys.argv[1:] if a.isdigit()),'8778'))
    args,url=command(port)
    if '--check' in sys.argv:
        print({'browser':args[0] if args else 'system default','flags':args[1:-1] if args else [],'url':url});sys.exit(0)
    time.sleep(.9)
    if args:subprocess.Popen(args,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    else:os.startfile(url)
