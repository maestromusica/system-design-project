import React, {Component} from 'react'
import * as THREE from 'three'
const OrbitControls = require('three-orbit-controls')(THREE)
import {adaptCoordinates, createMeshMaterial} from '../../utils/simulation'
import {
  Button,
  RadioGroup,
  RadioAligned
} from '../../styled/components'
import {
  Section,
  SectionTitle,
  SectionItem
} from '../../styled/section'

export default class SimulationRenderer extends Component {
  state = {
    scene: undefined,
    camera: undefined,
    cameraSize: {
      x: 20,
      y: 10,
      z: 14
    },
    boxes: [],
    simulationOngoing: false,
    simulationFinished: false,
    level: -1
  }

  _resetLevel(level) {
    this.state.boxes[level].forEach(id => {
      let box = this.state.scene.getObjectByName(id)
      box.material.opacity = 0.95
    })
  }

  _hideLevel(level) {
    this.state.boxes[level].forEach(id => {
      let box = this.state.scene.getObjectByName(id)
      box.material.opacity = 0.2
    })
  }

  _showLevel(level) {
    const numOfLvls = this.state.boxes.length
    if(level === -1) {
      // this means we should show all levels
      for(let i=0; i<numOfLvls; i++) {
        this._resetLevel(i)
      }
    }
    else {
      for(let i=0; i<numOfLvls; i++) {
        if(i == level) {
          this._resetLevel(i)
        }
        else {
          this._hideLevel(i)
        }
      }
    }
  }

  _cleanRenderer(cb) {
    this.state.boxes.forEach(level => {
      level.forEach(id => {
        const box = this.state.scene.getObjectByName(id)
        this.state.scene.remove(box)
      })
    })
    this.setState({
      boxes: []
    }, () => {
      cb.call(this)
    })
  }

  _addBoxesToRenderer() {
    let boxes = this.props.boxes

    let pos = 0
    boxes = boxes.map(level => {
      return level.map(box => {
        const adaptedCoordinates = adaptCoordinates(box, {
          xCamera: this.state.cameraSize.x,
          yCamera: this.state.cameraSize.y,
          zCamera: this.state.cameraSize.z
        })
        return {
          ...box,
          ...adaptedCoordinates
        }
      })
    }).map(level => {
      return level.map(box => {
        box.id = pos++
        return box
      })
    })

    let flattenedBoxes = []
    boxes.forEach(level => {
      level.forEach((box, id) => {
        flattenedBoxes.push(box)
      })
    })

    pos = 0

    const addToScene = () => {
      if(pos < flattenedBoxes.length) {
        const box = flattenedBoxes[pos]
        const itemGeometry = new THREE.BoxGeometry(box.width, box.height, box.depth)
        const itemMaterial = createMeshMaterial(box.color)
        let cube = new THREE.Mesh(itemGeometry, itemMaterial)
        cube.position.set(box.x, box.y, box.z)
        cube.name = box.id
        pos += 1
        this.state.scene.add(cube)

        let geo = new THREE.EdgesGeometry(cube.geometry)
        let mat = new THREE.LineBasicMaterial({color: 0x444444, linewidth: 2})
        let wireframe = new THREE.LineSegments(geo, mat)
        cube.add(wireframe);
      }
      else {
        window.clearInterval(intervalID)
        this.setState({
          simulationOngoing: false,
          simulationFinished: true
        })
      }
    }
    var intervalID

    this.setState({
      simulationOngoing: true,
      boxes: boxes.map(level => level.map(box => box.id))
    }, () => {
      intervalID = setInterval(addToScene, 300)
      this.setState({
        intervalID
      })
    })
  }

  componentDidMount() {
    let rendererWidth = (window.innerWidth - 280) / 1.5 - 80
    if(rendererWidth > 700) {
      rendererWidth = 700
    }
    const rendererHeight = rendererWidth / 1.5

    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera( 75, 1.5, 0.1, 1000)
    let controls = new OrbitControls(camera, document.getElementById("graph-sim"))
    camera.position.set(0, 20, 10)
    controls.update()

    let renderer = new THREE.WebGLRenderer();
    renderer.setClearColor( 0xf0f0f0 );
    renderer.setSize( rendererWidth , rendererHeight );
    document.getElementById('graph-sim').appendChild( renderer.domElement );

    camera.position.z = 5;
    renderer.render(scene, camera);

    let geometry = new THREE.BoxGeometry(
      this.state.cameraSize.x,
      this.state.cameraSize.y,
      this.state.cameraSize.z
    )

    let geo = new THREE.EdgesGeometry( geometry ); // or WireframeGeometry( geometry )
    let mat = new THREE.LineBasicMaterial( { color: 0x000000, linewidth: 2 } );
    let wireframe = new THREE.LineSegments( geo, mat );
    wireframe.position.set(0, 0, 0);
    wireframe.name = 'container';
    scene.add( wireframe );

    let light = new THREE.DirectionalLight(0xffffff)
    light.position.set(-20, 20, 20).normalize()
    scene.add(light);


    function animate() {
      requestAnimationFrame(animate);
      // required if controls.enableDamping or controls.autoRotate are set to true
      controls.update();
      renderer.render(scene, camera);
    }

    animate();

    this.setState({
      scene: scene
    })
  }

  componentWillUnmount() {
    window.clearInterval(this.state.intervalID)
    let el = document.getElementById("graph-sim")
    el.outerHTML = ""
  }

  render() {
    let levels = []

    if(this.state.simulationFinished) {
      let numOfLvls = this.state.boxes.length
      levels.push(
        <RadioAligned value={-1} onClick={ev => {
          this.setState({
            level: -1
          })
          this._showLevel(-1)
        }} key={-1}>
          All levels
        </RadioAligned>
      )
      for(let i=numOfLvls-1; i>=0; i--) {
        levels.push(
          <RadioAligned value={i} onClick={ev => {
            this.setState({
              level: i
            }, () => {
              this._showLevel(i)
            })
          }} key={i}>
            Level {i}
          </RadioAligned>
        )
      }
    }
    else {
      levels = null
    }

    return (
      <Section>
        <SectionTitle>Simulations</SectionTitle>
        <SectionItem id="graph-sim"></SectionItem>
        <Button onClick={ev => {
          this._cleanRenderer(() => {
            this.setState({
              simulationOngoing: true,
              simulationFinished: false,
              level: -1
            })
            this._addBoxesToRenderer()
          })
        }} disabled={this.state.simulationOngoing}>
          Start mocked simulation
        </Button>
        {this.state.simulationFinished ? (
          <RadioGroup value={this.state.level}>
            {levels}
          </RadioGroup>
        ) : (
          null
        )}
      </Section>
    )
  }
}
