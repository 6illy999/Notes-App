 function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/";
        
    });
}


document.addEventListener("DOMContentLoaded", () => {
  

showMore()

function showMore() {
    const buttons = document.querySelectorAll(".more-vert");
    
    buttons.forEach( button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation(); // prevent triggering document click

            const popup = button.nextElementSibling;

            //close all popups first
            
            document.querySelectorAll(".popup").forEach(p => {
                if(p !== popup ) {
                    p.classList.remove("active")
                }                
            });
            
            //Toggle current popup
            popup.classList.toggle("active")
   
        })
    });

    document.addEventListener('click', () => {
            document.querySelectorAll(".popup").forEach(popup => {
                popup.classList.remove("active");
            });
            
        })

    window.addEventListener('resize', () => {
        if (window.innerWidth > 540) {
            document.querySelectorAll(".popup").forEach(popup => {
                popup.classList.remove("active");
            });
        }
    })    

}

})