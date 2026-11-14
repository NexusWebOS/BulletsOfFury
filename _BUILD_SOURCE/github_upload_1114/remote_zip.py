import io,urllib.request,urllib.error,re,struct,json,time
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):return None
class PartsReader(io.RawIOBase):
 def __init__(self,parts,session=None):
  self.parts=parts;self.session=session;self.pos=0;self.length=sum(p['size']for p in parts);self.links={};self.cache={};self.received=0
 def readable(self):return True
 def seekable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.length+offset;assert self.pos>=0;return self.pos
 def link(self,i):
  if i in self.links and time.monotonic()-self.links[i][0]<180:return self.links[i][1]
  p=self.parts[i];headers={'User-Agent':'BOF-build-verifier','Accept':'application/octet-stream'}
  if self.session and p.get('url','').startswith('https://api.github.com/'):
   url=p['url'];headers['Authorization']=self.session.headers['Authorization']
  else:url=p['browser_download_url']
  opener=urllib.request.build_opener(NoRedirect())
  try:
   r=opener.open(urllib.request.Request(url,headers=headers),timeout=60);target=url;r.close()
  except urllib.error.HTTPError as e:
   if e.code not in [301,302,303,307,308]:raise RuntimeError('Asset redirect HTTP '+str(e.code))
   target=e.headers['Location'];e.close()
  self.links[i]=(time.monotonic(),target);return target
 def piece(self,i,start,n):
  # Range responses are bounded and never retain signed download URLs on disk.
  url=self.link(i);req=urllib.request.Request(url,headers={'User-Agent':'BOF-build-verifier','Range':f'bytes={start}-{start+n-1}'})
  with urllib.request.urlopen(req,timeout=120)as r:
   assert r.status==206,'Release host ignored the requested byte range'
   data=r.read(n+1);assert len(data)==n,(len(data),n);self.received+=len(data);return data
 def read(self,n=-1):
  if n<0:n=self.length-self.pos
  n=min(n,self.length-self.pos);out=[]
  while n>0:
   offset=0
   for i,p in enumerate(self.parts):
    if self.pos<offset+p['size']:break
    offset+=p['size']
   at=self.pos-offset;block=at//(1024*1024);key=(i,block)
   if key not in self.cache:
    begin=block*1024*1024;self.cache[key]=self.piece(i,begin,min(1024*1024,p['size']-begin))
    while len(self.cache)>12:self.cache.pop(next(iter(self.cache)))
   data=self.cache[key];inside=at-block*1024*1024;take=min(n,len(data)-inside);assert take>0;out.append(data[inside:inside+take]);self.pos+=take;n-=take
  return b''.join(out)
