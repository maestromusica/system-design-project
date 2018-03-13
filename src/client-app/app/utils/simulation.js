import * as THREE from 'three'

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
    depth,
  }
}

export const adaptColor = color => {
  switch(color) {
    case "green":
      return 0x124c15
    case "red":
      return 0xbf3e1e
    case "blue":
      return 0x39c3e5
    case "purple":
      return 0xe082c4
    case "yellow":
      return  0xefb12b
    default:
      return 0x666666 // black-ish color
  }
}

export const createMeshMaterial = color => {
  let colorHex = adaptColor(color)

  return new THREE.MeshBasicMaterial({
    color: colorHex,
    // flatShading: true,
    transparent: true,
    opacity: 0.95
  })
}
