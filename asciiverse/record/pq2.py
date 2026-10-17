"""pq2 preview: a character is rolled up, then the game plays itself.

From the main menu the driver starts a new game and goes through the
character sheet the way a player would: a random name, a race
and a class picked from their lists, the stats rolled a few times (and
one roll taken back with Unroll), then Sold!. From there pq2 plays by
itself, as Progress Quest does: the prologue's visions, then the first
quest and the killing, looting and selling, with every bar filling. The
driver only opens the plot list once, when Act I begins, and quits
(Esc, which saves) after about 59 seconds, so the cast ends with the
terminal restored. The 80x24 screen is centred, so in 100x30 it starts
at row 3, column 10.

    python3 asciiverse/record/pq2.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rec
from rec import DOWN, ENTER, ESC, LEFT, RIGHT, F4

r = rec.Rec("pq2", "pq2")
r.wait_for("Start New Game", 8)
r.pump(1.2)
r.key(ENTER, 0.6)                    # Start New Game
r.wait_for("Sold!", 5)
r.pump(0.6)

r.key(RIGHT, 0.3)                    # to Random, and a new name
r.key(ENTER, 0.7)

r.key(DOWN, 0.3)                     # Race: open the list, walk down it
r.key(ENTER, 0.4)
for _ in range(3):
    r.key(DOWN, 0.25)
r.key(ENTER, 0.4)

r.key(DOWN, 0.3)                     # Class: the same
r.key(ENTER, 0.4)
for _ in range(3):
    r.key(DOWN, 0.25)
r.key(ENTER, 0.4)

r.key(DOWN, 0.3)                     # Roll a few times
for _ in range(3):
    r.key(ENTER, 0.5)
r.key(RIGHT, 0.3)                    # Unroll the last one
r.key(ENTER, 0.6)
r.key(LEFT, 0.2)
r.key(DOWN, 0.5)                     # Sold!
r.key(ENTER, 0.3)
r.wait_for("Plot Development", 5)

# the game plays itself; glance at the plot list once the prologue is
# done, then watch the first quest begin
plot_seen = False
while r.elapsed() < 59:
    if not plot_seen and "Act I" in r.text():
        r.pump(1.0)
        r.key(F4, 1.6)
        r.key(ESC, 0.2)
        plot_seen = True
    else:
        r.pump(0.25)
r.finish(ESC)
