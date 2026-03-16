const { exec } = require("child_process");

function updateProgress(percent, text){
  document.getElementById("progress").style.width = percent + "%";
  if(text) document.getElementById("status").innerText = text;
}

function convert(){
  let file = document.getElementById("file").files[0];
  if(!file) return alert("Select a BeamNG mod ZIP");

  updateProgress(0, "Starting conversion...");

  // Run Python converter
  const py = exec(`python convert.py "${file.path}"`);

  py.stdout.on('data', (data) => {
    data = data.toString();

    // Update progress based on Python step messages
    if(data.includes("EXTRACT_FILE")) {
      let parts = data.split(":");
      let index = parseInt(parts[1]);
      let total = parseInt(parts[2]);
      let percent = 10 + (index/total)*40; // Extracting files 10–50%
      updateProgress(percent, `Extracting file ${index}/${total}`);
    }
    else if(data.includes("CONVERT_TEXTURE")) updateProgress(60, "Converting textures...");
    else if(data.includes("IMPORT_MODEL")) updateProgress(80, "Importing model in Blender...");
    else if(data.includes("EXPORT_FBX")) updateProgress(95, "Exporting FBX...");
    else if(data.includes("DONE")) updateProgress(100, "Finished! FBX exported.");
  });

  py.stderr.on('data', (err) => {
    console.error(err.toString());
    updateProgress(0, "Error occurred during conversion!");
  });

  py.on('close', (code) => {
    if(code !== 0){
      updateProgress(0, "Conversion failed!");
    }
  });
}
