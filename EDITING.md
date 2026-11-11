# How to change the words on your site

You never need to touch code or layout. All the words live in the `content/` folder.
Change them, save, and the live site updates by itself about a minute later.

There are two ways to edit. Use whichever feels easier.

## Option A — Pages CMS (a simple editing screen)

1. Go to **https://app.pagescms.org** and sign in with your GitHub account.
2. Open your website repository.
3. In the left menu, pick what you want to change:
   - **Question cards** — the cards on the board and their detail pages
   - **Notes**
   - **Homepage, About and Contact texts**
   - **Experience**, **Questions I am chasing next**, **Methods page**
4. Change the words and press **Save**.

To add a question or a note, open the list and press **Add an entry**.
To hide one without deleting it, tick **Hide this question** (or **Hide this note**).

## Option B — straight on GitHub

1. Open your repository on github.com and go into the `content/` folder.
2. Click the file you want, then the pencil icon (Edit).
3. Change the words, then press **Commit changes**.

Rules for the files:

- Change only the words **after** a colon, e.g. `status: In progress` → `status: Completed`.
- If a line has a colon or starts with `[` inside the words, keep the "quotes" around it.
- In question and note files, the part between the two `---` lines is the card details;
  everything below is the detail page, written in plain text with `## ` for headings and
  `- ` for bullet points.

## Common jobs

| I want to… | Where |
|---|---|
| Change a card's one-sentence answer | `content/questions/<question>.md` → `answer:` |
| Mark work as finished | same file → `status: Completed` |
| Change the line under my name | `content/site.yml` → `who_line:` |
| Add a note | new file in `content/notes/`, named like `2026-11-20-my-topic.md` |
| Add my resume | upload `resume.pdf` into `content/files/` |
| Add a chart to a question | upload the image into `content/files/`, then set `figure: image: files/your-chart.png` |
| Add a paper or slides | upload into `content/files/`, then add it under `files:` in the question |
| Change the order of cards | `order:` in each question file (1 = first) |

Field names to use: `finance`, `economics`, `metrics` (Econometrics and Statistics), `risk`.

## If something looks wrong

Open the **Actions** tab on GitHub. A red cross means the last save had a typo
(often a missing quote). Open it to see which file, fix that line, and save again.
