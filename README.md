# VRC-OSC-ParticlePrinter

Prints an image in-game using a particle system, driven over OSC.

`osc-picasso.py` reads an image, resizes it to 512 wide (keeping aspect) x 128 tall, then walks the pixels and sends each one's position and color to VRChat as avatar params. The `Painter` prefab picks those up and paints them with a particle system.

## Setup

- Get [VRCFury](https://vrcfury.com/), drag `Unity/Painter.prefab` onto your avatar, upload as normal. VRCFury handles the params (`PaintEnabled`, `PosX`, `PosY`, `ColorR/G/B/A`) for you.
- Enable OSC in VRChat (Action Menu > Options > OSC > Enabled).
- `pip install python-osc Pillow`

## Usage

```
python osc-picasso.py --img image.png
```

Loops forever, restarting from the top each pass. Ctrl+C to stop.

Flags:

| Flag     | Default       | What it does        |
|----------|---------------|----------------------|
| `--img`  | `image.png`   | Image to print       |
| `--ip`   | `127.0.0.1`   | OSC server ip        |
| `--port` | `9000`        | OSC server port      |
