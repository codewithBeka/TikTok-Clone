const profile_click =document.querySelector("#profile-show")
const profile_dropdown =document.querySelector(".profile-down")


profile_click.addEventListener("click",()=>{
    profile_dropdown.classList.toggle("show")
    console.log(profile_dropdown)
})

const videos = document.querySelectorAll('#video-item');

function observeVideos() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.play();
        } else {
          entry.target.pause();
        }
      });
    },
    { threshold: 0.5 } // Play/pause when 50% of the video is in view
  );

  videos.forEach((video) => {
    observer.observe(video);
  });
}

observeVideos();