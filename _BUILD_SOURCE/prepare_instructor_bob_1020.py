from pathlib import Path
from PIL import Image
import shutil,urllib.request,json
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');A=R/'_ART_SOURCES/instructor_bob_1020';A.mkdir(exist_ok=True)
for d in ['references','returned','parts']:(A/d).mkdir(exist_ok=True)
for name in ['1.jpg','2.jpg']:shutil.copy2(Path(r'C:\Users\Mike\Desktop')/name,A/'references'/name)
src=Path(r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-3a46b50b-4537-4f6c-a9a0-d3df7847b6a4.png')
shutil.copy2(src,A/'returned/instructor-portraits.png')
url='https://api.pixellab.ai/mcp/images/cd10bd5f-a02f-4fc3-86c9-d4ff5b0bef8c/download?index=0'
with urllib.request.urlopen(url,timeout=90) as response:(A/'returned/bob.png').write_bytes(response.read())
print(json.dumps({'portrait':Image.open(src).size,'bob':Image.open(A/'returned/bob.png').size,'source':str(A)}))
