"""IDAPython plugin to demangle strings.

It demangles the string under the cursor and set the result as comment. This
relies on the DbgHelp DLL on your system, so it should work for most recent VC
versions. This can be run as a standalone tool as well (Python 2).
"""

import argparse
import ctypes
import ctypes.util
import platform

try:
    import idaapi
    import idc
    IS_IDAPYTHON = True
except ImportError:
    IS_IDAPYTHON = False

MAX_DEMANGLED_LEN = 2**12

def main():
    if IS_IDAPYTHON:
        setup_ida()
    else:
        run_standalone()

def setup_ida():
    bindings = {
        "Shift-G": demangle_str_at_screen_ea
    }
    for binding in bindings:
        idaapi.add_hotkey(binding, bindings[binding])
    print "Bound " + ", ".join(bindings.keys())

def run_standalone():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("name", type = str, help = "mangled name")
    args = argparser.parse_args()

    demangled = demangle_vc(args.name)
    if demangled:
        print demangled.decode("utf8", errors = "replace")

def demangle_str_at_screen_ea():
    ea = idc.ScreenEA()
    string = idc.GetString(ea)
    if not string:
        print "Couldn't get any string at {}.".format(hex(ea))
        return

    demangled = demangle_vc(string)
    if not demangled:
        print "Demangling failed."
        return

    idc.MakeComm(ea, demangled)

def demangle_vc(name, flags = 0x2800):
    """ Call DbgHelp.UnDecorateSymbolName and return the demangled name bytes.
    Default flags are UNDNAME_32_BIT_DECODE | UNDNAME_NO_ARGUMENTS because it
    seems to work only this way?! """
    if platform.system() != "Windows":
        print "DbgHelp is only available on Windows!"
        return ""

    dbghelp_path = ctypes.util.find_library("dbghelp")
    dbghelp = ctypes.windll.LoadLibrary(dbghelp_path)

    name = name.lstrip(".")
    mangled = ctypes.c_char_p(name.encode("utf8"))
    demangled = ctypes.create_string_buffer("\x00" * MAX_DEMANGLED_LEN)
    demangled_len = ctypes.c_int(MAX_DEMANGLED_LEN)
    flags = ctypes.c_int(flags)
    ret = dbghelp.UnDecorateSymbolName(mangled, demangled, demangled_len, flags)
    if ret == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        print "UnDecorateSymbolName failed ({})".format(error_code)
        return ""
    else:
        return demangled.value

if __name__ == "__main__":
    main()
