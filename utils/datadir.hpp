//
// Asciiverse: where saved games live.
//

#pragma once

#include <filesystem>

// The player's own folder for pq2's files: pq2/ under $XDG_DATA_HOME,
// else ~/.local/share/pq2, made if it does not exist yet. Falls back to
// the current folder when neither variable is set or it cannot be made.
std::filesystem::path DataDir();
