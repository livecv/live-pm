
from livepm.commands.build import BuildCommand
from livepm.commands.help import HelpCommand
from livepm.commands.deploy import DeployCommand
from livepm.commands.license import LicenseCommand
from livepm.commands.makedoc import MakeDocCommand
# from livepm.comamnds.new import NewCommand
from livepm.commands.syncversion import SyncVersionCommand

commands_order = [
    BuildCommand,
    DeployCommand,
    LicenseCommand,
    MakeDocCommand,
    # NewCommand,
    SyncVersionCommand,
    HelpCommand
]  

stored_commands = {c.name: c for c in commands_order}
