# This utility helps launch a launcher.options file.
# To use:
# 1. Create a file called "launcher.options" right next to this file.
# 2. On the first line of the file, add the name of the map to launch.
#    The map should be found in the "maps" directory. Example: "CollectMineralShards"
# 3. On the second line of the file, add the name of the agent to run.
#    The agent should be located in the "agents" directory. Example: "Teran.teran_base_agent"
# 4. Run launcher.py. Also Python should be in the path.

import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def find_starcraft_minigame_dir():
    if os.path.isdir("D:\Program Files (x86)\StarCraft II\Maps\mini_games\\"):
        return "D:\Program Files (x86)\StarCraft II\Maps\mini_games\\"
    elif os.path.isdir("C:\Program Files (x86)\StarCraft II\Maps\mini_games\\"):
        return "C:\Program Files (x86)\StarCraft II\Maps\mini_games\\"
    elif os.path.isdir("C:\Program Files\StarCraft II\Maps\mini_games\\"):
        return "C:\Program Files\StarCraft II\Maps\mini_games\\"
    elif os.path.isdir("D:\Program Files\StarCraft II\Maps\mini_games\\"):
        return "D:\Program Files\StarCraft II\Maps\mini_games\\"
    else:
        raise EnvironmentError("Cannot find StarCraft mini game directory.")


def main():
    if os.name != 'nt' or is_admin():
        mapFileFull = mapFile = agentFile = ""
        mamaPath = os.path.dirname(os.path.realpath(__file__))

        if not mamaPath.endswith("\\"):
            mamaPath = mamaPath + "\\"

        starcraft_dir = find_starcraft_minigame_dir()

        if not os.path.exists("launcher.options"):
            raise EnvironmentError("Cannot find launcher.options. See header of launcher.py on how to use.");

        with open("launcher.options") as f:
            mapFile = f.readline().replace("\n", "")
            agentFile = f.readline().replace("\n", "")

        if not mapFile.endswith(".SC2Map"):
            mapFileFull = mapFile + ".SC2Map"

        os.system('cp \"' + mamaPath + "maps\\" + mapFileFull + "\" \"" + starcraft_dir + mapFileFull + "\"")

        sys.path.append(mamaPath + "agents\\" + agentFile.split(".")[0])
        import pysc2.bin.agent as agent
        import importlib
        module_name, classname = ("agents." + agentFile).rsplit(".", 1)
        mod = getattr(importlib.import_module(module_name), classname)
        agent.run_thread(mod, mapFile, False)

        while (True):
            is_admin()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)



if  __name__ =='__main__':main()