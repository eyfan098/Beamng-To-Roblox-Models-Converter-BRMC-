const { exec } = require("child_process");

function updateProgress(percent, text) {
  document.getElementById("progress").style.width = percent + "%";
  if(text) document.getElementById("status").innerText = text;
}

function convert() {
  let file = document.getElementById("file").files[0];
  if (!file) return alert("Select a BeamNG mod zip");

  // Reset progress
  updateProgress(0, "Starting conversion...");

  // Step 1: Extracting ZIP
  updateProgress(10, "Extracting files...");

  // Run Python conversion
  const py = exec(`python convert.py "${file.path}"`);

  // Read Python stdout for live updates
  py.stdout.on('data', (data) => {
    if(data.includes("Extracting ZIP")) updateProgress(10, "Extracting files...");
    else if(data.includes("Converting textures")) updateProgress(50, "Converting textures...");
    else if(data.includes("Importing model")) updateProgress(70, "Importing model to Blender...");
    else if(data.includes("Exporting FBX")) updateProgress(90, "Exporting FBX...");
    else if(data.includes("DONE")) updateProgress(100, "Finished! FBX exported.");
  });

  py.stderr.on('data', (data) => {
    console.error(data);
    updateProgress(0, "Error occurred during conversion");
  });

  py.on('close', (code) => {
    if(code !== 0){
      updateProgress(0, "Conversion failed!");
    }
  });
}
