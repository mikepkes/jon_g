#!/usr/bin/python3

def helix_plunge(cmd, x, y, z, depth, feed, step, radius, tool_diameter=None):

    # If the tool diameter was given, reduce the diameter.
    if tool_diameter:
        radius_c = radius - (tool_diameter*.5)
        if radius_c <= 0.0:
            raise Exception("Radius is too small for tool diameter.")
    else:
        radius_c = radius

    # Move to the start position.  This could probably be a rapid.
    cmds = f"G01 X{x-radius_c} Y{y} Z{z} F{feed}\n"
    zpos = z
    opp = True
    while zpos > z-depth:
        zpos = max(zpos-(step*.5), z-depth)
        if opp:
            cmds += f"{cmd} X{x+radius_c} I{radius_c} Z{zpos} F{feed}\n"
        else:
            cmds += f"{cmd} X{x-radius_c} I{-radius_c} Z{zpos} F{feed}\n"
        opp = not opp

    #Finish the bottom circle at full depth.
    if opp:
        cmds += f"{cmd} X{x+radius_c} I{radius_c} Z{zpos} F{feed}\n"
    else:
        cmds += f"{cmd} X{x-radius_c} I{-radius_c} Z{zpos} F{feed}\n"
    opp = not opp

    #Rotate back into center while rising a step.
    if opp:
        cmds += f"{cmd} X{x} I{radius_c*.5} Z{min(zpos+step, z)} F{feed}\n"
    else:
        cmds += f"{cmd} X{x} I{-radius_c*.5} Z{min(zpos+step, z)} F{feed}\n"

    # Return to initial start.
    cmds += f"G01 Z{z} F{feed}"

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
    parser.add_argument("-c", "--command", type=str, choices=["G02", "G03"], default="G02", help="Command, either G02 (clockwise) or G03 (counter-clockwise), default G02")
    parser.add_argument("-td", "--tool_diameter", type=float, default=None, help="Tool diameter")

    args = parser.parse_args()

    print(helix_plunge(
        args.command,
        args.x,
        args.y,
        args.z,
        args.depth,
        args.feed,
        args.step,
        args.radius,
        tool_diameter=args.tool_diameter
    ))
