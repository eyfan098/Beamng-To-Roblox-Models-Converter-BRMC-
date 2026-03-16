const {exec} = require("child_process")

function convert(){

let file=document.getElementById("file").files[0]

if(!file)return

document.getElementById("status").innerText="Converting..."

exec(`python convert.py "${file.path}"`,(err)=>{

if(err){
document.getElementById("status").innerText="Conversion failed"
return
}

document.getElementById("status").innerText="Finished! Check output folder."

})

}
