#!/usr/bin/python3

def helix_plunge(x, y, z, depth, feed, step, radius):
    cmds = f"G01 X{x-radius} Y{y} Z{z}\n"
    zpos = z
    while zpos > z-depth:
        zpos = max(zpos-step, z-depth)
        cmds += f"G02 X{x-radius} I{radius} Z{zpos} F{feed}\n"
    return cmds

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=float, help="X Center", required=True)
    parser.add_argument("-y", type=float, help="Y Center", required=True)
    parser.add_argument("-z", type=float, help="Z Center", required=True)
    parser.add_argument("-d", "--depth", type=float, help="depth", required=True)
    parser.add_argument("-f", "--feed", type=float, help="feed", required=True)
    parser.add_argument("-s", "--step", type=float, help="step", required=True)
    parser.add_argument("-r", "--radius", type=float, help="radius", required=True)

    args = parser.parse_args()

    print(helix_plunge(
        args.x,
        args.y,
        args.z,
        args.depth,
        args.feed,
        args.step,
        args.radius
    ))