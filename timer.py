import os
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import configparser

import sys

def get_vertex_count(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
        vertex_count = 0
        for line in lines:
            if line.startswith("v "):
                vertex_count += 1
    return vertex_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the time complexity trend.')
    if sys.platform == "win32":
        parser.add_argument('-c', '--compiled_file', type=str,
                            help='Path to the compiled file', default=".\\mesh_build\\mesh")
    else:
        parser.add_argument('-c', '--compiled_file', type=str,
                            help='Path to the compiled file', default="./mesh_build/mesh")
    parser.add_argument('-o', '--output_file', type=str,
                        help='Path to the output image file', default="time_complexity.png")
    parser.add_argument('-i', '--input_file', type=str,
                        help='The initial meshes', default="./inp_meshes/tet_0.obj")
    parser.add_argument('-d', '--temp_dir', type=str,
                        help='Directory for saving intermediate meshes', default="./inp_meshes")
    parser.add_argument('-n', '--num_iters', type=int,
                        help="Number of recursive applications.", default=9)
    parser.add_argument('-cmd', '--command', type=str,
                        help='The method to run', default="subdivide")
    parser.add_argument('-p', '--param', type=str,
                        help='The parameters to increment', default="1")

    args = parser.parse_args()

    runtimes = []
    mesh_name = args.input_file.split("/")[-1]
    file_names = [
        f"{args.temp_dir}/{mesh_name.split('.')[0]}_{ind}.obj" for ind in range(0, args.num_iters + 1)]
    file_names[0] = args.input_file
    mesh_vertex_counts = []
    os.system("rm temp_inis")
    os.system("mkdir temp_inis")
    for ind in range(0, args.num_iters):
        inp_file = file_names[ind]
        out_file = file_names[ind+1]
        new_ini = configparser.ConfigParser()
        new_ini['IO'] = {
            'infile': inp_file,
            'outfile': out_file
        }
        new_ini["Method"] = {
            'method': args.command
        }
        new_ini["Parameters"] = {
            'args1' : args.param
        }
        if sys.platform == "win32":
            with open(f".\\temp_inis\\{args.command}_{ind}_{ind+1}.ini", 'w') as configfile:
                new_ini.write(configfile)
        else:
            with open(f"./temp_inis/{args.command}_{ind}_{ind+1}.ini", 'w') as configfile:
                new_ini.write(configfile)

        if sys.platform == "win32":
            sys_command = f"{args.compiled_file} .\\temp_inis\\{args.command}_{ind}_{ind+1}.ini"
        else:
            sys_command = f"{args.compiled_file} ./temp_inis/{args.command}_{ind}_{ind+1}.ini"
        
        print(sys_command)
        start_time = time.perf_counter()
        os.system(sys_command)
        end_time = time.perf_counter()
        runtimes.append((end_time - start_time) * 1000)
        vertex_count = get_vertex_count(inp_file)
        mesh_vertex_counts.append(vertex_count)

    # plot
    xs = np.linspace(4, max(mesh_vertex_counts), 100)

    y_linear = xs
    y_linear = y_linear * max(runtimes) / max(y_linear)
    y_nlogn = xs * np.log(xs)
    y_nlogn = y_nlogn * max(runtimes) / max(y_nlogn)
    y_nn = xs * xs
    y_nn = y_nn * max(runtimes) / max(y_nn)

    plt.figure()
    # dashed
    plt.plot(mesh_vertex_counts, runtimes, label="Yours", color="blue")
    plt.plot(xs, y_linear, label="n", color="red")
    plt.plot(xs, y_nlogn, label="nlogn", color="green")
    plt.plot(xs, y_nn, label="n^2", color="black")
    plt.legend(loc="lower right")
    plt.ylabel("time in milliseconds")
    plt.xlabel("Size of mesh")
    plt.title(f"{args.command} timing results")
    plt.savefig(args.output_file)