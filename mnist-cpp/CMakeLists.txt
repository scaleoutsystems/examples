cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(mnist-cpp)

list(APPEND CMAKE_PREFIX_PATH "$ENV{TORCH_DIR}/libtorch")
find_package(Torch REQUIRED)

find_package(NumCpp 2.6.2 REQUIRED)

add_executable(main main.cpp)
target_link_libraries(main "${TORCH_LIBRARIES}")
target_link_libraries(main NumCpp::NumCpp)
set_property(TARGET main PROPERTY CXX_STANDARD 14)