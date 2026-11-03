#!/bin/sh
# Builds the ncurses edition of pq2 into out/pq2 with upstream's CMake
# files; the Qt and GTK editions are left out. Compiler and flags come
# from the environment, so one script serves every target
# (see .github/workflows/release.yml):
#
#   asciiverse/build.sh                       # Debian, Ubuntu
#   STATIC=1 asciiverse/build.sh              # Alpine, static musl binary
#   CMAKE_OSX_ARCHITECTURES=arm64 MACOSX_DEPLOYMENT_TARGET=13.3 asciiverse/build.sh  # macOS
#   BUILD_TYPE=Debug CXXFLAGS=-fsanitize=address LDFLAGS=-fsanitize=address asciiverse/build.sh
#
# Needs CMake 3.27 or newer, a C++23 compiler, ncurses (wide) and zlib.
# nlohmann_json comes from third_party/, so nothing is downloaded.
set -eu
cd "$(dirname "$0")/.."
build="out/build"
set -- -DQT_ENABLED=OFF -DGTK_ENABLED=OFF -DNCURSES_ENABLED=ON \
  -DCMAKE_BUILD_TYPE="${BUILD_TYPE:-Release}"
if [ -n "${STATIC:-}" ]; then
  # link libncursesw.a and libz.a, as the compiler finds them, instead of
  # the shared libraries CMake would pick, and the whole program statically
  lib() { "${CXX:-c++}" -print-file-name="$1"; }
  set -- "$@" -DNCURSES_LIBRARY="$(lib libncursesw.a)" \
    -DZLIB_LIBRARY="$(lib libz.a)" -DCMAKE_EXE_LINKER_FLAGS="-static -s"
fi
rm -rf "$build" && mkdir -p out
cmake -S . -B "$build" "$@" >/dev/null
cmake --build "$build" --parallel "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)"
cp "$build/bin/pq2ncurses" out/pq2
echo "built pq2"
