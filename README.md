# Anime4K Python

Python wrapper of Anime4K GLSL shaders achieved with FFmpeg and libplacebo.

## Usages

```
from anime4k_python import Anime4K

anime4k = Anime4K(mode="A")
anime4k.process_video(
    "input.mp4",
    "output.mp4",
    1280,
    720,
    scale=2,
)
```
