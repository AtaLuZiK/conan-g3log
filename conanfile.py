import os
import shutil
from os import path

from conans import CMake, ConanFile, tools


class G3logConan(ConanFile):
    name = "g3log"
    version = "1.3.2.65"
    license = "The Unlicense"
    url = "https://github.com/AtaLuZiK/conan-g3log"
    description = """G3log is an asynchronous, "crash safe", logger that is easy to use with default logging sinks or you can add your own."""
    settings = "os", "compiler", "build_type", "arch"
    options = {
      "shared": [True, False],
      "use_dynamic_logging_levels": [True, False],
      "change_debug_to_dbug": [True, False],
      "use_dynamic_max_message_size": [True, False],
      "log_full_filename": [True, False],
      "enable_fatal_signal_handling": [True, False],
      "enable_vectored_exception_handling": [True, False],
      "debug_break_at_fatal_signal": [True, False],
    }
    default_options = '\n'.join([
      "shared=False",
      "use_dynamic_logging_levels=False",
      "change_debug_to_dbug=False",
      "use_dynamic_max_message_size=True",
      "log_full_filename=False",
      "enable_fatal_signal_handling=True",
      "enable_vectored_exception_handling=True",
      "debug_break_at_fatal_signal=False",
    ])
    exports_sources = "g3log-config.cmake", "patches/*"
    requires = (
        "boost/1.67.0@conan/stable",
        "zlib/1.2.11@conan/stable",
    )
    generators = "cmake"
    
    def config_options(self):
        if self.settings.compiler != "Visual Studio":
            del self.options.enable_vectored_exception_handling
            del self.options.debug_break_at_fatal_signal

    def source(self):
        self.download_g3log_source()
        self.download_g3sinks_source()

    def download_g3log_source(self):
        self.run("git clone https://github.com/KjellKod/g3log.git")
        self.run("cd g3log && git checkout de870694d5ae29b9e2f18ac4f8cfb9ff19599983")
        tools.patch("g3log", "patches/g3log/CMakeLists.txt.patch")

    def download_g3sinks_source(self):
        self.run("git clone https://github.com/KjellKod/g3sinks.git")
        self.run("cd g3sinks && git checkout 5240acc1404f0cc9402a5edc88af29b9887dcd45")
        tools.patch("g3sinks", "patches/g3sinks/CMakeLists.txt.patch")
        tools.patch("g3sinks", "patches/g3sinks/Options.cmake.patch")
        shutil.move("g3sinks", "g3log")

    def build(self):
        cmake = CMake(self)
        self.bind_cmake_bool_option(cmake, "shared", "G3_SHARED_LIB")
        self.bind_cmake_bool_option(cmake, "use_dynamic_logging_levels", "USE_DYNAMIC_LOGGING_LEVELS")
        self.bind_cmake_bool_option(cmake, "change_debug_to_dbug", "CHANGE_G3LOG_DEBUG_TO_DBUG")
        self.bind_cmake_bool_option(cmake, "use_dynamic_max_message_size", "USE_G3_DYNAMIC_MAX_MESSAGE_SIZE")
        self.bind_cmake_bool_option(cmake, "log_full_filename", "G3_LOG_FULL_FILENAME")
        self.bind_cmake_bool_option(cmake, "enable_fatal_signal_handling", "ENABLE_FATAL_SIGNALHANDLING")
        if self.settings.compiler == "Visual Studio":
            self.bind_cmake_bool_option(cmake, "enable_vectored_exception_handling", "ENABLE_VECTORED_EXCEPTIONHANDLING")
            self.bind_cmake_bool_option(cmake, "debug_break_at_fatal_signal", "DEBUG_BREAK_AT_FATAL_SIGNAL")
        cmake.definitions["BUILD_ROOT_DIR"] = os.getcwd()
        cmake.configure(source_folder="g3log")
        cmake.build()

    def build_g3sinks(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_ROOT_DIR"] = os.getcwd()
        cmake.configure(source_folder="g3sinks/logrotate", build_folder="g3sinks")
        cmake.build(build_folder="g3sinks")

    def package(self):
        if self.settings.os == "Windows":
            self.copy("g3logger.lib", dst="lib", src="lib")
            self.copy("g3logger.dll", dst="bin", src="bin")
            self.copy("g3logrotate.lib", dst="lib", src="lib")
        elif self.settings.os == "Linux":
            if self.options.shared:
                self.copy("libg3logger.so*", dst="lib", src="lib", symlinks=True)
            else:
                self.copy("libg3logger.a", dst="lib", src="lib")
            self.copy("libg3logrotate.a", dst="lib", src="lib")
        self.copy("g3log/*.hpp", dst="include", src="include")  # generated_definitions.hpp
        self.copy("g3log/*.hpp", dst="include", src=path.join(self.name, 'src'))
        self.copy("g3sinks/*.h", dst="include", src="g3log/g3sinks/logrotate/src")
        self.copy("g3log-config.cmake", dst=".")

    def package_info(self):
        self.cpp_info.libs = ["g3logger", "g3logrotate"]
    
    def bind_cmake_bool_option(self, cmake, name, cmake_name):
        cmake.definitions[cmake_name] = "ON" if getattr(self.options, name) else "OFF"
        return "ON" if getattr(self.options, name) else "OFF"
