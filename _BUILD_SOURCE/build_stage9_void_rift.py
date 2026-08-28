"""Build Stage 9's seamless 680px-wide void/water background master."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_ART_SOURCES" / "stage9_void_rift" / "void_rift_water_generated_v1.png"
OUTPUT = ROOT / "assets" / "game" / "stage9_void_rift" / "void_rift_water_loop_680x4096.png"


def main() -> None:
    with Image.open(SOURCE) as raw:
        source = raw.convert("RGB")
    half = source.resize((680, 2048), Image.Resampling.LANCZOS)
    master = Image.new("RGB", (680, 4096))
    master.paste(half, (0, 0))
    master.paste(half.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, 2048))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    master.save(OUTPUT, optimize=True)
    print(f"built {OUTPUT.relative_to(ROOT)}: {master.width}x{master.height}")


if __name__ == "__main__":
    main()
