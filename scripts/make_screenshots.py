from subprocess import run
from os import path

WORKDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/scripts"
SNAPDIR = "/home/mschmidt/instant-relightable-ngp/data/snapshots"
DATADIR = "/home/mschmidt/instant-relightable-ngp/data/synthetic"
DOMEDIR = "/mnt/bigdisk/OBJECTS2011/Samurai/"

SNAPS = ["bike_colmap", "bike_python", "lego","samurai", "metal_balls"]

def checkSnapshot(snap):
	snap_file = f"{snap}.msgpack"
	path_snap_full = path.join(SNAPDIR,snap_file)
	return path.exists(path_snap_full)

def checkSnapshots():
	for s in SNAPS:
		print(s, checkSnapshot(s))

def saveSnapshot(transform_path, snap_path):
	run(["python3", "run.py","--mode", "nerf", "--scene", transform_path, "--save_snapshot", snap_path ],cwd=WORKDIR)

def saveSnapshots():

	scene_bike_colmap = "../../data/synthetic/bike/transforms_colmap_2000.json"
	scene_bike_python = "../../data/synthetic/bike/transforms_python_2000.json"
	scene_lego = "../../data/synthetic/lego/transforms_scale_4.json"
	scene_sam = ""
	
	snap_bike_colmap = path.join(SNAPDIR,"bike_colmap.msgpack")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	snap_lego = path.join(SNAPDIR,"lego.msgpack")
	snap_sam =""
	
	if not checkSnapshot("bike_colmap"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_colmap, "--save_snapshot", snap_bike_colmap ],cwd=WORKDIR)
	if not checkSnapshot("bike_python"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--save_snapshot", snap_bike_python ],cwd=WORKDIR)
	if not checkSnapshot("lego"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_lego, "--save_snapshot", snap_lego  ],cwd=WORKDIR)
	if not checkSnapshot("samurai"):
		pass
		#run(["python3", "run.py","--mode", "nerf", "--scene", scene_sam, "--save_snapshot", sam_sam  ],cwd=WORKDIR)
	
checkSnapshots()
saveSnapshots()

def makeScreenshotBike():
	scene_bike_python = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	screenshot_transforms = scene_bike_python
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/python"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)

def makeScreenshotLego():
	scene_bike_python = path.join(DATADIR,"lego/transforms_scale_4.json")
	snap_bike_python = path.join(SNAPDIR,"lego.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_scale_3.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/python"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)
	
makeScreenshotLego()
