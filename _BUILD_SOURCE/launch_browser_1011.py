"""Launch the user's local arcade window fullscreen; no profile mutation."""
import os,sys,subprocess,time,shutil
from pathlib import Path
def browser_path():
    roots=[os.environ.get('PROGRAMFILES',''),os.environ.get('PROGRAMFILES(X86)',''),os.environ.get('LOCALAPPDATA','')]
    for suffix in ['Microsoft/Edge/Application/msedge.exe','Google/Chrome/Application/chrome.exe']:
        for root in roots:
            p=Path(root)/suffix
            if root and p.is_file():return str(p)
    return shutil.which('msedge') or shutil.which('chrome')
if __name__=='__main__':
    browser=browser_path()
    if '--check' in sys.argv:
        print('Fullscreen browser:',browser or 'default browser fallback');sys.exit(0)
    port=int(sys.argv[1]);assert 8765<=port<=8772
    url=f'http://127.0.0.1:{port}/index.html?arcade=fullscreen'
    time.sleep(.9)
    if browser:subprocess.Popen([browser,'--new-window','--start-fullscreen',url],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    else:os.startfile(url)
