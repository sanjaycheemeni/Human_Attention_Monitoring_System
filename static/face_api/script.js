const video = document.getElementById('video')
const cur_usr =  getUser()
const session_key = getSeesionKey()

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('static/face_api/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('static/face_api/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('static/face_api/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('static/face_api/models')
]).then(startVideo)

function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

// video.addEventListener('play', () => {
//   const canvas = faceapi.createCanvasFromMedia(video)
//   document.body.append(canvas)
//   const displaySize = { width: video.width, height: video.height }
//   faceapi.matchDimensions(canvas, displaySize)
//   setInterval(async () => {
//     const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
//     const resizedDetections = faceapi.resizeResults(detections, displaySize)
//     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
//     faceapi.draw.drawDetections(canvas, resizedDetections)
//     faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
//     console.log(detections[0]['landmarks'])
//     faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
//   }, 100)
// })

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video)
  document.body.append(canvas)
  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    
    
  
    try{
      
      var landmarks = resizedDetections[0]['landmarks']._positions;

      //calculation of E.A.R (left eye)
      var left_p2_p6  = parseFloat(dist(landmarks[37]._x,  landmarks[37]._y,landmarks[41]._x,  landmarks[41]._y))
      var left_p3_p5  = parseFloat(dist(landmarks[38]._x,  landmarks[38]._y,landmarks[40]._x,  landmarks[40]._y))
      var left_p1_p4  = parseFloat(dist(landmarks[36]._x,  landmarks[36]._y,landmarks[39]._x,  landmarks[39]._y))

      var left_EAR = parseFloat( (left_p2_p6 + left_p3_p5)/(2*left_p1_p4))

      //calculation of E.A.R (left eye)
      var right_p2_p6  = parseFloat(dist(landmarks[37]._x,  landmarks[37]._y,landmarks[41]._x,  landmarks[41]._y))
      var right_p3_p5  = parseFloat(dist(landmarks[38]._x,  landmarks[38]._y,landmarks[40]._x,  landmarks[40]._y))
      var right_p1_p4  = parseFloat(dist(landmarks[36]._x,  landmarks[36]._y,landmarks[39]._x,  landmarks[39]._y))

      var right_EAR = parseFloat( (right_p2_p6 + right_p3_p5)/(2*right_p1_p4))



      // calculation of M.A.R
      var p2_p8  = parseFloat(dist(landmarks[61]._x,  landmarks[61]._y,landmarks[67]._x,  landmarks[67]._y))
      var p3_p7  = parseFloat(dist(landmarks[62]._x,  landmarks[62]._y,landmarks[66]._x,  landmarks[66]._y))
      var p4_p6  = parseFloat(dist(landmarks[63]._x,  landmarks[63]._y,landmarks[65]._x,  landmarks[65]._y))
      var p1_p5  = parseFloat(dist(landmarks[60]._x,  landmarks[60]._y,landmarks[64]._x,  landmarks[64]._y))

      var MAR = parseFloat(p2_p8 + p3_p7 + p4_p6)/(2*p1_p5)
      

      // identifying emotion of user
      var emotion = findEmotion(resizedDetections[0]['expressions'])

      if ( MAR > parseFloat(0.7000))  
        console.log("yawning..!!")
      if (left_EAR < 0.3)
        console.log("eye blinked..!!")

      // console.log(getSeesionKey())
      //  uploooooaaaaading...
      var cur_usr =  getUser()
      var session_key = getSeesionKey()
      EAR = parseFloat((left_EAR+right_EAR)/2)
      data = {
          "session_key" : session_key,"user" : cur_usr,"MR" :  MAR, "EAR" : EAR
      }
      // uploadLog(data)
      
    }
    catch(err){
      console.log('Face Reading failed...trying next frame!!')
    }


  
    
  }, 1000)
})

function dist(x1,y1,x2,y2){
    return parseFloat(Math.sqrt( (parseFloat(x1-x2)*parseFloat(x1-x2)) + (parseFloat(y1-y2)*parseFloat(y1-y2))))
}

function findEmotion(dict) {
  let maxVal = -Infinity;
  let maxKey = null;
  
  for (const [key, value] of Object.entries(dict)) {
    if (value > maxVal) {
      maxVal = value;
      maxKey = key;
    }
  }
  
  return maxKey;
}


// JSON.parse('{"session_key":${session_key}, "user_id":usr, "mar":, "ear":"New York"}')


// JSON.parse('{"session_key" : "session_key",
//                               "user_id" :${usr},
//                               "mar" : mar,
//                               "ear":ear, }')

