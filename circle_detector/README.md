This is Nick's hacky method.

Although intended for IR, it has only been tested using visible light (and that's how all the params are currently set). This comprises:
1) a webcam
2) a desk lamp behind the webcam as if the webcam itself were shooting light
3) a chopstick
4) a retroreflective corner cube (https://en.wikipedia.org/wiki/Corner_reflector) about 1 cm large with the interior faces covered in a layer of tinfoil; this is affixed to the tip of the chopstick with epoxy (although hot glue is probably better) so that the tip of the "wand" is retroreflective (with visible light) just like the original wand is with IR

Given a stream of color image frames, we try to detect a circle being completed with the wand tip, at which point we play a "spell sound" (this should be improved and the spell should have a more significant, thematic effect, such as lighting up an LED or a room smart light or something). We only recognize one spell right now, the circle shape.

Algorithm overview:
1) threshold each frame to try and get only the tip of the wand white and the rest black
2) accumulate these frames over time into one single accumulated frame
3) find candidate circles on the accumulated frame (using hough circle transform)
4) score each circle by the number of inliers
5) pick the best circle
6) if the arc length of the inliers on this circle is enough, cast the spell!

Files:
1) full_test.py is the full monty, live.
2) camera_test.py tests your webcam HW. Probably want to do this first.
3) sound_test.py similarly tests your sound HW.
3) lumos_detector.py is the top-level class that uses the other util classes.
4) util classes each should have a _test.py, which use test data rather than HW.
