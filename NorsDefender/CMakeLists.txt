cmake_minimum_required(VERSION 3.10)
project(NorsDefender)

set(CMAKE_CXX_STANDARD 17)

add_executable(nors_defender nors_defender.cpp)
target_link_libraries(nors_defender pthread)
