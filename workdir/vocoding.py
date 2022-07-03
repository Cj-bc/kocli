# References:
# https://qiita.com/ohtaman/items/84426cee09c2ba4abc22#声を変換してみる
# https://pysoundfile.readthedocs.io/en/latest/
# https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder/blob/master/pyworld/pyworld.pyx
import pyworld as pw
import soundfile as sf
import numpy as np
import numpy.typing as npt
from typing import Callable
import click

import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), "test-rec.wav")
OUT_FILE = os.path.join(os.path.dirname(__file__), "converted.wav")


def identical(a):
    """Return given value. Same as 'id' function of Haskell"""
    return a

def convert_mono(mono_audio: npt.NDArray[float], samplerate: float,
                 f0_converter: Callable[float, float] = identical,
                 sp_converter: Callable[float, float] = identical):
    """Convert monaural audio

    Parameters:
        mono_audio:
            numpy array of audio stream.
        samplerate:
            samplerate of given audio.

        f0_converter:
            The function to modify f0.

        sp_converter:
            The function to modify sp.
    """
    # https://stackoverflow.com/questions/26778079/valueerror-ndarray-is-not-c-contiguous-in-cython
    f0, sp, ap = pw.wav2world(mono_audio.copy(order='C'), samplerate)
    converted_sp = np.zeros_like(sp)

    for f in range(converted_sp.shape[1]):
        converted_sp[:, f] = sp[:, sp_converter(f)]

    return pw.synthesize(f0_converter(f0), converted_sp, ap, samplerate)

@click.command()
@click.option("--output", default=OUT_FILE, help="Output wav file")
@click.option("--f0", default=2, help="The value to multipy with f0")
@click.option("--sp", default=5/6, help="The value to multipy with sp")
@click.argument("file")
def run(output, f0, sp, file):
    """Run Voice changer"""
    data, samplerate = sf.read(file)

    ch1 = convert_mono(data[:, 0], samplerate, lambda f0: f0*f0, lambda sp_v: int(sp_v*sp))
    ch2 = convert_mono(data[:, 1], samplerate, lambda f0: f0*f0, lambda sp_v: int(sp_v*sp))
    
    result = np.stack((ch1, ch2), axis=1)
    sf.write(output, result, samplerate)

if __name__ == '__main__':
    run()

