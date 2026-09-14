from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets" / "game" / "atlas" / "nca_56.png"
OUTPUT = Path(__file__).resolve().parent / "storm_sovereign_reference.png"


def main() -> None:
    with Image.open(SOURCE) as source:
        # Registered atlas tuple: mbs6_master = [56, 772, 1158, 384, 384].
        frame = source.crop((772, 1158, 772 + 384, 1158 + 384)).convert("RGBA")
        frame.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
