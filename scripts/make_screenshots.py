from subprocess import run
from os import path

WORKDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/scripts"
SNAPDIR = "/home/mschmidt/instant-relightable-ngp/data/snapshots"
DATADIR = "/home/mschmidt/instant-relightable-ngp/data/synthetic"
DOMEDIR = "/mnt/bigdisk/OBJECTS2011/Samurai/"

SNAPS = ["bike_singlecolmap" "bike_single","bike_colmap", "bike_python", "lego","samurai", "metal_balls"]

def checkSnapshot(snap):
	snap_file = f"{snap}.msgpack"
	path_snap_full = path.join(SNAPDIR,snap_file)
	return path.exists(path_snap_full)

def checkSnapshots():
	for s in SNAPS:
		print(s, checkSnapshot(s))

def saveSnapshot(transform_path, snap_path):
	run(["python3", "run.py","--mode", "nerf", "--scene", transform_path, "--save_snapshot", snap_path ],cwd=WORKDIR)

def saveSnapshots(force=False):
	scene_bike_single = "../../data/synthetic/bike/transforms_python_151.json"
	scene_bike_colmap = "../../data/synthetic/bike/transforms_colmap_2000.json"
	scene_bike_singlecolmap = "../../data/synthetic/bike/transforms_colmap_151.json"
	scene_bike_python = "../../data/synthetic/bike/transforms_python_2000.json"
	scene_lego = "../../data/synthetic/lego/transforms_scale_4.json"
	scene_sam = path.join(DOMEDIR,"./hdr/hdr_alpha_crop/transforms_out.json")
	scene_balls = "../../data/synthetic/metal_linearlight/transforms_python.json"
	
	snap_bike_singlecolmap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	snap_bike_single = path.join(SNAPDIR,"bike_single.msgpack")
	snap_bike_colmap = path.join(SNAPDIR,"bike_colmap.msgpack")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	snap_lego = path.join(SNAPDIR,"lego.msgpack")
	snap_sam =path.join(SNAPDIR,"samurai.msgpack")
	snap_balls = path.join(SNAPDIR,"metal_balls.msgpack")
	
	if force or not checkSnapshot("bike_singlecolmap"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_singlecolmap, "--save_snapshot", snap_bike_singlecolmap, "--n_steps", "100000"],cwd=WORKDIR)
	if force or not checkSnapshot("bike_single"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_single, "--save_snapshot", snap_bike_single, "--n_steps", "100000"],cwd=WORKDIR)
	if force or not checkSnapshot("bike_colmap"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_colmap, "--save_snapshot", snap_bike_colmap, "--n_steps", "100000" ],cwd=WORKDIR)
	if force or not checkSnapshot("bike_python"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--save_snapshot", snap_bike_python, "--n_steps", "100000"],cwd=WORKDIR)
	if force or not checkSnapshot("lego"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_lego, "--save_snapshot", snap_lego, "--n_steps", "100000"  ],cwd=WORKDIR)
	if force or not checkSnapshot("samurai"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_sam, "--save_snapshot", snap_sam, "--n_steps", "100000"  ],cwd=WORKDIR)
	if force or not checkSnapshot("metal_balls"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_balls, "--save_snapshot", snap_balls, "--n_steps", "100000"   ],cwd=WORKDIR)

def makeScreenshotBikeColmap():
	scene_bike_python = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	snap_bike_python = path.join(SNAPDIR,"bike_colmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_151.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/colmap"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)

# done
def makeScreenshotBike():
	scene_bike_python = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	screenshot_transforms = scene_bike_python
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/python"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)

def makeScreenshotSingle():
	scene_bike_python = path.join(DATADIR,"bike/transforms_python_151.json")
	snap_bike_python = path.join(SNAPDIR,"bike_single.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_151.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_py"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)

def makeScreenshotSingleColmap():
	scene_bike_python = path.join(DATADIR,"bike/transforms_colmap_151.json")
	snap_bike_python = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_colmap_151.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_col"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--load_snapshot", snap_bike_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)


def makeScreenshotLego():
	scene_lego_python = path.join(DATADIR,"lego/transforms_scale_4.json")
	snap_lego_python = path.join(SNAPDIR,"lego.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_python_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/test"
	run(["python3", "run.py","--mode", "nerf", "--scene", scene_lego_python, "--load_snapshot", snap_lego_python, "--screenshot_transforms", screenshot_transforms, "--screenshot_dir", screenshot_dir ],cwd=WORKDIR)
	
#makeScreenshotLego()

def calcLosses(scene,snap,test):
	run(["python3", "run.py","--mode", "nerf", 
	"--scene", scene, 
	"--load_snapshot", snap, 
	"--test_transforms", test, 
	],cwd=WORKDIR)

def calcLossesLegoAll():
	scene = path.join(DATADIR,"lego/transforms_scale_4.json")
	snap = path.join(SNAPDIR,"lego.msgpack")
	test = path.join(DATADIR,"lego/transforms_python_test.json")
	calcLosses(scene,snap,test)

def calcLossesBikePython():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	test = path.join(DATADIR,"bike/transforms_python_2000.json")
	calcLosses(scene,snap,test)

	

if __name__ == "__main__":
	checkSnapshots()
	saveSnapshots()
	makeScreenshotSingle()
	makeScreenshotSingleColmap()
	makeScreenshotBikeColmap()