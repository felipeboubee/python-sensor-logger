"""Plot an acquisition run, marking the samples the reader had to substitute."""

import matplotlib.pyplot as plt

# Two themes so the same figure can sit on a light or a dark page without being
# re-edited by hand. The failure colour is a reserved status red rather than a
# second series colour, and is additionally distinguished by marker shape and a
# legend entry, so it never depends on colour alone to be readable. Both sets
# clear a 3:1 contrast floor against their own surface and separate under
# simulated colour blindness (worst-case ΔE 21.6 light, 25.7 dark).
THEMES = {
    "light": {
        "surface": "#fcfcfb",
        "ink": "#0b0b0b",
        "ink_muted": "#52514e",
        "reading": "#2a78d6",
        "failure": "#d03b3b",
    },
    "dark": {
        "surface": "#1a1a19",
        "ink": "#ffffff",
        "ink_muted": "#c3c2b7",
        "reading": "#3987e5",
        "failure": "#d03b3b",
    },
}


def _style_axes(ax, c):
    """Apply the recessive grid/frame treatment shared by both panels."""
    ax.set_facecolor(c["surface"])
    ax.grid(True, color=c["ink_muted"], alpha=0.15, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(c["ink_muted"])
        ax.spines[side].set_alpha(0.4)
    ax.tick_params(colors=c["ink_muted"], labelsize=9)


def plot_run(rows, path, default, theme="light"):
    """Save a two-panel distance-vs-time plot of `rows` to `path`.

    Samples equal to `default` are the reader's sentinel rather than
    measurements. The top panel shows the record as written, sentinels included,
    which is what demonstrates no sample was dropped. The bottom panel drops to
    the measured range, where the sentinels would otherwise compress every real
    reading into an unreadable band at the bottom of the axis.

    theme -- key into THEMES; "dark" for embedding on a dark page.
    """

    if not rows:
        raise ValueError("no rows to plot")
    if theme not in THEMES:
        raise ValueError(f"unknown theme {theme!r}; expected one of {sorted(THEMES)}")

    c = THEMES[theme]

    t = [r[0] for r in rows]
    d = [r[1] for r in rows]

    # Exact float equality is safe here: the sentinel is written verbatim by the
    # reader and round-tripped through the CSV, never arrived at by arithmetic.
    bad_t = [ti for ti, di in rows if di == default]
    good = [di for di in d if di != default]

    # One figure per call, so plotting two runs in the same process does not
    # draw them both onto the same axes.
    fig, (ax_full, ax_zoom) = plt.subplots(
        2, 1, figsize=(9, 6.4), sharex=True,
        gridspec_kw={"height_ratios": [1, 1.5]},
        facecolor=c["surface"])

    fig.suptitle(
        f"Sensor log — {len(rows)} samples over {t[-1]:.2f} s, "
        f"{len(bad_t)} read failures recorded",
        color=c["ink"], fontsize=12.5, x=0.02, ha="left", y=0.98)

    # --- Top: the record exactly as logged -------------------------------
    ax_full.plot(t, d, linewidth=1.2, color=c["reading"], label="logged value")
    if bad_t:
        ax_full.scatter(bad_t, [default] * len(bad_t),
                        marker="x", s=44, linewidths=1.7, color=c["failure"], zorder=3,
                        label=f"read failure → {default:g} m sentinel ({len(bad_t)})")
    ax_full.set_ylabel("distance (m)", color=c["ink_muted"])
    # Legend above the axes rather than inside them: anywhere inside collides
    # with the sentinel spikes, which by definition reach the top of this panel.
    ax_full.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2,
                   fontsize=9, frameon=False, labelcolor=c["ink"])
    _style_axes(ax_full, c)

    # --- Bottom: measurements only ---------------------------------------
    # Substituted samples become gaps rather than spikes, so the line breaks
    # where the sensor failed instead of dragging the y-scale to 99 m.
    measured = [di if di != default else float("nan") for di in d]
    ax_zoom.plot(t, measured, linewidth=1.4, color=c["reading"])
    for ti in bad_t:
        ax_zoom.axvline(ti, color=c["failure"], linewidth=1.0, alpha=0.45, zorder=1)

    if good:
        span = max(good) - min(good)
        pad = span * 0.12 if span else 1.0
        ax_zoom.set_ylim(min(good) - pad, max(good) + pad)

    ax_zoom.set_xlabel("time (s)", color=c["ink_muted"])
    ax_zoom.set_ylabel("distance (m)", color=c["ink_muted"])
    ax_zoom.set_title("measured range only — red rules mark the substituted samples",
                      color=c["ink_muted"], fontsize=9.5, loc="left", pad=6)
    _style_axes(ax_zoom, c)

    # Explicit margins rather than tight_layout, which cannot account for the
    # legend anchored outside the top axes.
    fig.subplots_adjust(top=0.855, bottom=0.085, left=0.085, right=0.98, hspace=0.30)
    fig.savefig(path, dpi=150, facecolor=c["surface"])
    plt.close(fig)
