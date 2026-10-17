cmake_minimum_required(VERSION 3.27)
project(pq2ncurses)

set(
        SOURCE_FILES
        pq2ncurses.cpp
        pq2ncurses.hpp
        mainmenu.cpp
        mainmenu.hpp
        ncursesview.cpp
        ncursesview.hpp
        charactercreator.cpp
        charactercreator.hpp
        gamescreen.cpp
        gamescreen.hpp
        loadscreen.cpp
        loadscreen.hpp
)

add_library(pq2ncurses STATIC ${SOURCE_FILES})

# the wide-character ncurses, which draws the progress bars' block
# characters: ncursesw where it is a library of its own (on Debian and
# Ubuntu plain -lncurses is the narrow one), else ncurses (macOS, whose
# ncurses is the wide one); NCURSES_LIBRARY can name the file instead
find_library(NCURSES_LIBRARY NAMES ncursesw ncurses REQUIRED)

target_link_libraries(pq2ncurses pq2gui pq2game pq2utils ${NCURSES_LIBRARY})
target_include_directories(pq2ncurses
        PRIVATE pq2gui pq2game pq2utils
        INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
)