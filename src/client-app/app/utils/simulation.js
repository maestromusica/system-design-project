export const adaptCoordinates = (
  {x, y, z, width, height, depth},
  {xCamera, yCamera, zCamera}
) => {
  // the 0, 0, 0 position is in fact the center of the box
  return {
    x: x + width/2 -xCamera/2 ,
    y: y + height/2 - yCamera/2,
    z: z + depth/2 - zCamera/2,
    width,
    height,
    depth
  }
}
