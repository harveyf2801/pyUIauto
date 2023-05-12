import argparse
import re
from importlib_metadata import version
from enum import IntEnum

class ExitCode(IntEnum):
    VERSION_NUMBER_INVALID = 1
    VERSION_BELOW_CURRENT = 2
    VERSION_IS_CURRENT = 3

parser = argparse.ArgumentParser(description='version arguments.')
parser.add_argument("--version",
                    action="store",
                    help="Version to use"
                    )
parser.add_argument("--version-maj",
                    action="store",
                    help="Major version to use"
                    )
parser.add_argument("--version-min",
                    action="store",
                    help="Minor version to use"
                    )
parser.add_argument("--version-build",
                    action="store",
                    help="Build version to use"
                    )
args = parser.parse_args()

pattern = "^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"

new_version = ""
current_version = version("pyuiauto")

if args.version:
    new_version = args.version
elif (args.version_maj and args.version_min and args.version_build):
    new_version = f"{args.version_maj}.{args.version_min}.{args.version_build}"

if new_version == current_version:
    exit(ExitCode.VERSION_IS_CURRENT)
elif new_version < current_version:
    exit(ExitCode.VERSION_BELOW_CURRENT)
elif not re.fullmatch(pattern, new_version):
    exit(ExitCode.VERSION_NUMBER_INVALID)
else:
    exit(0)

