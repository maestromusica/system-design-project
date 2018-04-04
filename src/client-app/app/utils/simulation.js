import * as THREE from 'three'

export const adaptCoordinates = (
  {x, y, z, width, height, depth},
  {xCamera, yCamera, zCamera}
) => {
  // the 0, 0, 0 position is in fact the center of the box
  const obj = {
    x: x -xCamera/2 ,
    y: y + height/2 - yCamera/2,
    z: z - zCamera/2,
    width,
    height,
    depth,
  }
  console.log(obj)
  return obj
}

export const adaptBoxCoords = (bins) => {
  bins = bins.map((bin, level) => {
    return bin.map((box, idx) => {
      const width = box.rotateto == 90 ? box.length : box.width
      const length = box.rotateto == 90 ? box.width : box.length
      return {
        height: 4,
        width: width * 2,
        depth: length * 2,
        color: box.colour,
        x: (box.centreto[0]) * 2,
        y: level * 4,
        z: (box.centreto[1]) * 2
      }
    })
  })
  console.log("Bins: ", bins)
  return bins
}

export const adaptColor = color => {
  switch(color) {
    case "green":
      return 0x124c15
    case "red":
      return 0xbf3e1e
    case "blue":
      return 0x39c3e5
    case "pink":
      return 0xe082c4
    case "yellow":
      return  0xefb12b
    case "orange":
      return 0xf47e24
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
