"""Final audio: voice + music (ducked under voice) + SFX → loudness-normalized stereo WAV.

Levels live here; tune per video with attributes on Video (video.music_db, video.sfx_db).
"""
import subprocess

from . import sfx as S

MUSIC_DB = -19.0     # music bed level before ducking (a real, mastered track)
GEN_DB = -13.0       # generated score (music.py) is mixed quieter than a mastered track → less cut
SFX_DB = -7.0        # SFX bus level
DUCK = "threshold=0.025:ratio=6:attack=20:release=380:makeup=1"
LOUDNESS = "loudnorm=I=-14:TP=-1.0:LRA=11"   # TikTok/Reels target


def build_mix(project, video, out_wav):
    dur = video.duration
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    sfx_wav = out_wav.parent / "sfx.wav"
    S.write_wav(sfx_wav, S.track(video.all_cues(), dur))
    voice, music = project.voice(), project.music()
    generated = False
    if not music:
        from .music import write_music
        music = write_music(video, project.slug, out_wav.parent / "music_gen.wav")
        generated = music is not None
    music_db = getattr(video, "music_db", GEN_DB if generated else MUSIC_DB)
    sfx_db = getattr(video, "sfx_db", SFX_DB)

    args = ["ffmpeg", "-v", "error", "-y"]
    filt, mixin = [], []
    idx = 0
    if voice:
        args += ["-i", str(voice)]
        ms = int(round(project.pre_roll * 1000))         # opt-in pre-roll (brand sting): voice starts later
        delay = f"adelay={ms}:all=1," if ms else ""
        filt.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,{delay}apad,atrim=0:{dur}[vo0]")
        filt.append("[vo0]asplit=2[vo][vsc]")
        mixin.append("[vo]")
        idx += 1
    if music:
        args += (["-i", str(music)] if generated else ["-stream_loop", "-1", "-i", str(music)])
        mf = (f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},"
              f"volume={music_db}dB,afade=t=in:d=0.8,afade=t=out:st={max(0, dur - 2.5)}:d=2.5")
        if voice:
            filt.append(mf + "[mus]")
            filt.append(f"[mus][vsc]sidechaincompress={DUCK}[duck]")
            mixin.append("[duck]")
        else:
            filt.append(mf + "[duck]")
            mixin.append("[duck]")
        idx += 1
    elif voice:
        filt.append("[vsc]anullsink")
    args += ["-i", str(sfx_wav)]
    filt.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={sfx_db}dB[fx]")
    mixin.append("[fx]")
    filt.append(f"{''.join(mixin)}amix=inputs={len(mixin)}:normalize=0:duration=longest,"
                f"atrim=0:{dur},{LOUDNESS},aresample=48000[out]")
    args += ["-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)]
    subprocess.run(args, check=True)
    print(f"✓ {out_wav}  (voice={'yes' if voice else 'no'}, music={'generated' if generated else ('yes' if music else 'no')}, "
          f"sfx={len(video.all_cues())} cues)")
    return out_wav
