# EDCOR 310: The Science of Learning

Source files for the EDCOR 310 open textbook by Benjamin Pacini.

## Building the website

The live site is the `site/` folder, served by Cloudflare at learning.benjaminpacini.com.
The home page, table of contents, and published chapter pages are generated from the chapter snapshot in `etb-live/`. The build also installs the shared device-voice audio player from `audio/player/`:

    python3 build/build_site.py

Run it after any change to chapter titles, subtitles, unit pages, chapter content, or book order, and commit the updated `site/` files.
