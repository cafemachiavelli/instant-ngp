from subprocess import run
from os import path
import argparse


STEPS = "100000"
SAMPLEDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/data/nerf"
WORKDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/scripts"
SNAPDIR = "/home/mschmidt/instant-relightable-ngp/data/snapshots"
DATADIR = "/home/mschmidt/instant-relightable-ngp/data/synthetic"
DOMEDIR = "/mnt/bigdisk/OBJECTS2011/Samurai/"

SNAPS = ["lego_big","fox", "bike_singlecolmap", "bike_single","bike_colmap", "bike_python", "lego","lego_single","samurai", "metal_balls"]

scene_bike_single = "../../data/synthetic/bike/transforms_python_cl066.json"

def parse_args():
	parser = argparse.ArgumentParser(description="Run Relit-NGP, save configurations, render screenshots or calculate errors")

	parser.add_argument("--scene", "--training_data", default="", help="The scene to load. Can be the scene's name or a full path to the training data.")
	parser.add_argument("--mode", default="", const="nerf", nargs="?", choices=["nerf", "sdf", "image", "volume"], help="Mode can be 'nerf', 'sdf', 'image' or 'volume'. Inferred from the scene if unspecified.")
	parser.add_argument("--network", default="", help="Path to the network config. Uses the scene's default if unspecified.")

	parser.add_argument("--load_snapshot", default="", help="Load this snapshot before training. recommended extension: .msgpack")
	parser.add_argument("--save_snapshot", default="", help="Save this snapshot after training. recommended extension: .msgpack")

	parser.add_argument("--nerf_compatibility", action="store_true", help="Matches parameters with original NeRF. Can cause slowness and worse results on some scenes.")
	parser.add_argument("--test_transforms", default="", help="Path to a nerf style transforms json from which we will compute PSNR.")
	parser.add_argument("--near_distance", default=-1, type=float, help="Set the distance from the camera at which training rays start for nerf. <0 means use ngp default")
	parser.add_argument("--exposure", default=0.0, type=float, help="Controls the brightness of the image. Positive numbers increase brightness, negative numbers decrease it.")
	parser.add_argument("--diff_dir", default="", help="Path to folder where source, reconstruction and difference images will be saved.")

	return parser.parse_args()



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
	scene_bike_colmap = 		"../../data/synthetic/bike/transforms_colmap_2000.json"
	scene_bike_singlecolmap = 	"../../data/synthetic/bike/transforms_colmap_151.json"
	scene_bike_python = 		"../../data/synthetic/bike/transforms_python_2000.json"
	scene_lego = 				"../../data/synthetic/lego/transforms_train.json"
	scene_lego_single = 		"../../data/synthetic/lego/transforms_cl046.json"
	scene_sam = path.join(DOMEDIR,"./hdr/hdr_alpha_crop/transforms_out.json")
	scene_balls = 				"../../data/synthetic/metal_linearlight/transforms_out.json"
	scene_balls_single = 				"../../data/synthetic/metal_linearlight/transforms_out_cl067.json"

	big =  "/home/mschmidt/instant-relightable-ngp/instant-ngp/configs/nerf/big_deep.json"
	deep =  "/home/mschmidt/instant-relightable-ngp/instant-ngp/configs/nerf/deep.json"	

	snap_fox = path.join(SNAPDIR,"fox.msgpack")
	snap_bike_singlecolmap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	snap_bike_single = path.join(SNAPDIR,"bike_single.msgpack")
	snap_bike_colmap = path.join(SNAPDIR,"bike_colmap.msgpack")
	snap_bike_python = path.join(SNAPDIR,"bike_python.msgpack")
	snap_lego = path.join(SNAPDIR,"lego0.msgpack")
	snap_lego_deep = path.join(SNAPDIR,"lego_deep.msgpack")
	snap_sam =path.join(SNAPDIR,"samurai.msgpack")
	snap_balls = path.join(SNAPDIR,"metal_balls.msgpack")
	snap_balls_single = path.join(SNAPDIR,"metal_balls_single.msgpack")
	snap_lego_big = path.join(SNAPDIR,"lego_big.msgpack")
	snap_lego_single = path.join(SNAPDIR, "lego_single0.msgpack")
	
	if force or not checkSnapshot("fox"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_fox, "--save_snapshot", snap_fox, "--n_steps", STEPS],cwd=WORKDIR)
	if force or not checkSnapshot("bike_singlecolmap"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_singlecolmap, "--save_snapshot", snap_bike_singlecolmap, "--n_steps", STEPS],cwd=WORKDIR)
	if force or not checkSnapshot("bike_single"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_single, "--save_snapshot", snap_bike_single, "--n_steps", STEPS],cwd=WORKDIR)
	if force or not checkSnapshot("bike_colmap"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_colmap, "--save_snapshot", snap_bike_colmap, "--n_steps", STEPS ],cwd=WORKDIR)
	if force or not checkSnapshot("bike_python"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_bike_python, "--save_snapshot", snap_bike_python, "--n_steps", STEPS],cwd=WORKDIR)
	if force or not checkSnapshot("lego"):
		run(["python3", "run.py","--mode", "nerf","--near_distance", "0.9","--scene", scene_lego, "--save_snapshot", snap_lego, "--n_steps", STEPS  ],cwd=WORKDIR)
	if force or not checkSnapshot("samurai"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_sam, "--save_snapshot", snap_sam, "--n_steps", STEPS  ],cwd=WORKDIR)
	if force or not checkSnapshot("metal_balls"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_balls, "--save_snapshot", snap_balls, "--n_steps", STEPS   ],cwd=WORKDIR)
	if force or not checkSnapshot("metal_balls_single"):
		run(["python3", "run.py","--mode", "nerf", "--scene", scene_balls_single, "--save_snapshot", snap_balls_single, "--n_steps", STEPS   ],cwd=WORKDIR)
	if force or not checkSnapshot("lego_big"):
		run(["python3", "run.py","--mode", "nerf", "--near_distance", "0.9","--scene", scene_lego, "--save_snapshot", snap_lego_big, "--n_steps", STEPS,"--network", big   ],cwd=WORKDIR)
	if force or not checkSnapshot("lego_single"):
		run(["python3", "run.py","--mode", "nerf","--near_distance", "0.9", "--scene", scene_lego_single, "--save_snapshot", snap_lego_single, "--n_steps", STEPS  ],cwd=WORKDIR)
	if force or not checkSnapshot("lego_deep"):
		run(["python3", "run.py","--mode", "nerf", "--near_distance", "0.9","--scene", scene_lego, "--save_snapshot", snap_lego_deep, "--n_steps", STEPS,"--network", deep   ],cwd=WORKDIR)

def makeScreenshots(scene,snap,tf,dir):

	print(f"Rendering screenshots from {scene}, {snap}, {tf}.")
	run(["python3", "run.py","--mode", "nerf", "--near_distance", "0.9","--scene", scene, "--load_snapshot", snap, "--screenshot_transforms", tf, "--screenshot_dir", dir ],cwd=WORKDIR)

def makeScreenshotFox():
	scene = path.join(SAMPLEDIR,"fox/transforms.json")
	snap = path.join(SNAPDIR,"fox.msgpack")
	screenshot_transforms = "../data/nerf/fox/transforms.json"
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/fox/screenshots"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

# Bike Screenshots
def makeScreenshotBikeColmap():
	scene = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	snap = path.join(SNAPDIR,"bike_colmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/colmap"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotBike():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_cl066.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/python"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotBikeSingle():
	scene = scene_bike_single
	snap = path.join(SNAPDIR,"bike_single.msgpack")
	screenshot_transforms = scene_bike_single
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_py"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotSingleColmap():
	scene = path.join(DATADIR,"bike/transforms_colmap_cl066.json")
	snap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_colmap_cl066.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/single_col"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

# Lego
def makeScreenshotLego():
	scene = path.join(DATADIR,"lego/transforms_train.json")
	snap = path.join(SNAPDIR,"lego.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/test"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotLegoBig():
	scene = path.join(DATADIR,"lego/transforms_train.json")
	snap = path.join(SNAPDIR,"lego_big.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/big"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotLegoSingle():
	scene = path.join(DATADIR,"lego/transforms_in.json")
	snap = path.join(SNAPDIR,"lego_single.msgpack")
	screenshot_transforms = path.join(DATADIR,"lego/transforms_in.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/lego/screenshots/single"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def calcLosses(scene,snap,test):
	print(f"Calculating losses from {scene}, {snap}, {test}.")
	run(["python3", "run.py","--mode", "nerf", 	"--scene", scene, "--near_distance", "0.99",	"--load_snapshot", snap, 	"--test_transforms", test],cwd=WORKDIR)

def calcLossesFox():
	scene= path.join(SAMPLEDIR,"fox/transforms.json")
	snap = path.join(SNAPDIR,"fox.msgpack")
	test = path.join(SAMPLEDIR,"fox/transforms.json")
	calcLosses(scene,snap,test)

def calcLossesLego():
	scene = path.join(DATADIR,"lego/transforms_train.json")
	snap = path.join(SNAPDIR,"lego.msgpack")
	test = path.join(DATADIR,"lego/transforms_cl046.json")
	calcLosses(scene,snap,test)

def calcLossesLegoBig():
	scene = path.join(DATADIR,"lego/transforms_train.json")
	snap = path.join(SNAPDIR,"lego_big.msgpack")
	test = path.join(DATADIR,"lego/transforms_test.json")
	calcLosses(scene,snap,test)

def calcLossesLegoDeep():
	scene = path.join(DATADIR,"lego/transforms_train.json")
	snap = path.join(SNAPDIR,"lego_deep.msgpack")
	test = path.join(DATADIR,"lego/transforms_test.json")
	calcLosses(scene,snap,test)

def calcLossesLegoSingle():
	scene = path.join(DATADIR,"lego/transforms_cl046.json")
	snap = path.join(SNAPDIR,"lego_single.msgpack")
	test = path.join(DATADIR,"lego/transforms_cl046.json")
	calcLosses(scene,snap,test)

# Bike sets
def calcLossesBikePython():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	test = path.join(DATADIR,"bike/transforms_python_cl066.json")
	calcLosses(scene,snap,test)

def calcLossesBikePython1():
	# Losses of Bike w/o light_dir
	scene = scene_bike_single
	snap =  path.join(SNAPDIR,"bike_single.msgpack")
	test = scene_bike_single
	calcLosses(scene,snap,test)

def calcLossesBikeColmap():
	# Losses of bike with lightdir trained with Colmap
	scene = path.join(DATADIR,"bike/transforms_colmap_2000.json")
	snap = path.join(SNAPDIR,"bike_colmap.msgpack")
	test = path.join(DATADIR,"bike/transforms_colmap_cl066.json")
	calcLosses(scene,snap,test)

def calcLossesBikeColmap1():
	scene = path.join(DATADIR,"bike/transforms_colmap_cl066.json")
	snap = path.join(SNAPDIR,"bike_singlecolmap.msgpack")
	test = path.join(DATADIR,"bike/transforms_colmap_cl066.json")
	calcLosses(scene,snap,test)

# Sphere begins here

def calcLossesSphere1():
	scene = path.join(DATADIR,"metal_linearlight/transforms_out_cl067.json")
	snap = path.join(SNAPDIR,"metal_balls_single.msgpack")
	test = path.join(DATADIR,"metal_linearlight/transforms_out_cl067.json")
	calcLosses(scene,snap,test)

def calcLossesSphere():
	scene = path.join(DATADIR,"metal_linearlight/transforms_out.json")
	snap = path.join(SNAPDIR,"metal_balls.msgpack")
	test = path.join(DATADIR,"metal_linearlight/transforms_out_cl067.json")
	calcLosses(scene,snap,test)


if __name__ == "__main__":
	checkSnapshots()
	saveSnapshots()
	#makeScreenshotLego()
	#makeScreenshotLegoBig()
	#makeScreenshotBikeSingle()
	#makeScreenshotSingleColmap()
	#makeScreenshotBikeColmap()
	#makeScreenshotBike()
	#calcLossesFox()
	#calcLossesLego()
	calcLossesLegoDeep()
	#calcLossesLegoSingle()
	#calcLossesLegoBig()
	#calcLossesBikePython()
	#calcLossesBikePython1()
	#calcLossesBikeColmap()
	#calcLossesBikeColmap1()
	#calcLossesSphere()
	#calcLossesSphere1()