from subprocess import run
from os import path
import argparse

SAMPLEDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/data/nerf"
WORKDIR = "/home/mschmidt/instant-relightable-ngp/instant-ngp/scripts"
SNAPDIR = "/home/mschmidt/instant-relightable-ngp/data/snapshots"
DATADIR = "/home/mschmidt/instant-relightable-ngp/data/synthetic"
DOMEDIR = "/mnt/bigdisk/OBJECTS2011/Samurai/"

SNAPS = ["fox", "bike_singlecolmap" "bike_single","bike_colmap", "bike_python", "lego","samurai", "metal_balls"]

scene_bike_single = "../../data/synthetic/bike/transforms_python_151.json"

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

	parser.add_argument("--screenshot_transforms", default="", help="Path to a nerf style transforms.json from which to save screenshots.")
	parser.add_argument("--screenshot_frames", nargs="*", help="Which frame(s) to take screenshots of.")
	parser.add_argument("--screenshot_dir", default="", help="Which directory to output screenshots to.")
	parser.add_argument("--screenshot_spp", type=int, default=16, help="Number of samples per pixel in screenshots.")

	parser.add_argument("--video_camera_path", default="", help="The camera path to render, e.g., base_cam.json.")
	parser.add_argument("--video_camera_smoothing", action="store_true", help="Applies additional smoothing to the camera trajectory with the caveat that the endpoint of the camera path may not be reached.")
	parser.add_argument("--video_loop_animation", action="store_true", help="Connect the last and first keyframes in a continuous loop.")
	parser.add_argument("--video_fps", type=int, default=60, help="Number of frames per second.")
	parser.add_argument("--video_n_seconds", type=int, default=1, help="Number of seconds the rendered video should be long.")
	parser.add_argument("--video_spp", type=int, default=8, help="Number of samples per pixel. A larger number means less noise, but slower rendering.")
	parser.add_argument("--video_output", type=str, default="video.mp4", help="Filename of the output video.")

	parser.add_argument("--save_mesh", default="", help="Output a marching-cubes based mesh from the NeRF or SDF model. Supports OBJ and PLY format.")
	parser.add_argument("--marching_cubes_res", default=256, type=int, help="Sets the resolution for the marching cubes grid.")
	

	parser.add_argument("--width", "--screenshot_w", type=int, default=0, help="Resolution width of GUI and screenshots.")
	parser.add_argument("--height", "--screenshot_h", type=int, default=0, help="Resolution height of GUI and screenshots.")

	parser.add_argument("--gui", action="store_true", help="Run the testbed GUI interactively.")
	parser.add_argument("--train", action="store_true", help="If the GUI is enabled, controls whether training starts immediately.")
	parser.add_argument("--n_steps", type=int, default=-1, help="Number of steps to train for before quitting.")
	parser.add_argument("--second_window", action="store_true", help="Open a second window containing a copy of the main output.")

	parser.add_argument("--sharpen", default=0, help="Set amount of sharpening applied to NeRF training images. Range 0.0 to 1.0.")


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
	scene_lego = 				"../../data/synthetic/lego/transforms_scale_4.json"
	scene_sam = path.join(DOMEDIR,"./hdr/hdr_alpha_crop/transforms_out.json")
	scene_balls = 				"../../data/synthetic/metal_linearlight/transforms_python.json"
	
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

# Here debug functions
def makeScreenshotBike():
	scene = path.join(DATADIR,"bike/transforms_python_2000.json")
	snap = path.join(SNAPDIR,"bike_python.msgpack")
	screenshot_transforms = path.join(DATADIR,"bike/transforms_python_test.json")
	screenshot_dir = "/home/mschmidt/instant-relightable-ngp/data/synthetic/bike/screenshots/python0"
	makeScreenshots(scene,snap,screenshot_transforms,screenshot_dir)

def makeScreenshotBikeSingle():
	scene = scene_bike_single
	snap = path.join(SNAPDIR,"bike_single.msgpack")
	screenshot_transforms = scene_bike_single
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
	scene = scene_bike_single
	snap =  path.join(SNAPDIR,"bike_single.msgpack")
	test = scene_bike_single
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
	#makeScreenshotBikeSingle()
	#makeScreenshotSingleColmap()
	#makeScreenshotBikeColmap()
	#makeScreenshotBike()
	#calcLossesFox()
	calcLossesBikePython()
	#calcLossesBikePython1()
	#calcLossesBikeColmap()
	#calcLossesBikeColmap1()
	# Single Colmap still isn't working
