cmake_minimum_required(VERSION 3.5)
project(NorsMonitor VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

add_executable(NorsMonitor
    nors_monitor.cpp
)

target_link_libraries(NorsMonitor PRIVATE Qt5::Widgets)
