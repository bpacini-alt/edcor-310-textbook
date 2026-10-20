# EDCOR 310: The Science of Learning

Source files for the EDCOR 310 open textbook by Benjamin Pacini.

## Building the website

The live site is the `site/` folder, served by Cloudflare at learning.benjaminpacini.com.
The home page and table of contents are generated from the chapter snapshot in `etb-live/`:

    python3 build/build_site.py

Run it after any change to chapter titles, subtitles, unit pages, or book order, and commit the updated `site/` files.
