"""Open the local enemy guide once its server is listening."""
import os,sys,time,urllib.request,webbrowser
port=int(sys.argv[1])
if not 8765<=port<=8772:raise SystemExit('Invalid local game port')
url=f'http://127.0.0.1:{port}/enemy-atlas.html'
for _ in range(40):
    try:
        with urllib.request.urlopen(url,timeout=.4) as response:
            if response.status==200:break
    except (OSError,TimeoutError):time.sleep(.2)
if os.name=='nt':os.startfile(url)
else:webbrowser.open(url)
