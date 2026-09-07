# hsjang0.github.io/hsjang

Personal academic homepage of **Hyosoon Jang (장효순)** — Ph.D. student, Graduate School of AI, KAIST.

Live at **<https://hsjang0.github.io/hsjang/>**.

## Updating the site

Almost every change is a one-file edit under `_data/`. Nothing else needs to change.

| To change | Edit |
| --- | --- |
| Papers (title, authors, venue, links, thumbnail) | `_data/publications.yaml` |
| News items on the front page | `_data/news.yaml` |
| Invited talks | `_data/talks.yaml` |
| Honors and awards | `_data/awards.yaml` |
| Name, affiliation, email, social links, CV | `_data/main_info.yaml` |
| The About paragraphs | `index.html` |

### Adding a paper

Add an entry at the top of `papers:` in `_data/publications.yaml`:

```yaml
  - tag: "C5"                       # key used by the [C5] references in the bio
    title: "Paper Title"
    authors: "<b>Hyosoon Jang</b>, Co Author"   # bold your own name
    venue: "Conference on Something (ABC)"      # full name, shown under the authors
    venue_short: "ABC"                          # short name, shown in the badge
    year: "2026"
    highlight: "Oral, 1.2%"         # optional; makes the badge stand out
    selected: y                     # "y" to show it on the home page
    image: "/assets/publications/thumb.png"     # optional thumbnail
    links:
      - label: "Paper"
        url: "/assets/publications/paper.pdf"   # site-relative paths are fine
      - label: "Code"
        url: "https://github.com/hsjang0/repo"  # or absolute URLs
```

Each paper gets an anchor from its `tag`, so `#C5` links straight to it —
that is how the `[C5]` chips in the About section work.

Put PDFs and thumbnails in `assets/publications/`. Thumbnails are cropped to
16:10, so a wide figure works best.

## Deployment

Pushing to `main` triggers [`.github/workflows/jekyll-gh-pages.yml`](.github/workflows/jekyll-gh-pages.yml),
which builds the site with `actions/jekyll-build-pages` and publishes it to GitHub Pages.

> **Do not set `baseurl` in `_config.yml`.** The build action injects `/hsjang`
> at build time; hardcoding it there overrides that value and breaks every
> asset path. Keep using `| relative_url` for internal links.

## Local preview

The site needs Jekyll (Ruby ≥ 2.7):

```bash
bundle exec jekyll serve   # or: jekyll serve
```

## Structure

```
index.html            single page: hero, about, news, publications, talks, awards
_layouts/default.html <head>, top bar, footer, SEO + Open Graph meta
_data/                all content (see the table above)
libs/custom/site.css  the whole stylesheet — design tokens at the top
libs/custom/site.js   theme toggle, sticky top bar, scroll spy
assets/               profile photos, paper PDFs and thumbnails
robots.txt, image-sitemap.xml, google*.html   SEO / Search Console
```

No CSS framework and no JavaScript dependencies. Light and dark themes are
driven by the tokens in the `:root` blocks of `site.css`; the theme follows the
system setting and can be overridden with the toggle in the top bar.
