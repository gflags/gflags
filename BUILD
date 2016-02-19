# Bazel build file for gflags
#
# See INSTALL.md for instructions for adding gflags to a Bazel workspace.

licenses(["notice"])

cc_library(
    name = "gflags",
    srcs = [
        "src/gflags.cc",
        "src/gflags_completions.cc",
        "src/gflags_reporting.cc",
        "src/mutex.h",
        "src/util.h",
        ":config_h",
        ":gflags_completions_h",
        ":gflags_declare_h",
        ":gflags_h",
        ":includes",
    ],
    hdrs = ["gflags.h"],
    copts = [
        "-Wno-sign-compare",
        "-DHAVE_STDINT_H",
        "-DHAVE_SYS_TYPES_H",
        "-DHAVE_INTTYPES_H",
        "-DHAVE_SYS_STAT_H",
        "-DHAVE_UNISTD_H",
        "-DHAVE_FNMATCH_H",
        "-DHAVE_STRTOLL",
        "-DHAVE_STRTOQ",
        "-DHAVE_PTHREAD",
        "-DHAVE_RWLOCK",
        "-DGFLAGS_INTTYPES_FORMAT_C99",
    ],
    includes = [
        "include",
    ],
    visibility = ["//visibility:public"],
)

genrule(
    name = "config_h",
    srcs = [
        "src/config.h.in",
    ],
    outs = [
        "config.h",
    ],
    cmd = "sed -r -e 's,^#cmakedefine,// cmakedefine,' $(<) > $(@)",
)

genrule(
    name = "gflags_h",
    srcs = [
        "src/gflags.h.in",
    ],
    outs = [
        "gflags.h",
    ],
    cmd = "sed -r -e 's/@[A-Z_]+@//' $(<) > $(@)",
)

genrule(
    name = "gflags_completions_h",
    srcs = [
        "src/gflags_completions.h.in",
    ],
    outs = [
        "gflags_completions.h",
    ],
    cmd = "sed -r -e 's/@GFLAGS_NAMESPACE@/gflags/' $(<) > $(@)",
)

genrule(
    name = "gflags_declare_h",
    srcs = [
        "src/gflags_declare.h.in",
    ],
    outs = [
        "gflags_declare.h",
    ],
    cmd = ("sed -r -e '" +
           "s/@GFLAGS_NAMESPACE@/gflags/;" +
           "s/@(HAVE_STDINT_H|HAVE_SYS_TYPES_H|HAVE_INTTYPES_H" +
           "|GFLAGS_INTTYPES_FORMAT_C99)@/1/;" +
           "s/@([A-Z0-9_]+)@/0/" +
           "' $(<) > $(@)"),
)

genrule(
    name = "includes",
    srcs = [
        ":gflags_h",
        ":gflags_declare_h",
    ],
    outs = [
        "include/gflags/gflags.h",
        "include/gflags/gflags_declare.h",
    ],
    cmd = "mkdir -p $(@D)/include/gflags && cp $(SRCS) $(@D)/include/gflags",
)
