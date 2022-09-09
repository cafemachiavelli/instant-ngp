from subprocess import run
from os import path

SAMPLEDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/data/nerf"
WORKDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/scripts"
SNAPDIR = "/home/mschmidt/instant-relightable-ngp/data/snapshots"
DATADIR = "/home/mschmidt/instant-relightable-ngp/data/synthetic"
DOMEDIR = "/mnt/bigdisk/OBJECTS2011/Samurai/"

SNAPS = ["fox", "bike_singlecolmap" "bike_single","bike_colmap", "bike_python", "lego","samurai", "metal_balls"]

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
	scene_fox = path.join(SAMPLEDIR,"fox/transforms.json")
	scene_bike_single = "../../data/synthetic/bike/transforms_python_151.json"
	scene_bike_colmap = "../../data/synthetic/bike/transforms_colmap_2000.json"
	scene_bike_singlecolmap = "../../data/synthetic/bike/transforms_colmap_151.json"
	scene_bike_python = "../../data/synthetic/bike/transforms_python_2000.json"
	scene_lego = "../../data/synthetic/lego/transforms_scale_4.json"
	scene_sam = path.join(DOMEDIR,"./hdr/hdr_alpha_crop/transforms_out.json")
	scene_balls = "../../data/synthetic/metal_linearlight/transforms_python.json"
	
	snap_fox = path.join(SNAPDIR,"fox.msgpack")
	snap_bike_singlecolmap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	snap_bike_single = path.join(SNAPDIR,"bike_single.msgpack")
	snap_bike_colmap = path.join(SNAPDIR,"bike_colmap.msgpack")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	snap_lego = path.join(SNAPDIR,"lego.msgpack")
	snap_sam =path.join(SNAPDIR,"samurai.msgpack")
	snap_balls = path.join(SNAPDIR,"metal_balls.msgpack")
	
	if force or not checkSnapshot("fox"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_fox, "--save_snapshot", snap_fox, "--n_steps", "10000"],cwd=WORKDIR)
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

def makeScreenshots(scene,snap,tf,dir):
	print(f"Rendering screenshots from {scene}, {snap}, {tf}.")
	run(["python3", "run.py","--mode", "nerf", "--scene", scene, "--load_snapshot", snap, "--screenshot_transforms", tf, "--screenshot_dir", dir ],cwd=WORKDIR)

def makeScreenshotFox():
	scene = path.join(SAMPLEDIR,"fox/transforms.json")
	snap = path.join(SNAPDIR,"fox.msgpack")
	screenshot_transforms = "../data/nerf/fox/transforms.json"
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/fox/screenshots"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotBikeColmap():
	scene = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	snap = path.join(SNAPDIR,"bike_colmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/colmap"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotBike():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/python"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotSingle():
	scene = path.join(DATADIR,"bike/transforms_python_151.json")
	snap = path.join(SNAPDIR,"bike_single.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_151.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_py"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotSingleColmap():
	scene = path.join(DATADIR,"bike/transforms_colmap_151.json")
	snap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_colmap_151.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_col"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotLego():
	scene = path.join(DATADIR,"lego/transforms_scale_4.json")
	snap = path.join(SNAPDIR,"lego.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_python_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/test"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def calcLosses(scene,snap,test):
	print(f"Calculating losses from {scene}, {snap}, {test}.")
	run(["python3", "run.py","--mode", "nerf", 	"--scene", scene, 	"--load_snapshot", snap, 	"--test_transforms", test],cwd=WORKDIR)

def calcLossesFox():
	scene= path.join(SAMPLEDIR,"fox/transforms.json")
	snap = path.join(SNAPDIR,"fox.msgpack")
	test = path.join(SAMPLEDIR,"fox/transforms.json")
	calcLosses(scene,snap,test)

def calcLossesLegoAll():
	scene = path.join(DATADIR,"lego/transforms_scale_4.json")
	snap = path.join(SNAPDIR,"lego.msgpack")
	test = path.join(DATADIR,"lego/transforms_python_test.json")
	calcLosses(scene,snap,test)

# Bike sets
def calcLossesBikePython():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	test = path.join(DATADIR,"bike/transforms_python_test.json")
	calcLosses(scene,snap,test)

def calcLossesBikePython1():
	# Losses of Bike w/o light_dir
	scene = path.join(DATADIR,"bike/transforms_python_151.json")
	snap =  path.join(SNAPDIR,"bike_single.msgpack")
	test = path.join(DATADIR,"bike/transforms_python_151.json")
	calcLosses(scene,snap,test)

def calcLossesBikeColmap():
	# Losses of bike with lightdir trained with Colmap
	scene = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	snap = path.join(SNAPDIR,"bike_colmap.msgpack")
	test = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	calcLosses(scene,snap,test)

def calcLossesBikeColmap1():
	scene = path.join(DATADIR,"bike/transforms_colmap_151.json")
	snap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	test = path.join(DATADIR,"bike/transforms_colmap_151.json")
	calcLosses(scene,snap,test)
	

if __name__ == "__main__":
	#checkSnapshots()
	saveSnapshots()
	#makeScreenshotFox()
	#makeScreenshotSingle()
	#makeScreenshotSingleColmap()
	#makeScreenshotBikeColmap()
	#makeScreenshotBike()
	#calcLossesFox()
	#calcLossesBikePython()
	#calcLossesBikePython1()
	#calcLossesBikeColmap()
	calcLossesBikeColmap1()
	# Single Colmap still isn't working
