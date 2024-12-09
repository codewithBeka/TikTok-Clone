const fileInput = document.getElementById("file-input");
const upload_input = document.getElementById("upload-input");
const uploadedVideo = document.getElementById("uploaded-video");

function previewVideo() {
  const file = fileInput.files[0];
  if (!file) {
    uploadedVideoContainer.classList.remove("upload_show"); // Hide container if no file selected
    return;
  }


  if (file.type !== 'video/mp4') {
    alert('Only MP4 videos are allowed.');
    return;
  }
  if (file) {
    upload_input.classList.add("remove");
    const videoUrl = URL.createObjectURL(file);
    console.log(videoUrl)


    uploadedVideo.innerHTML = `
    
             <video     
              autoPlay
              loop
              muted
              className=" absolute rounded-xl object-cover z-10 p-[13px] w-full h-full" 
              src="${videoUrl}" 
              >
               </video>

    
           <div
              class="absolute -bottom-12 flex items-center justify-between z-50 rounded-xl border w-full p-2 border-gray-300">
              <div class="flex items-center truncate">
                <AiOutlineCheckCircle size="16" class="min-w-[16px]" />
                <p class="text-[11px] pl-1 truncate text-ellipsis">${videoUrl.slice(5)}</p>
              </div>
              <button id="remove" class="text-[11px] ml-2 font-semibold">
                Change
              </button>
     
   
    `;
    console.log(uploadedVideo);
  }

}

