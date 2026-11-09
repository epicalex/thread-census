# Just one more thread

A static, unofficial celebration of Lenny’s follow-up questions. No framework, install step, analytics, external fonts, or runtime data requests.

## Publish on GitHub Pages

Copy `index.html`, `style.css`, `script.js`, `favicon.svg`, and `.nojekyll` to the publishing folder of your GitHub Pages repository. All asset paths are relative, so project URLs work. The prepared `thread-census-github-pages.zip` contains precisely these files.

The finished HTML includes all data; opening `index.html` locally also works. JavaScript adds search, the pull/follow filter, and the resize Easter egg. Width changes trigger the wool animation after a brief pause; height-only changes do not. Reduced-motion preferences disable the animation.

## Update the data

From the original project workspace, rerun the archived analysis and then regenerate this page:

```sh
python3 outputs/count_threads.py --repo work/full-archive --review outputs/full-archive/thread-review.json --out outputs/full-archive --source mcp
python3 outputs/full-archive/analyse_themes.py
python3 thread-census/build.py
```

`build.py` uses the reviewed results in `data/thread-results.json`. Edit `template.html` for page copy and layout, then regenerate. If refreshing the underlying archive, review new candidates first, and update the snapshot date and coverage notes in the template to match the new run.

Leaderboard: count descending, episodes with at least two moments. Timestamp log: episode date descending, timestamps ascending within each episode. YouTube preference and the Deb Liu date correction come from the existing analyzer and link map.

Only derived counts and paraphrased topic descriptions are included. Do not publish the original workspace or raw transcript archive. Original podcast content belongs to Lenny Rachitsky; this is a personal, non-commercial fan project and is not endorsed by him.

The chance figure is the share of archive transcripts with at least one qualifying pull/follow moment. The counter counts only literal pulls; follows do not reset it. Topic classifications live in `outputs/full-archive/thread-themes-review.json`. New or changed moments require an editorial topic review before building. The full interpretation and limitations are in `outputs/full-archive/thread-theme-analysis.md`.

## Build this repository

Run `python3 build.py` from the repository root. The data folder contains derived metadata, counts and paraphrased summaries; it contains no raw transcripts. The archive recount commands above refer to the original analysis workspace.

## Creator

[Alex Cragg on LinkedIn](https://www.linkedin.com/in/alexcragg) · [GitHub repository](https://github.com/epicalex/thread-census)
