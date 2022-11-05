import './style.css'
import { setupCounter } from './counter'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import {Color, EdgesGeometry} from 'three'

const appContainer = document.querySelector("#app")!
const width = window.innerWidth
const height = window.innerHeight

const scene = new THREE.Scene()

const camera = new THREE.OrthographicCamera(width/-2, width/2, height/2, height/-2, 0, 100)

camera.zoom = 60
camera.updateProjectionMatrix()
//const camera = new THREE.PerspectiveCamera(
//    75, window.innerWidth / window.innerHeight, 0.1, 1000
//)
const renderer = new THREE.WebGLRenderer( {antialias: true} )
scene.background = new THREE.TextureLoader().load("/space.jpeg")

renderer.setSize( window.innerWidth, window.innerHeight )
appContainer.appendChild( renderer.domElement )

const cubeGeometry = new THREE.BoxGeometry( 1, 1, 1 );
const cubeMaterial = new THREE.MeshStandardMaterial( { color: 0xeeeeee, opacity: 0.5, transparent: true } );
const lineMaterial = new THREE.LineBasicMaterial( { color: 0xcccccc, opacity: 1, transparent: true } )
const originLineMaterial = new THREE.LineBasicMaterial( { color: 0x00cc00, opacity: 1, transparent: true } )
const destinationLineMaterial = new THREE.LineBasicMaterial( { color: 0xcc0000, opacity: 1, transparent: true } )
const frontierLineMaterial = new THREE.LineBasicMaterial( { color: 0x8888ff, opacity: 1, transparent: true } )
const size = {
    x: 5.0,
    y: 5.0,
    z: 5.0
}

const data = await fetch("http://localhost:8080")
    .then(response => response.json())
console.log(data)


const origin = new THREE.Vector3(1, 1, 1)
const destination = new THREE.Vector3(5, 5, 5)

type role = "none" | "path" | "origin" | "destination" | "frontier"

const barrierGeo = new THREE.PlaneGeometry(1, 1)
const barrierMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000, opacity: 0.80, transparent: true, side: THREE.DoubleSide })

const parse_v3 = (d: string) => {
    return new THREE.Vector3(...d.split(" ").map(v => parseInt(v)))
}

const offset = 0.2
class SwarmCube {
    geo: THREE.BoxGeometry = cubeGeometry
    mesh: THREE.Mesh | null = null;
    outlineMesh: THREE.LineSegments | null = null
    position: THREE.Vector3 | null = null
    role: role = "none"
    constructor(i: number, j: number, k: number) {
        this.position = new THREE.Vector3(i, j, k)
    }
    add (scene: THREE.Scene) {
        this.mesh && scene.add( this.mesh );
        this.outlineMesh && scene.add( this.outlineMesh );
    }
    remove (scene: THREE.Scene) {
        this.role = "none"
        this.mesh && scene.remove( this.mesh );
        this.outlineMesh && scene.remove( this.outlineMesh );
    }
    createMeshes() {
        if(!this.position) {
            return
        }
        const i = this.position.x
        const j = this.position.y
        const k = this.position.z
        switch(this.role) {
            case "frontier": {
                const edges = new EdgesGeometry( this.geo )
                const lines = new THREE.LineSegments( edges, frontierLineMaterial );
                lines.position.set(
                    i+offset*i - size.x/2 - 0.5, 
                    j+offset*j - size.y/2 - 0.5, 
                    k+offset*k - size.z/2 - 0.5
                )
                this.outlineMesh = lines
                break;
            }
            case "origin": {
                const edges = new EdgesGeometry( this.geo )
                const lines = new THREE.LineSegments( edges, originLineMaterial );
                lines.position.set(
                    i+offset*i - size.x/2 - 0.5, 
                    j+offset*j - size.y/2 - 0.5, 
                    k+offset*k - size.z/2 - 0.5
                )
                this.outlineMesh = lines
                break;
            }
            case "destination": {
                if(!this.position) {
                    return
                }
                this.role = "destination"
                const edges = new EdgesGeometry( this.geo )
                const lines = new THREE.LineSegments( edges, destinationLineMaterial );
                lines.position.set(
                    i+offset*i - size.x/2 - 0.5, 
                    j+offset*j - size.y/2 - 0.5, 
                    k+offset*k - size.z/2 - 0.5
                )
                this.outlineMesh = lines
                break;
            }
        }
        if(this.role != "frontier") {
            const cube = new THREE.Mesh( this.geo, cubeMaterial );
            cube.position.set(i+offset*i - size.x/2 - 0.5, j+offset*j - size.y/2 - 0.5, k+offset*k - size.z/2 - 0.5)
            this.mesh = cube
        }
    }
    setCovered() {
        this.role = "path"
    }
    setFrontier() {
        this.role = "frontier"
    }
    setDestination () {
        this.role = "destination"
    }
    setOrigin () {
        this.role = "origin"
    }
}

class Barrier {
    change_basis = new THREE.Vector3(-1, -1, -1) // (1 1 1) to (0 0 0) origin
    constructor(fromV3: THREE.Vector3, toV3: THREE.Vector3) {
        const delta = toV3.sub(fromV3)
        fromV3.add(this.change_basis)
        const x = fromV3.x
        const y = fromV3.y
        const z = fromV3.z
        console.log(fromV3, toV3, x, y, z)
        const mesh = new THREE.Mesh( barrierGeo, barrierMaterial )
        mesh.position.set(
            x+offset*x - size.x/2 - 0.5 + delta.x*(0.5 + offset/2), 
            y+offset*y - size.y/2 - 0.5 + delta.y*(0.5 + offset/2), 
            z+offset*z - size.z/2 - 0.5 + delta.z*(0.5 + offset/2), 
        )
        mesh.rotation.set(
            Math.PI/2*delta.y, 
            Math.PI/2*delta.x, 
            Math.PI/2*delta.z 
        ) // still no clue why x and y swapped. Weird
        scene.add(mesh)
    }
}
for (const barrier of data.bannedPaths) {
    let l = parse_v3(barrier[0])
    let r = parse_v3(barrier[1])
    console.log(l, r)
    new Barrier(l, r)
}

const cubes: SwarmCube[][][] = []
const createInnerCubes = () => {
    for(let i = 0; i < size.x; i++) {
        cubes.push([])
        for(let j = 0; j < size.y; j++) {
            cubes[i].push([])
            for(let k = 0; k < size.z; k++) {
                const sc = new SwarmCube(i, j, k)
                if (new THREE.Vector3(i+1, j+1, k+1).equals(origin)) {
                    sc.setOrigin()
                    sc.createMeshes()
                    sc.add(scene)
                }
                if (new THREE.Vector3(i+1, j+1, k+1).equals(destination)) {
                    sc.setDestination()
                    sc.createMeshes()
                    sc.add(scene)
                }
                cubes[i][j][k] = sc
            }
        }
    }
}


const process_input = (data: any) => {
    for (const plane of cubes.flat()) {
        for (const cube of plane.flat()) {
            if(cube.role == "origin" || cube.role == "destination") {}
            else {
                cube.remove(scene)
            }
        }
    }
    for (const c of data.frontier) {
        const coords = c
        const cube = cubes[coords[0]-1][coords[1]-1][coords[2]-1]
        cube.setFrontier()
        cube.createMeshes()
        cube.add(scene)
    }
    for (const c of data.covered_tiles) {
        const coords = c
        const cube = cubes[coords[0]-1][coords[1]-1][coords[2]-1]
        cube.setCovered()
        cube.createMeshes()
        cube.add(scene)
    }


}

const create_iterator_handler = () => {
    const len = data.iterations.length-1
    const el: HTMLInputElement = document.createElement("input")
    el.type = "range"
    el.min = "0"
    el.max = len.toString()
    el.id = "iter"
    el.oninput = (e) => {
        const d = data.iterations[el.value]
        console.log(el.value)
        iter < len && process_input(d)
    }
    document.body.appendChild(el)

    const IteratorButton = document.querySelector("#iter")!
    let iter = 0
    IteratorButton.addEventListener('click', () => {
        iter++
    })
}
create_iterator_handler()


const spotlight = new THREE.SpotLight(0xffffff, 1)
spotlight.lookAt(0, 0, 0)
scene.add(spotlight)

const createOuterCube = () => {
    const geometry = new THREE.BoxGeometry( 
        size.x+offset*size.x, 
        size.y+offset*size.y, 
        size.z+offset*size.z, 
    );
    const edges = new EdgesGeometry( geometry )
    const outerCube = new THREE.LineSegments( edges, lineMaterial );
    outerCube.position.set(-0.6, -0.6, -0.6)
    scene.add(outerCube)
    
}
createInnerCubes()
createOuterCube()



camera.position.z = 10


const controls = new OrbitControls( camera, renderer.domElement )
controls.update()

const onPositionChange = (o?: any) => {
    spotlight.position.set(camera.position.x, camera.position.y, camera.position.z)
    
}
onPositionChange()

controls.addEventListener('change', onPositionChange)

function animate() {
	requestAnimationFrame( animate );
    controls.update()
	renderer.render( scene, camera );
}
animate()



setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
