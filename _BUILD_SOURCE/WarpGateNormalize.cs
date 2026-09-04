using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;

public static class WarpGateNormalize
{
    private static bool Matte(Color c)
    {
        int min = Math.Min(c.R, Math.Min(c.G, c.B));
        int max = Math.Max(c.R, Math.Max(c.G, c.B));
        return min >= 178 && max - min <= 22;
    }

    public static void Build(string input, string outputDirectory)
    {
        Directory.CreateDirectory(outputDirectory);
        using (var source = new Bitmap(input))
        using (var strip = new Bitmap(96 * 8, 96, PixelFormat.Format32bppArgb))
        using (var stripGraphics = Graphics.FromImage(strip))
        {
            stripGraphics.Clear(Color.Transparent);
            stripGraphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            stripGraphics.PixelOffsetMode = PixelOffsetMode.Half;

            for (int frame = 0; frame < 8; frame++)
            {
                int x0 = (int)Math.Round(frame * source.Width / 8.0);
                int x1 = (int)Math.Round((frame + 1) * source.Width / 8.0);
                int w = x1 - x0, h = source.Height;
                var outside = new bool[w, h];
                var queue = new int[w * h];
                int head = 0, tail = 0;

                Action<int, int> seed = (x, y) => {
                    if (x < 0 || y < 0 || x >= w || y >= h || outside[x, y]) return;
                    if (!Matte(source.GetPixel(x0 + x, y))) return;
                    outside[x, y] = true;
                    queue[tail++] = y * w + x;
                };
                for (int x = 0; x < w; x++) { seed(x, 0); seed(x, h - 1); }
                for (int y = 0; y < h; y++) { seed(0, y); seed(w - 1, y); }
                while (head < tail)
                {
                    int encoded = queue[head++], px = encoded % w, py = encoded / w;
                    seed(px - 1, py); seed(px + 1, py);
                    seed(px, py - 1); seed(px, py + 1);
                }

                using (var isolated = new Bitmap(w, h, PixelFormat.Format32bppArgb))
                {
                    int minX = w, minY = h, maxX = -1, maxY = -1;
                    for (int y = 0; y < h; y++)
                    for (int x = 0; x < w; x++)
                    {
                        if (outside[x, y]) { isolated.SetPixel(x, y, Color.Transparent); continue; }
                        Color c = source.GetPixel(x0 + x, y);
                        isolated.SetPixel(x, y, Color.FromArgb(255, c.R, c.G, c.B));
                        minX = Math.Min(minX, x); minY = Math.Min(minY, y);
                        maxX = Math.Max(maxX, x); maxY = Math.Max(maxY, y);
                    }
                    if (maxX < minX || maxY < minY) throw new InvalidDataException("Empty gate frame " + frame);

                    int contentW = maxX - minX + 1, contentH = maxY - minY + 1;
                    // The authored source is an upright 3/4 ring, not a floor portal.  Lock the
                    // projected footprint so image-generation drift cannot turn individual
                    // frames into tall ovals.  A slightly wider-than-tall silhouette reads as a
                    // circular ring under mild top-down perspective while preserving its thick
                    // near/lower rim and pass-through depth.
                    int drawW = 88;
                    int drawH = 84;
                    int dx = (96 - drawW) / 2, dy = (96 - drawH) / 2;

                    using (var normalized = new Bitmap(96, 96, PixelFormat.Format32bppArgb))
                    using (var g = Graphics.FromImage(normalized))
                    {
                        g.Clear(Color.Transparent);
                        g.InterpolationMode = InterpolationMode.NearestNeighbor;
                        g.PixelOffsetMode = PixelOffsetMode.Half;
                        g.DrawImage(isolated, new Rectangle(dx, dy, drawW, drawH),
                            new Rectangle(minX, minY, contentW, contentH), GraphicsUnit.Pixel);
                        string file = Path.Combine(outputDirectory, "nfx_s5gate96_" + frame + ".png");
                        normalized.Save(file, ImageFormat.Png);
                        stripGraphics.DrawImageUnscaled(normalized, frame * 96, 0);
                    }
                }
            }
            strip.Save(Path.Combine(outputDirectory, "nfx_s5gate96_strip.png"), ImageFormat.Png);
        }
    }
}
