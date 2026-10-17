//
// Asciiverse: where saved games live.
//

#include "datadir.hpp"
#include <cstdlib>
#include <system_error>

std::filesystem::path DataDir() {
    std::filesystem::path base;
    if (const char *xdg = std::getenv("XDG_DATA_HOME"); xdg && *xdg == '/') {
        base = xdg;
    }
    else if (const char *home = std::getenv("HOME"); home && *home) {
        base = std::filesystem::path(home) / ".local" / "share";
    }
    else {
        return std::filesystem::current_path();
    }
    const auto dir = base / "pq2";
    std::error_code error;
    std::filesystem::create_directories(dir, error);
    if (!std::filesystem::is_directory(dir, error)) {
        return std::filesystem::current_path();
    }
    return dir;
}
