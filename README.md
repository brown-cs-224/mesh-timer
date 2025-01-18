# Python Timer Script

This repository contains a script (and a mesh file) to help measure and visualize the time complexity of your implementation of the mesh subdivision routine. A good implementation should show a a linear/log-linear trend.

To run the script, first compile your mesh code (in release mode!). The build output should contain a `./mesh` executable.
Then, run the script with the following command:

```bash
python timer.py -c <path_to_your_mesh_executable> 
```

If you are using Qt on windows, you might run into a runtime error claiming that you are missing some .dll files. To remedy this, locate the `windeploy.exe` file in `/Qt`(look for something like `/Qt/6.5.2/mingw_64/bin/windeployqt.exe`). Run the following command:

```bash
./windeployqt.exe --release <path_to_your_mesh_executable>
```

After this, use the python script as directed. This should run the script, which will call your mesh executable with a range of input sizes and measure the time it takes to subdivide the mesh. The results will be saved as a lineplot image `time_complexity.png` in the same directory.

![Time Complexity](demo.png)