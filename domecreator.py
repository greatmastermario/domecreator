import math

min_height = -63
max_height = 320


def create_dome(x, y, z, radius):
    if y > max_height:
        raise ValueError
    dome_coords = list()
    add_coords(x, y, z, radius, dome_coords)
    return dome_coords


def add_coords(x, y, z, radius, dome_coords):
    max_y = [max_height + 1, y + radius + 1]
    current_layer = None
    layer_coords = list()
    for height_index in range(0, math.ceil(math.pi * 20 * radius)):
        dy, flat_radius = height(height_index, radius)
        if (dy + y) in max_y:
            return
        elif dy + y < min_height:
            continue
        if round_abs(y + dy) != current_layer:
            print("Adding layer " + str(current_layer) + " to coords")
            for layer_coord in layer_coords:
                dome_coords.append(layer_coord)
            layer_coords.clear()
            current_layer = round_abs(y + dy)
        add_ring(x, y + dy, z, flat_radius, layer_coords)
    for layer_coord in layer_coords:
        dome_coords.append(layer_coord)


def height(height_index, radius):
    theta_height = math.atan(1.0 / 40.0 / radius)
    y = math.sin(theta_height * height_index) * radius
    flat_radius = math.cos(theta_height * height_index) * radius
    return y, flat_radius


def add_ring(x, y, z, radius, dome_coords):
    for ring_index in range(0, math.ceil(math.pi * 80 * radius)):
        theta_flat = math.atan(1.0 / 40.0 / radius)
        dx = math.cos(theta_flat * ring_index) * radius
        dz = math.sin(theta_flat * ring_index) * radius
        next_coord = (round_abs(x + dx), round_abs(y), round_abs(z + dz))
        if next_coord not in dome_coords:
            dome_coords.append(next_coord)


def round_abs(val):
    signum = math.copysign(1, val)
    unsigned = round(abs(val))
    return int(unsigned * signum)


if __name__ == "__main__":
    input_x = int(input("Origin X: "))
    input_y = int(input("Origin Y: "))
    input_z = int(input("Origin Z: "))
    input_radius = int(input("Radius: "))
    output_file = input("File location: ")
    output_coords = create_dome(input_x, input_y, input_z, input_radius)
    if len(output_coords) == 0:
        print("Unable to generate coordinates; no coords found")
    with open(output_file, "w") as file:
        for coord in output_coords:
            file.write(str(coord))
            file.write("\n")
