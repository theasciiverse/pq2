cmake_minimum_required(VERSION 3.27)
project(pq2game)

# nlohmann_json 3.11.3, the version upstream fetched at build time, is
# kept in third_party/ (its single header, sha256 9bea4c80...103ea6, as
# published with the release), so a build needs no network.
add_library(nlohmann_json INTERFACE)
target_include_directories(nlohmann_json SYSTEM INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/nlohmann_json)
add_library(nlohmann_json::nlohmann_json ALIAS nlohmann_json)

find_package(ZLIB REQUIRED)

set(
        SOURCE_FILES
        game.cpp
        spells.hpp
        spells.cpp
        game.hpp
        types.hpp
        offensiveattributes.hpp
        offensiveattributes.cpp
        defensiveattributes.hpp
        defensiveattributes.cpp
        shields.cpp
        shields.hpp
        armors.cpp
        armors.hpp
        weapons.cpp
        weapons.hpp
        specials.cpp
        specials.hpp
        itemattributes.cpp
        itemattributes.hpp
        itemofs.cpp
        itemofs.hpp
        boringitems.cpp
        boringitems.hpp
        monsters.cpp
        monsters.hpp
        races.cpp
        races.hpp
        classes.cpp
        classes.hpp
        titles.cpp
        titles.hpp
        newgame.cpp
        newgame.hpp
        character.hpp
        monstermods.cpp
        monstermods.hpp
        jsonserialiser.cpp
        jsonserialiser.hpp
        character.cpp
)

add_library(pq2game STATIC ${SOURCE_FILES})

target_link_libraries(pq2game PRIVATE pq2utils nlohmann_json::nlohmann_json ZLIB::ZLIB)
target_include_directories(pq2game
        PRIVATE pq2utils nlohmann_json::nlohmann_json
        INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
)