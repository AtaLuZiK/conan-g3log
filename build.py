import copy
import platform

from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="g3log:shared")
    
    extend_settings = []
    for settings in builder.items:
        settings = copy.deepcopy(settings)
        settings.options["g3log:use_dynamic_logging_levels"] = True
        extend_settings.append(settings)
    builder.items.extend(extend_settings)
    
    extend_settings = []
    for settings in builder.items:
        settings = copy.deepcopy(settings)
        settings.options["g3log:change_debug_to_dbug"] = True
        extend_settings.append(settings)
    builder.items.extend(extend_settings)
    
    if platform.system() == "Windows":
        extend_settings = []
        for settings in builder.items:
            settings = copy.deepcopy(settings)
            settings.options["g3log:debug_break_at_fatal_signal"] = True
            extend_settings.append(settings)
        builder.items.extend(extend_settings)
    
    builder.run()
