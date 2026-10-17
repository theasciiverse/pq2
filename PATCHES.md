# Changes from upstream

This is the Asciiverse packaging of pq2, Nick Bollom's remake of
Progress Quest, from github.com/nbollom/pq2 (the `upstream` remote,
GPL-3.0, see `LICENSE`). The `asciiverse` branch starts from upstream's
`master` at `62416be` (2025-01-12, "some include changes for lib
headers"; upstream has no tags and reports version 2025.0). None of its
three forks has anything newer. Everything after that commit is ours.

Progress Quest itself is Eric Fredricksen's (2002), released under the
MIT licence (http://progressquest.com/license.txt, "Copyright (c)
2002-2004 Eric Fredricksen"); pq2's races, classes, monsters, spells and
items come from it. pq2 is not the original and is presented in the
catalog as a remake.

Only the ncurses edition is built. The Qt and GTK editions, their
sources and upstream's `resources/pq.png` stay in the tree untouched and
are not shipped.

## Build

- **No download at build time.** `game/CMakeLists.txt` fetched
  nlohmann_json v3.11.3 from GitHub with FetchContent. Its single header,
  `json.hpp` from the v3.11.3 release (sha256
  `9bea4c8066ef4a1c206b2be5a36302f8926f7fdc6087af5d20b417d0cf103ea6`,
  the checksum published in the release notes; the same file as
  `single_include/nlohmann/json.hpp` at the tag), is kept in
  `third_party/nlohmann_json/` with its `LICENSE.MIT` (sha256
  `86b998c7...45cf14`), behind an interface target of the same name.
  Ubuntu's `nlohmann-json3-dev` would also do, but is not installed by
  default, and Alpine and macOS would each need their own package.
- **Static internal libraries.** The game, utils, gui and ncurses
  libraries were `SHARED`; they are `STATIC`, so the program is one
  binary.
- **Wide ncurses, found by name.** The ncurses edition linked
  `-lncurses`, the narrow library on Debian and Ubuntu, while its
  progress bars are Unicode block characters. `ncurses/CMakeLists.txt`
  now finds `ncursesw`, else `ncurses` (macOS, whose one ncurses is the
  wide one); `NCURSES_LIBRARY` can name the file.
- **libc++.** `ncurses/loadscreen.cpp` includes `<algorithm>` for
  `std::sort`, which libstdc++ supplied through other headers but LLVM's
  libc++ (macOS) does not.
- `asciiverse/build.sh` configures with Qt and GTK off and copies the
  program to `out/pq2`; `STATIC=1` links `libncursesw.a`, `libz.a` and the
  C++ library statically (Alpine). `asciiverse/package.sh` packs
  `dist/pq2-<target>.tar.gz` from `asciiverse/archive/pq2.txt`.
  `.github/workflows/release.yml` builds static musl Linux (x86_64,
  aarch64) and macOS (x86_64, arm64) on a tag. No Windows build:
  upstream turns the ncurses edition off on Windows. Upstream's own
  workflows run only on pushes to `master`, so they stay as they are.

## Files

- **Saved games in the player's data folder.** A new character was saved
  as `<name>.pq2` in whatever folder the game was started from, and Load
  Game opened on that folder. Both now use `pq2/` under
  `$XDG_DATA_HOME`, else `~/.local/share/pq2`, made on first use
  (`utils/datadir.cpp`); the current folder is the fallback when it
  cannot be made. Load Game can still browse elsewhere.
- A save named on the command line is used as given; a bare name that is
  not in the current folder is looked for in the data folder, with or
  without `.pq2` (`main.cpp`), so `pq2 Ada` carries on Ada's game.
- Load Game lists a folder it cannot read as empty instead of ending the
  game with an uncaught `filesystem_error`.

## Screen

- **Centred.** Every view drew its 80x24 window at the terminal's top
  left corner. It is placed in the middle, also after a resize, and what
  the old window left behind is cleared (`NCursesView::Resize`).
- **Popups follow the view.** The lists (race, class, equipment, spells,
  inventory, plot, quests) and the load error were `subwin()` windows,
  positioned from the terminal's corner; they are `derwin()` windows
  relative to the view. A resize deleted the view's window while a popup
  was still its subwindow, which curses refuses; the popup is dropped
  first and drawn again on the next frame.
- **No flicker.** Each frame began with `wclear()`, which makes curses
  repaint the whole terminal on every refresh, ten times a second.
  `werase()` clears the window without forcing that, so only changes are
  sent: a minute on the game screen, measured in a pty, went from 982 KB
  of output to 23 KB.
- **Nothing printed over the screen.** `Game::Close()` printed "Closing"
  to standard output while curses owned the terminal (it landed in the
  bottom border) and the ncurses front end printed "cleaning up" after
  restoring it. Both debugging messages are gone.

## Bugs

- **New characters started with garbage counters.** `Character`'s
  numbers had no initial values and NewGame's character is never zeroed,
  so `CurrentPlotProgress`, `CurrentQuestProgress` and `CurrentMonster`
  began with whatever was in memory. Under AddressSanitizer, which fills
  new memory with `0xbe`, the Prologue's bar stood at 100% from the
  start, and UBSan reported an invalid `CurrentActionType` when the
  character was copied. Every scalar field now starts at zero
  (`game/character.hpp`).
- **Loading a damaged save.** `Game::LoadGame()` returned without
  `gzclose()` when a save did not parse, leaking zlib's buffers on each
  failed attempt (LeakSanitizer), and treated `gzread()`'s -1 for a
  damaged file as data, passing a negative length to
  `stringstream::write()`. The file is closed as soon as it is read and
  a read error counts as an invalid save.

## Checked

- Built with GCC 15 and Clang 21 (glibc), GCC 14 static against musl in
  Alpine 3.22, and Clang 20 with libc++ in Alpine (standing in for
  macOS), all with upstream's `-Wall -Wextra -Wpedantic -Werror`.
- An ASan and UBSan build played through the menu, the character sheet
  (names, both lists, rolls, unroll), all five popups, the refresh keys,
  resizes, quitting, Load Game and loading damaged saves, with no
  reports after the fixes above. A throwaway harness ran the game core
  under ASan and UBSan for three characters to level 21 (about 83 hours
  of game time each), saving and reloading every few game hours and
  comparing the character's hash after each reload: no reports, no
  differences.

## Catalog files

- `asciiverse/pq2/NOTICE`, `asciiverse/pq2/LICENSE.progressquest`
  (Progress Quest's MIT licence as published at
  http://progressquest.com/license.txt, sha256
  `cf01e19a835f40f72bc413eb0c668ff84e4d80c27eb65b6df8e28c30717b4f37`) and
  nlohmann/json's licence go in the archive beside upstream's `LICENSE`.
- `asciiverse/record/pq2.py` plays the preview through `rec.py`, from
  the NetBSD games' recorder; `asciiverse/casts/pq2.cast` is its
  recording.
