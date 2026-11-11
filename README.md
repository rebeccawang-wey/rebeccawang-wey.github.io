# Rebecca Wang — The Question Board

A personal website organised by questions, not job titles.

- **Words and content:** `content/` — see [EDITING.md](EDITING.md)
- **Design rules:** [DESIGN.md](DESIGN.md)
- **Templates:** `templates/` · **Styles:** `assets/css/site.css`
- **Build:** `build.py` turns `content/` into a finished site in `_site/`

## Put it online (one time, about 10 minutes)

1. Create a free account on github.com.
2. Create a new repository. For the address `yourname.github.io`, name the repository
   exactly `yourname.github.io`. Any other name gives `yourname.github.io/name/`
   (then set `base_path: "/name/"` in `content/site.yml`).
3. Upload every file and folder from this project (drag them into the repository page,
   including the hidden `.github` folder and `.pages.yml` — on a Mac, press
   Cmd + Shift + . in Finder to see hidden files). Commit.
4. In the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
5. Open the **Actions** tab and wait for the green tick. Your site is live.

To use your own domain later, add it under Settings → Pages → Custom domain.

## Build on your own computer (optional)

```
pip install -r requirements.txt
python build.py            # output in _site/
python -m http.server --directory _site 8000   # open http://localhost:8000
```

The build lists anything that needs checking, such as a related question that
does not exist or a file that is missing.
