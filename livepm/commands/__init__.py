
from livepm.commands.build import BuildCommand
from livepm.commands.help import HelpCommand
from livepm.commands.deploy import DeployCommand
from livepm.commands.license import LicenseCommand
from livepm.commands.makedoc import MakeDocCommand
from livepm.commands.new import NewCommand
from livepm.commands.syncversion import SyncVersionCommand
from livepm.commands.install import InstallCommand
from livepm.commands.search import SearchCommand
from livepm.commands.dependencies import DependenciesCommand
from livepm.commands.list import ListCommand
from livepm.commands.uninstall import UninstallCommand
from livepm.commands.update import UpdateCommand
from livepm.commands.show import ShowCommand
from livepm.commands.showremote import ShowRemoteCommand

commands_order = [
    BuildCommand,
    DeployCommand,
    LicenseCommand,
    MakeDocCommand,
    NewCommand,
    SyncVersionCommand,
    HelpCommand,
    InstallCommand,
    SearchCommand,
    DependenciesCommand,
    ListCommand,
    UninstallCommand,
    UpdateCommand,
    ShowCommand,
    ShowRemoteCommand
]  

stored_commands = {c.name: c for c in commands_order}
