cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(mnist-cpp)

list(APPEND CMAKE_PREFIX_PATH "$ENV{TORCH_DIR}/libtorch")
find_package(Torch REQUIRED)

set(HEADER_FILES "${CMAKE_CURRENT_SOURCE_DIR}/net.h")

foreach(_target
  train validate)
    add_executable(${_target} "${_target}.cpp" "${HEADER_FILES}")
    target_link_libraries(${_target} "${TORCH_LIBRARIES}")
    set_property(TARGET ${_target} PROPERTY CXX_STANDARD 14)
endforeach()