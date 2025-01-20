# Python Timer Script

This repository contains a script (and a mesh file) to help measure and visualize the time complexity of your implementation of a geometry processing function. A good implementation should show a a linear/log-linear trend.

To run the script, first compile your mesh code (in release mode!). The build output should contain a `./mesh` executable.
Then, run the script with the following command:

```bash
python timer.py -c <path_to_your_mesh_executable> -o <path_to_output_image> -i <path_to_input_mesh> -d <directory_for_intermediate meshes> -n <number_of_recursive_iterations> -cmd <method> -p <method_parameter>
```

If you are using Qt on windows, you might run into a runtime error claiming that you are missing some .dll files. To remedy this, locate the `windeploy.exe` file in `/Qt`(look for something like `/Qt/6.5.2/mingw_64/bin/windeployqt.exe`). Run the following command:

```bash
./windeployqt.exe --release <path_to_your_mesh_executable>
```

After this, use the python script as directed. This should run the script, which will call your mesh executable with a range of input sizes and measure the time it takes to perform this geometry processing function on the mesh. The results will be saved as a lineplot image `time_complexity.png` in the same directory. The image below shows the script's output for the subdivision routine.

![Time Complexity](demo.png)
