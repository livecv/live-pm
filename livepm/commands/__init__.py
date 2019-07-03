
from livepm.commands.build import BuildCommand
from livepm.commands.help import HelpCommand
from livepm.commands.deploy import DeployCommand
from livepm.commands.license import LicenseCommand
from livepm.commands.makedoc import MakeDocCommand
from livepm.commands.new import NewCommand
from livepm.commands.syncversion import SyncVersionCommand
from livepm.commands.install import InstallCommand

commands_order = [
    BuildCommand,
    DeployCommand,
    LicenseCommand,
    MakeDocCommand,
    NewCommand,
    SyncVersionCommand,
    HelpCommand,
    InstallCommand
]  

stored_commands = {c.name: c for c in commands_order}
