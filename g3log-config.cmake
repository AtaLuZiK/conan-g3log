find_path(G3LOG_INCLUDE_DIR NAMES g3log/g3log.hpp PATHS ${CONAN_INCLUDE_DIRS_G3LOG})
find_library(G3LOG_LIBRARY NAMES g3logger PATHS ${CONAN_LIB_DIRS_G3LOG})
find_library(G3LOGROTATE_LIBRARY NAMES g3logrotate ${CONAN_LIB_DIRS_G3LOG})

find_library(Boost REQUIRED)
find_package(ZLIB REQUIRED)

add_library(G3log INTERFACE IMPORTED)
target_include_directories(G3log
  INTERFACE ${G3LOG_INCLUDE_DIR}
  INTERFACE ${Boost_INCLUDE_DIRS}
  INTERFACE ${ZLIB_INCLUDE_DIR}
)
target_link_libraries(G3log
  INTERFACE ${G3LOG_LIBRARY}
  INTERFACE ${G3LOGROTATE_LIBRARY}
  INTERFACE ${Boost_LIBRARIES}
  INTERFACE ${ZLIB_LIBRARY}
)

mark_as_advanced(G3LOG_INCLUDE_DIR G3LOG_LIBRARY_DIR G3LOG_LIBRARY)

message("** G3log found by Conan!")
set(G3LOG_FOUND TRUE)
message("   - includes: ${G3LOG_INCLUDE_DIR}")
message("   - libraries: ${G3LOG_LIBRARY}")
