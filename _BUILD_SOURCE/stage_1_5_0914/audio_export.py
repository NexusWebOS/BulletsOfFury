"""Use the game exporter with Chromium's overridden buffer-source start method pinned too."""
import render_audio as inherited
audio_module_source=inherited.audio_module_source
write_wav_float=inherited.write_wav_float
RENDER=inherited.RENDER
old='    const proxy = new Proxy(off, {get: function(t, p){'
new='''    /* AudioBufferSourceNode owns an overload of start; patching its parent does not pin noise.
       Samples and loops above are already scheduled. Only game-module noise is pinned here. */
    const _bufferStart = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function(when, offset, duration){
      if (window.__synthOn && this.context === off) when = Math.max(when || 0, window.__tOff);
      if (duration !== undefined) return _bufferStart.call(this, when, offset, duration);
      if (offset !== undefined) return _bufferStart.call(this, when, offset);
      return _bufferStart.call(this, when);
    };
    const proxy = new Proxy(off, {get: function(t, p){'''
assert RENDER.count(old)==1;RENDER=RENDER.replace(old,new,1)
old='    AudioScheduledSourceNode.prototype.start = _start;'
new=old+'\n    AudioBufferSourceNode.prototype.start = _bufferStart;'
assert RENDER.count(old)==1;RENDER=RENDER.replace(old,new,1)
