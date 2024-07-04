import sys
import pathlib
root_path = pathlib.Path(__file__).parent.parent
sys.path.append(root_path)
from chaosmesh_app.chaosmesh_api import ChaosMeshAPI

chaos_mesh = ChaosMeshAPI()