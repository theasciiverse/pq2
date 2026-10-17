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
# characters; on Debian and Ubuntu plain -lncurses is the narrow one
set(CURSES_NEED_NCURSES TRUE)
set(CURSES_NEED_WIDE TRUE)
find_package(Curses REQUIRED)

target_link_libraries(pq2ncurses pq2gui pq2game pq2utils ${CURSES_LIBRARIES})
target_include_directories(pq2ncurses
        PRIVATE pq2gui pq2game pq2utils ${CURSES_INCLUDE_DIRS}
        INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
)